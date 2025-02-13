from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import pandas as pd
import json
import qrcode

PWD = open("Databastyper/Kunskapkontroll_1/mongoDB/mongodb.pwd", "r").read().strip()
uri = f"mongodb+srv://theodor:{PWD}@database.if42v.mongodb.net/?retryWrites=true&w=majority&appName=Database"

client = MongoClient(uri, server_api=ServerApi('1'))
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

database = client["Database"]
collection = database["Suplier_&_pruducts"]

csv_file = "Databastyper/Kunskapkontroll_1/mongoDB/products.csv"
json_file = "Databastyper/Kunskapkontroll_1/mongoDB/suppliers.json"

df_csv = pd.read_csv(csv_file, encoding="utf-8")

with open(json_file, "r", encoding="utf-8") as file:
    json_data = json.load(file)
df_json = pd.DataFrame(json_data)

merged_df = df_json.merge(df_csv, on="SupplierID", how="left")  
merged_json = merged_df.to_dict(orient="records")

with open("merged_data.json", "w", encoding="utf-8") as file:
    json.dump(merged_json, file, indent=4)

collection.insert_many(merged_json)

query_math = {
    "$expr": {
        "$gt": ["$ReorderLevel", { "$add": ["$UnitsInStock", "$UnitsOnOrder"] }]
    }
}

result = collection.find(query_math)
data = list(result)

for idx, item in enumerate(data):
    qr_text = f"Företag: {item['CompanyName']}\nKontakt: {item['ContactName']}\nTelefon: {item['Phone']}"
    
    qr = qrcode.make(qr_text)
    
    qr_filename = f"Databastyper/Kunskapkontroll_1/mongoDB/qr_codes_{item['ProductName']}.png"
    qr.save(qr_filename)

    print(f"QR-kod skapad: {qr_filename}")
