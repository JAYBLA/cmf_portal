import json
from decimal import Decimal

from .services import (
    monthly_sales,
    monthly_purchases,
)


# ==========================================================
# INCOME
# ==========================================================

def get_monthly_income(year):

    income = monthly_sales(year)

    # -------------------------------------------------
    # Future integrations
    # -------------------------------------------------

    # from projects.services import monthly_project_income
    #
    # project_income = monthly_project_income(year)
    #
    # for i in range(12):
    #     income[i] += project_income[i]

    return income


# ==========================================================
# EXPENSES
# ==========================================================

def get_monthly_expenses(year):

    expenses = monthly_purchases(year)

    # -------------------------------------------------
    # Future integrations
    # -------------------------------------------------

    # Office expenses
    #
    # office = monthly_office_expenses(year)
    #
    # for i in range(12):
    #     expenses[i] += office[i]

    # Project material expenses
    #
    # project = monthly_project_material_cost(year)
    #
    # for i in range(12):
    #     expenses[i] += project[i]

    # Payroll
    #
    # payroll = monthly_payroll(year)
    #
    # for i in range(12):
    #     expenses[i] += payroll[i]

    return expenses


# ==========================================================
# PROFIT
# ==========================================================

def get_monthly_profit(year):

    income = get_monthly_income(year)
    expenses = get_monthly_expenses(year)

    profit = []

    for inc, exp in zip(income, expenses):
        profit.append(inc - exp)

    return profit


# ==========================================================
# JSON FOR CHARTS
# ==========================================================

def chart_data(year):

    income = get_monthly_income(year)
    expenses = get_monthly_expenses(year)
    profit = get_monthly_profit(year)

    return {
        "income": json.dumps([float(i) for i in income]),
        "expenses": json.dumps([float(i) for i in expenses]),
        "profit": json.dumps([float(i) for i in profit]),

        "total_income": float(sum(income)),
        "total_expenses": float(sum(expenses)),
        "total_profit": float(sum(profit)),
    }