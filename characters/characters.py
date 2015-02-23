#!/usr/bin/python

__author__ = 'lovro'

import os
import sys

sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))

import shutil

from helpers.hash_checker import HashChecker as Hash
from MongoDB.db_client import MongoDB


'''
 pseudo alg
 check file hash
 if hash is the same there is no change
 if there is change then we need parse users file
 check if there is user written in saved_chars.txt
 if user is not there it is new user and we need to save it into database
 when user is saved to database simply add its name into saved_users.txt
 copy latest saved file into directory
'''


class Characters:
    # path for characters file from game server
    chars_new = "athena.txt"

    # file path for local files with characters
    chars_text_file = "saved_chars.txt"
    chars_saved = "athena.txt"

    def __init__(self):
        """
        Constructor in which we set default paths for local athena.txt and char.txt and servers char txt file

        """
        self.chars_text_file = os.path.join(os.getcwd(), self.chars_text_file)
        self.chars_saved = os.path.join(os.getcwd(), self.chars_saved)


        # THIS PATH WILL BE REPLACED WITH ORIGINAL CHARACHTERS FILE
        #self.chars_new = os.path.join("/Users/lovro/coding/Python/MWlogScrapper/test_data", self.chars_new)

        #PATH ON SERVER /root/tmwAthena/tmwa-server-data/world/save
        self.chars_new = os.path.join("/root/tmwAthena/tmwa-server-data/world/save", self.chars_new)


    def check_hash(self):

        """
        Method that calls hash comparison of two files to determine if there is changes
        :rtype : Boolean
        """
        if self.check_file_exists(self.chars_new) and self.check_file_exists(self.chars_saved):
            hash_ = Hash()
            if not hash_.check_file_hash(self.chars_new, self.chars_saved):
                return False
            else:
                return True
        else:
            print "Sorry specified file doesn't exist"


    def get_accounts_from_server(self):
        """
        This method should get location of original servers data about user accounts
        """
        # Todo this method to work on server


    def check_file_exists(self, file_path):
        """
        Method that checks if specific file exists
        :param file_path:
        :return:
        """
        if os.path.isfile(file_path):
            return True
        else:
            return False

    def get_new_users(self):
        """
        Method that reads users data from servers original user accounts file
        """
        f = open(self.chars_new, 'r')
        for line in f:
            self.parse_character(line)

    def parse_character(self, line):

        """
        Method that parses accounts.txt file and if it's new user then we save it to database and append to
        saved_users.txt
        :rtype : object
        """

        user = line.split("\t")

        # Skipping reserved value for new user
        if user[1][0] == "%":
            return 0

        if not self.find_character(user[2]):
            self.save_character(user[0], user[1], user[2], user[18])

    def find_character(self, user):
        """
        Method that searches user in local saved_chars.txt file and returns true if it is find
        :rtype : Boolean
        """
        searchfile = open(self.chars_text_file, "r")
        for line in searchfile:
            if user in line:
                searchfile.close()
                return True

        searchfile.close()
        return False

    def save_character(self, char_id, user_id, char_name, quest_info):
        """
        Method that handles saving new users data to textfile and database
        :param user_id:
        """
        user_id = self.parse_user_id(user_id)

        if self.save_character_database(char_id, user_id, char_name, quest_info):
            self.save_character_text(char_name)
            self.replace_local_characters_file()

    def parse_user_id(self, user_id):
        """
        Method that takes fuzzed user_id returns clean user id
        :param user_id:
        :return:
        """
        return user_id.split(",")[0]

    def save_character_database(self, user, user_id, char_name, quest_info):
        """
        Method that provides saving new users data to database
        :param user:
        :param user_id:
        :return:
        """
        charachter = {"char_name": char_name,
                      "quest_info": quest_info}
        try:
            mongo = MongoDB()
            db = mongo.get_manaworld_database()

            db.ManaWorldDB.update(
                {"id_user": user_id},
                {"$push": {"charachters": charachter}})

            return True
        except:
            return False

    def save_character_text(self, user):
        """
        Method that saves new user to text file so we could check users again using it
        :param user:
        """
        with open(self.chars_text_file, "a") as myfile:
            myfile.write(user + "\n")

    def replace_local_characters_file(self):
        """
        Method that copies original account file to local copy which we use to calculate hash
        """
        shutil.copyfile(self.chars_new, self.chars_saved)


if __name__ == '__main__':
    charachters = Characters()
    if not charachters.check_hash():
        charachters.get_new_users()

    else:
        print "Nothing to do here..."
