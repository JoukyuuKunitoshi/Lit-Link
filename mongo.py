from pymongo import MongoClient
import hashlib
from bson.objectid import ObjectId
import datetime

def hash_password(password):
    hash_object = hashlib.sha256()
    password_bytes = password.encode("utf-8")
    hash_object.update(password_bytes)
    return hash_object.hexdigest()

class DataBase:
    def __init__(self):
        cluster = MongoClient("mongodb://admin:AdminTop1166060088_SilverDenis05%40gmail.com_aue228_DeTrAdAl2005@217.25.94.249:27017/?directConnection=true&serverSelectionTimeoutMS=2000&appName=mongosh+2.2.5")
        self.db = cluster["BookExchange"]
        self.users = self.db["users"]
        self.books = self.db["books"]
        print("Database connected")

    def register(self, username, password):
        password = hash_password(password)
        if self.users.find_one({"username": username}):
            return "Username already taken!"
        user = {"username": username, "password": password, "permissions": ["user"]}
        self.users.insert_one(user)
        return True
    
    def login(self, username, password):
        password = hash_password(password)
        user = self.users.find_one({"username": username, "password": password})
        return user

    def add_book(self, username, title, author, link, description):
        book = {"username": username, "title": title, "author": author, "description": description, "link": link, "date": datetime.datetime.now()}
        return self.books.insert_one(book)

    def get_books(self, username):
        return self.books.find({"username": username})

    def get_all_books(self):
        return self.books.find({})

    def edit_book(self, book_id, action):
        if action == "delete":
            self.books.delete_one({"_id": ObjectId(book_id)})
            return action
        self.books.find_one_and_update({"_id": ObjectId(book_id)}, {"$set": {"status": action}})
        return action

    def admin(self, username):
        user = self.users.find_one({"username": username})
        return "admin" in user["permissions"]
