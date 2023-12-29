from pymongo.mongo_client import MongoClient

uri = "uri"

client = MongoClient(uri)
db = client.amino

def ping():
    try:
        client.admin.command('ping')
        print("Pinged your deployment. You successfully connected to MongoDB!")
    except Exception as e:
        print(e)
        
def addNewUser(uid=None):
    try:
        if uid is not None:
            if getUser(uid) is None:
                db.UsersInfo.insert_one(
                    {
                        "uid": uid,
                        "xp": 0,
                        "lvl": 1,
                        "background": 0
                    }
                )
                return "Carta criada com sucesso."
            else:
                return "Já tem uma carta de rank criada."
    except:
        return None
    
def getUser(uid=None):
    try:
        if uid is not None:
            uid = {'uid': uid}
            user = db.UsersInfo.find_one(uid)  # Use find_one to get a single user
            if user:
                return user
            else:
                return None
        return None
    except:
        return None

def updateUser(uid=None, xp=None, lvl=None, background=None):
    try:
        if uid is not None and xp is not None and lvl is not None and background is not None:
            uid = {'uid': uid}
            value = { "$set": {"xp": xp, "lvl": lvl, "background": background}}
            db.UsersInfo.update_one(uid, value)
    except:
        return None

def sortLeaderboard():
    try:
        pipeline = [
            {
                "$sort": {"lvl": -1, "xp": -1}
            },
            {
                "$limit": 5
            }
        ]

        topUsers = list(db.UsersInfo.aggregate(pipeline))
        return topUsers
    except:
        return None

def deleteUser(uid=None):
    try:
        if uid is not None:
            result = db.UsersInfo.delete_one({"uid": uid})
            if result.deleted_count == 1:
                return "Rank deletado com sucesso."
            else:
                return "User não encontrado."
    except:
        return None

def deleteAllUsers():
    try:
        result = db.UsersInfo.delete_many({})
        return f"Deletado {result.deleted_count} utilizadores."
    except:
        return None


