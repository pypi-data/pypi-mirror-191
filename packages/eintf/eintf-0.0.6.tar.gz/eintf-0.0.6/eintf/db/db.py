import os

from pymongo import MongoClient

client = MongoClient(os.environ.get("EINDB"))
db = client['eintf']


def get_db():
    return db


def create_collection(collection_name: str):
    if collection_name not in db.list_collection_names():
        db.create_collection(collection_name)


def drop_collection(collection_name: str):
    return db.drop_collection(collection_name)


def insert_to_collection(collection_name: str, update: dict):
    get_collection(collection_name).insert_one(update)


def get_collection(collection_name: str):
    create_collection(collection_name)
    return db.get_collection(collection_name)
