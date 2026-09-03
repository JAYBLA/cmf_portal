import json

from .services import monthly_expenses, monthly_income


def get_monthly_income(year):
    return monthly_income(year)


def get_monthly_expenses(year):
    return monthly_expenses(year)


def get_monthly_profit(year):
    return [
        income - expense
        for income, expense in zip(
            get_monthly_income(year),
            get_monthly_expenses(year),
        )
    ]


def chart_data(year):
    # Resolve every source once so the totals and plotted series always agree.
    income = get_monthly_income(year)
    expenses = get_monthly_expenses(year)
    profit = [inc - exp for inc, exp in zip(income, expenses)]

    return {
        "income": json.dumps([float(value) for value in income]),
        "expenses": json.dumps([float(value) for value in expenses]),
        "profit": json.dumps([float(value) for value in profit]),
        "total_income": sum(income),
        "total_expenses": sum(expenses),
        "total_profit": sum(profit),
    }
