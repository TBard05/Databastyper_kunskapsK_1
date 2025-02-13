from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import streamlit as st
import pandas as pd

st.title("Shopping list")

PWD = open("Databastyper/Kunskapkontroll_1/mongoDB/mongodb.pwd", "r").read().strip()
uri = f"mongodb+srv://theodor:{PWD}@database.if42v.mongodb.net/?retryWrites=true&w=majority&appName=Database"

client = MongoClient(uri, server_api=ServerApi('1'))

database = client["Database"]
collection = database["Suplier_&_pruducts"]

query_math = {
    "$expr": {
        "$gt": ["$ReorderLevel", { "$add": ["$UnitsInStock", "$UnitsOnOrder"] }]
    }
}

result = collection.find(query_math)
data = list(result)

for idx, item in enumerate(data):
    qr_text = f"Företag: {item['CompanyName']}\nKontakt: {item['ContactName']}\nTelefon: {item['Phone']}"

product_names = [item['ProductName'] for item in data]
product_counts = pd.Series(product_names).value_counts().reset_index()
product_counts.columns = ["Product Name", "Amount we need"]

st.write(product_counts)