import pandas as pd
import automation_configs as configs
import numpy as np
import mysql.connector
from contextlib import contextmanager


@contextmanager
def connect(conn_string):
    conn = mysql.connector.connect(
        user=conn_string.user,
        password=conn_string.password,
        host=conn_string.host,
        database=conn_string.database,
    )
    try:
        yield conn
    finally:
        conn.close()

def select_all_stores():
    return f"""
select * from stores;
"""

def select_all_ordershistory():
        return f"""
select * from ordershistory;
"""


def select_all(table):
    return f"""
select * from {table}
"""

# Function to prepare data and update stores_ovenseconds
def update_stores_ovenseconds(conn, ovenseconds, storeno):
    # Replace this with your implementation to prepare and execute the update query
    update_query = f"UPDATE stores SET ovenseconds = {ovenseconds} WHERE StoreNo = '{storeno}';"
    conn.execute(update_query)

def main_for_ovenseconds():
    # Get user input for ovenseconds
    ovenseconds = int(input("Enter the value for ovenseconds:"))
    # Get user input for storenos, separated by a comma
    stores = input("Enter the storeno, separate by comma:").split(',')

def active_stores_by_date(conn, start_date, end_date, active_date):
    select_active_query = f"""
    SELECT COUNT(*) as [Live stores by {active_date}]
    FROM (
        SELECT DISTINCT StoreNo
        FROM (
            SELECT StoreNo, DueDate, MAX(ORDERID) AS MaxOrderID, COUNT(*) AS NumberOfOrders
            FROM OrdersHistory
            WHERE DueDate BETWEEN '{start_date}' AND '{end_date}'
            GROUP BY StoreNo, DueDate
        ) as d
        GROUP BY StoreNo
    ) as dd
    """
    cursor = conn.cursor()
    cursor.execute(select_active_query)
    result = cursor.fetchone()
    cursor.close()
    return result[0] if result else None


