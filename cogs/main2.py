from pymongo import MongoClient

cluster = MongoClient("mongodb+srv://dbrbase:oT4y7678BFK00Bsp@rodinadb.rhew3.mongodb.net/rodinaname?retryWrites=true&w=majority")
db = cluster["RodinaBD"]

moder = db["moders"]
print('Добавляю')
moder.update_one({"guild": 777, "id": 2}, {"$set": {"test": 22}}, upsert = True)
print('добавил')
