__author__ = 'lovro'

import os
import shutil
from server.private.helpers.hash_checker import HashChecker as Hash
from server.private.MongoDB.db_client import MongoDB

'''
 pseudo alg
 check file hash
 if hash is the same there is no change
 if there is change then we need parse users file
 check if there is user written in saved_users.txt
 if user is not there it is new user and we need to save it into database
 when user is saved to database simply add its name into saved_users.txt
 copy latest saved file into directory
'''


class Accounts:
    # accounts files paths for files that have users info
    accounts_new = "account.txt"

    # file path for file with user names
    accounts_text_file = "saved_users.txt"
    accounts_saved = "account.txt"

    def __init__(self):
        """
        Constructor in which we set default paths for local saved_users.txt and accounts.txt and servers txt file

        """
        self.accounts_text_file = os.path.join(os.getcwd(), self.accounts_text_file)
        self.accounts_saved = os.path.join(os.getcwd(), self.accounts_saved)


        # todo path for accounts from server
        self.accounts_new = os.path.join("/Users/lovro/coding/Python/MWlogScrapper/test_data",
                                         self.accounts_new)


    def check_hash(self):

        """
        Method that calls hash comparison of two files to determine if there is changes
        :rtype : Boolean
        """
        if self.check_file_exists(self.accounts_new) and self.check_file_exists(self.accounts_saved):
            hash_ = Hash()
            if not hash_.check_file_hash(self.accounts_new, self.accounts_saved):
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
        f = open(self.accounts_new, 'r')
        for line in f:
            self.parse_user(line)

    def parse_user(self, line):

        """
        Method that parses accounts.txt file and if it's new user then we save it to database and append to saved_users.txt
        :rtype : object
        """

        # Skipping comments
        if line[0] == "/":
            return 0
        else:
            user = line.split("\t")

            # Skipping reserved value for new user
            if user[1][0] == "%":
                return 0

            if not self.find_user(user[1]):
                self.save_user(user[1], user[0], user[3], user[4], user[7])


    def find_user(self, user):
        """
        Method that searches user in local saved_users.txt file and returns true if it is find
        :rtype : Boolean
        """
        searchfile = open(self.accounts_text_file, "r")
        for line in searchfile:
            if user in line:
                searchfile.close()
                return True

        searchfile.close()
        return False

    def save_user(self, user, user_id, date_registrated, gender, email):
        """
        Method that handles saving new users data to textfile and database
        :param user:
        :param user_id:
        """

        if self.save_user_database(user, user_id, date_registrated, gender, email):
            self.save_user_text(user)
            self.replace_local_accounts_file()

    def save_user_database(self, user, user_id, date_registrated, gender, email):
        """
        Method that provides saving new users data to database
        :param user:
        :param user_id:
        :return:
        """
        account = {"user": user,
                   "id_user": user_id,
                   "gender": gender,
                   "email": email,
                   "date_registrated": date_registrated}
        try:
            mongo = MongoDB()
            mana_db = mongo.get_manaworld_database()
            acc_id = mana_db.ManaWorldDB.insert(account)
            return True
        except:
            return False


    def save_user_text(self, user):
        """
        Method that saves new user to text file so we could check users again using it
        :param user:
        """
        with open(self.accounts_text_file, "a") as myfile:
            myfile.write("\n" + user)

    def replace_local_accounts_file(self):
        """
        Method that copies original account file to local copy which we use to calculate hash
        """
        shutil.copyfile(self.accounts_new, self.accounts_saved)


if __name__ == '__main__':
    accounts = Accounts()
    if not accounts.check_hash():
        accounts.get_new_users()

    else:
        print "Nothing to do here..."