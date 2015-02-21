__author__ = 'lovro'

from pymongo import MongoClient


class MongoDB:
    HOST = 'localhost'
    PORT = 27017

    client = ""
    ManaWorld = ""
    ManaWorldCollection = ""

    def __init__(self):
        self.connect_mongo_db()
        pass

    def connect_mongo_db(self):
        """
        Method that makes connection to the local database
        """
        self.client = MongoClient(self.HOST, self.PORT)

    def get_manaworld_database(self):
        """
        Method gives instance of mongoDB
        :return: Instance of document for ManaWorld in MongoDB
        """
        self.ManaWorld = self.client.ManaWorld
        return self.ManaWorld
        #self.get_manaworld_collection()

    def get_manaworld_collection(self):
        """
        Method that returns MW data collection where we can store game data
        """
        self.ManaWorldCollection = self.ManaWorld.ManaWorldDB
        return self.ManaWorldCollection


