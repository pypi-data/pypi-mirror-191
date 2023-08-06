from abc import ABC, abstractmethod
from collections import OrderedDict
from copy import copy
from dataclasses import dataclass
from datetime import datetime, time, timedelta
from decimal import Decimal
from io import StringIO, TextIOBase
from sys import stdout
from typing import Any, ClassVar, List

from termcolor import colored

from lazy_budget.budget import Budget, FinancialOperation
from lazy_budget.helpers import generate_sequence_by_average_tree
from lazy_budget.money_provider import Money, format_money, get_zero
from lazy_budget.stats import BasicBudgetStats, get_categories_to_spendings


def format_percent(f: float):
    f *= 100
    return f"{f:.00f}%"


class LastUpdatedOrderedDict(OrderedDict):
    "Store items in the order the keys were last added"

    def __setitem__(self, key, value):
        super().__setitem__(key, value)
        self.move_to_end(key)


@dataclass
class BaseDisplay(ABC):
    locale: str

    def format_money(self, *args, **kwargs):
        return format_money(
            *args,
            locale=self.locale,
            **kwargs,
        )

    def __str__(self):
        result = StringIO()
        self.print(result)
        return result.getvalue()

    @abstractmethod
    def print(self, file: TextIOBase = stdout):
        raise NotImplementedError


@dataclass
class BaseStatListDisplay(BaseDisplay):
    separator: ClassVar = ":"

    def get_initial_data(self):
        return LastUpdatedOrderedDict()

    @abstractmethod
    def get_display_data(self) -> dict:
        """
        Returns a dict with data to display.
        """
        raise NotImplementedError

    def __str__(self):
        result = StringIO()
        self.print(result)
        return result.getvalue()

    def print(self, file: TextIOBase = stdout):
        menu_data = self.get_display_data()
        padding = (
            max(len(x) for x in menu_data.keys())  # right-adjusted text
            + 1  # one more space before the ":"
        )
        for stat_name, stat_value in menu_data.items():
            self.print_stat(stat_name, stat_value, padding, file)

    @classmethod
    def print_stat(
        cls,
        stat_name: str,
        stat_value: Any,
        padding: int,
        file: TextIOBase,
    ):
        print((stat_name).rjust(padding), cls.separator, stat_value, file=file)


@dataclass
class BaseBudgetStatsDisplay(BaseStatListDisplay):
    budget_stats: BasicBudgetStats

    @property
    def zero(self):
        return get_zero(self.budget_stats.currency)


class BasicStatsDisplay(BaseBudgetStatsDisplay):
    def get_display_data(self):
        data = self.get_initial_data()
        data["today"] = self.budget_stats.today
        data[
            "days left / total"
        ] = f"{self.budget_stats.days_left}/{self.budget_stats.total_days}"
        data[
            "total spent / avail"
        ] = f"{self.format_money(self.budget_stats.total_spent)} / {self.format_money(self.budget_stats.total_available)}"
        data["days% | money% left"] = "%s | %s" % (
            format_percent(self.budget_stats.days_left / self.budget_stats.total_days),
            format_percent(
                self.budget_stats.total_available / self.budget_stats.budget.total
            ),
        )
        data["avail / day"] = self.format_money(self.budget_stats.available_per_day)
        if self.budget_stats.can_spend_today > self.zero:
            data["CAN spend today"] = colored(
                self.format_money(abs(self.budget_stats.can_spend_today)),
                "green",
            )
        else:
            data["overspent"] = colored(
                self.format_money(abs(self.budget_stats.can_spend_today)),
                "red",
            )

        data["spent today"] = colored(
            self.format_money(self.budget_stats.spent_today),
            "green" if self.budget_stats.can_spend_today > self.zero else "red",
        )
        if self.budget_stats.can_spend_today < get_zero(self.budget_stats.currency):
            data["days until can spend"] = self.budget_stats.days_until_can_spend

        data["avg spent / day"] = self.format_money(self.budget_stats.avg_spent_per_day)
        if self.budget_stats.currently_keeping.amount < 0:
            loss = self.format_money(-self.budget_stats.currently_keeping)
            data["kept"] = colored(
                f"no keep, lost {loss}",
                "red",
            )
        else:
            data["kept"] = colored(
                self.format_money(self.budget_stats.currently_keeping),
                "green"
                if self.budget_stats.currently_keeping > self.budget_stats.budget.keep
                else "red",
            )

        return data


@dataclass
class SpentByCategoryDisplay(BaseStatListDisplay):
    budget: Budget
    operations: List[FinancialOperation]

    def get_display_data(self) -> dict:
        return {
            category or "<no category>": format_money(money_value, self.locale)
            for category, money_value in get_categories_to_spendings(
                self.budget, self.operations
            ).items()
        }


@dataclass
class NextDaysDisplay(BaseBudgetStatsDisplay):
    how_many_days: int = 5
    factor_in_average_spendings: bool = False
    no_spendings_today: bool = False
    prediction_coeff: Decimal = Decimal("1")
    avg_daily_spending: Decimal | None = None
    maximum_spent: Decimal | None = None

    def get_display_data(self) -> dict:
        data = self.get_initial_data()
        today = self.budget_stats.today
        budget_end = self.budget_stats.budget.end
        d = copy(today)
        if self.factor_in_average_spendings and not self.avg_daily_spending:
            self.avg_daily_spending = self.budget_stats.avg_spent_per_day.amount

        if not self.maximum_spent:
            self.maximum_spent = self.budget_stats.maximum_spent.amount

        if self.avg_daily_spending:
            predictions = generate_sequence_by_average_tree(
                expected_avg=round(
                    self.avg_daily_spending * self.prediction_coeff,
                    2,
                ),
                how_many_numbers=self.how_many_days,
                start=0,
                end=self.maximum_spent,
            )
            predictions = list(
                map(
                    lambda x: Money(x, currency=self.budget_stats.currency),
                    predictions,
                )
            )
            if self.no_spendings_today:
                predictions[0] = self.budget_stats.budget.zero
        else:
            predictions = None

        while (
            d <= budget_end and (days_passed := (d - today).days) < self.how_many_days
        ):
            daily_bonus = self.budget_stats.available_per_day * days_passed
            if predictions:
                available = (
                    self.budget_stats.can_spend_today
                    + daily_bonus
                    - sum(
                        predictions[: days_passed + 1],
                        start=self.budget_stats.budget.zero,
                    )
                )
            else:
                available = self.budget_stats.can_spend_today + daily_bonus

            value = colored(
                available,
                "red" if available < self.budget_stats.budget.zero else "green",
            )
            if predictions:
                after_spending = predictions[days_passed]
                if after_spending > self.budget_stats.budget.zero:
                    after_spending = format_money(after_spending, locale=self.locale)
                    value += f" after spending {after_spending}"

            data[d.isoformat()] = value
            d = (datetime.combine(d, time()) + timedelta(days=1)).date()
        return data


@dataclass
class IfResetDisplay(BaseStatListDisplay):
    now_stats: BasicBudgetStats
    reset_stats: BasicBudgetStats
    simple: bool = True

    def get_display_data(self) -> dict:
        if self.simple:
            return {
                "Current available/day": colored(
                    format_money(self.now_stats.available_per_day),
                    "red"
                    if self.now_stats.available_per_day
                    < self.reset_stats.available_per_day
                    else "green",
                ),
                "Reset available/day": colored(
                    format_money(self.reset_stats.available_per_day),
                    "red"
                    if self.now_stats.available_per_day
                    > self.reset_stats.available_per_day
                    else "green",
                ),
                "": "",
                "Current can spend": colored(
                    format_money(self.now_stats.can_spend_today),
                    "red"
                    if self.now_stats.can_spend_today < self.reset_stats.can_spend_today
                    else "green",
                ),
                "Reset can spend": colored(
                    format_money(self.reset_stats.can_spend_today),
                    "red"
                    if self.reset_stats.can_spend_today < self.now_stats.can_spend_today
                    else "green",
                ),
            }

        now_display = BasicStatsDisplay(self.locale, budget_stats=self.now_stats)
        reset_display = BasicStatsDisplay(self.locale, budget_stats=self.reset_stats)
        return {
            **{f"NOW {k}": v for k, v in now_display.get_display_data().items()},
            "": "",
            **{f"RESET {k}": v for k, v in reset_display.get_display_data().items()},
        }
