"""
Question 2: Customer Purchase Analysis

Using the provided dataset 'customer_purchases.csv', perform the following analyses:

1. Calculate the following metrics per customer:
   - Total amount spent
   - Average purchase value
   - Number of purchases
   - Most frequently bought category

2. Create a summary DataFrame with:
   - Top 5 customers by total spend
   - Bottom 5 customers by total spend

3. Calculate the monthly purchase trends:
   - Total sales per month
   - Average purchase value per month

Bonus: Identify any customers who haven't made a purchase in the last 3 months
"""

# Your code here
import pandas as pd
from datetime import datetime, timedelta


class Q2:
    def __init__(self, data_file="../data/customer_purchases.csv"):
        self._data = pd.read_csv(data_file)
        self._amount_spent = ""
        self._inactive = ""
        self._monthly_sales = ""
        self._summary = {}
        self._metrics()
        self._make_summary()
        self._monthly()
        self._customer_sleep()

    def _metrics(self):
        self._amount_spent = self._data.groupby("customer_id").agg(
            total=("amount", "sum"),
            mean=("amount", "mean"),
            number_purchase=("purchase_id", "count"),
            frequent_category=("category", lambda x: x.mode()),
        )

    def _make_summary(self):
        self._summary["top"] = self._amount_spent.sort_values("total", ascending=False)[
            0:5
        ]
        self._summary["bottom"] = self._amount_spent.sort_values(
            "total", ascending=True
        )[0:5]

    def _monthly(self):
        self._data["purchase_date"] = pd.to_datetime(self._data["purchase_date"])
        self._data["month"] = self._data["purchase_date"].dt.to_period("M")

        self._monthly_sales = (
            self._data.groupby("month")
            .agg(total_sales=("amount", "sum"), average=("amount", "mean"))
            .reset_index()
        )

    def _customer_sleep(self):
        _today = datetime.today()
        _last = self._data.groupby("customer_id")["purchase_date"].max().reset_index()
        self._inactive = _last[_last["purchase_date"] < (_today - timedelta(days=90))]

    def get_summary(self):
        return self._summary

    def get_metrics(self):
        return self._amount_spent

    def get_inactive(self):
        return self._inactive

    def get_monthly_sales(self):
        return self._monthly_sales
