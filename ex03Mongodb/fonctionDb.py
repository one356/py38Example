import pymongo


mdb = pymongo.MongoClient("localhost",27017,tz_aware=True)
def handler_db():
    newDb = mdb.test1
    print(newDb)
    newDb.user.insert({"name":"张三","psw":"aaa"})

if __name__ == "__main__":
    handler_db()