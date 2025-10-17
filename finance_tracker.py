from fastapi import FastAPI,HTTPException
from pydantic import BaseModel
from typing import Optional,List
from enum import Enum
from datetime import datetime

app=FastAPI(title="Finance Tracker API",version="1.0.0")

transactions_db=[]

class TransactionType(str,Enum):
    INCOME = "income"
    EXPENSE =  "expense"

class Category(str,Enum):
    FOOD = "food"
    TRANSPORT = "transport"
    ENTERTAINMENT="entertainment"
    BILLS="bills"
    SHOPPING = "shopping"
    SALARY="salary"
    OTHER="other"

class Transaction(BaseModel):
    id:int
    amount:float
    description:str
    type:TransactionType
    category:Category
    date:datetime

class TransactionCreate(BaseModel):
    amount:float
    description:str
    type:TransactionType
    category:Category

transaction_id_counter =1 

@app.post("/transactions",response_model = Transaction)

def create_transaction(transaction:TransactionCreate):
    global transaction_id_counter
    new_transaction = Transaction(
        id = transaction_id_counter,
        **transaction.dict(),
        date=datetime.now()
    )
    transactions_db.append(new_transaction)
    transaction_id_counter +=1
    return new_transaction

@app.get("/transactions")

def get_transactions():
    return transactions_db

@app.get("/transactions/{transaction_id}")

def get_transaction(transaction_id:int):
    for transaction in transactions_db:
        if transaction.id == transaction_id:
            return transaction
    raise HTTPException(status_code=404,detail="transaction not found")


@app.get("/balance")

def get_balance():
    total_income = sum(t.amount for t in transactions_db if t.type == TransactionType.INCOME)
    total_expenses = sum(t.amount for t in transactions_db if t.type == TransactionType.EXPENSE)

    return {
        "total_income":total_income,
        "total_expenses":total_expenses,
        "current_balance":total_income-total_expenses
    }

@app.get("/analytics/spending-by-category")

def spending_by_category():
    spending={}
    for transaction in transactions_db:
        if transaction.type ==TransactionType.EXPENSE:
            if transaction.category not in spending:
                spending[transaction.category]=0
            spending[transaction.category]+= transaction.amount

    return spending


@app.get("/analytics/monthly-summary")

def monthly_summary():
    current_month = datetime.now().month
    current_year = datetime.now().year

    monthly_income = 0
    monthly_expenses = 0

    for transaction in transactions_db:
        if transaction.date.month == current_month and transaction.date.year == current_year:
            if transaction.type == TransactionType.INCOME:
                monthly_income += transaction.amount
            elif transaction.type == TransactionType.EXPENSE:
                monthly_expenses += transaction.amount

    return {
        "month": current_month,
        "year": current_year,
        "monthly_income": monthly_income,
        "monthly_expenses": monthly_expenses,
        "monthly_balance":monthly_income-monthly_expenses
    }
