from pymongo import MongoClient


class Mongo:
    # Mongodb baglantisi ve database ismi
    client = MongoClient('mongodb://localhost:27017')
    db = client['data-test']
    courses = db.courses
