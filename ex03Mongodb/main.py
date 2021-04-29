import pymongo
class Datebase(object):
    def __init__(self,HOST,PORT):
        self.HOST = HOST
        self.PORT = PORT
    def mongodb_connect(self):
        db = pymongo.MongoClient(host=self.HOST,port=self.PORT,tz_aware=True)
        r = db.practice01.user.find()
        for i in r:
            print(i)

    # def mysqldb_connect(self):
    #     pass

if __name__ == "__main__":
    mdb = Datebase("localhost",27017)
    mdb.mongodb_connect()  
    
    
    
