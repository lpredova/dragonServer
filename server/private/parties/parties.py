from macpath import split

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
 check if there is user written in saved_party.txt
 if user is not there it is new user and we need to save it into database
 when user is saved to database simply add its name into saved_users.txt
 copy latest saved file into directory
'''


class Party:
    # path for parties file from game server
    party_new = "party.txt"

    # file path for local files with parties
    party_text_file = "saved_parties.txt"
    party_saved = "party.txt"

    def __init__(self):
        """
        Constructor in which we set default paths for local athena.txt and char.txt and servers char txt file

        """
        self.party_text_file = os.path.join(os.getcwd(), self.party_text_file)
        self.party_saved = os.path.join(os.getcwd(), self.party_saved)


        # todo path for accounts from server
        self.party_new = os.path.join("/Users/lovro/coding/Python/MWlogScrapper/test_data", self.party_new)


    def check_hash(self):

        """
        Method that calls hash comparison of two files to determine if there is changes
        :rtype : Boolean
        """
        if self.check_file_exists(self.party_new) and self.check_file_exists(self.party_saved):
            hash_ = Hash()
            if not hash_.check_file_hash(self.party_new, self.party_saved):
                return False
            else:
                return True
        else:
            print "Sorry specified file doesn't exist"


    def get_parties_from_server(self):
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
        f = open(self.party_new, 'r')
        for line in f:
            self.parse_party(line)

    def parse_party(self, line):
        """
        Method that parses accounts.txt file and if it's new user then we save it to database and append to saved_users.txt
        :rtype : object
        """

        party = line.split("\t")

        if not self.find_party(party):
            self.save_party(party)


    def find_party(self, party):
        """
        Method that searches user in local saved_party.txt file and returns true if it is find
        :rtype : Boolean
        """
        searchfile = open(self.party_text_file, "r")
        for line in searchfile:
            # print "trazim " + party[1] + self.write_party_members(party) + " u " + line
            if party[1] + self.write_party_members(party) in line:
                # He found the party, now we need to get members names
                searchfile.close()
                return True

        searchfile.close()
        return False

    def save_party(self, party):
        """
        Method that handles saving new parties data to textfile and database
        :param user:
        :param user_id:
        """
        if self.save_party_database(party):
            self.save_party_text(party)
            self.replace_local_parties_file()

    def parse_user_id(self, user_id):
        """
        Method that takes fuzzed user_id returns clean user id
        :param user_id:
        :return:
        """
        return user_id.split(",")[0]

    def save_party_database(self, party):
        """
        Method that provides saving new users data to database
        :param user:
        :param user_id:
        :return:
        """

        admins = self.get_party_admins(party)
        charachers = self.get_party_members(party)

        for char in charachers:

            admin = 0

            for element in admins:
                if element == char:
                    admin = 1

            party_user = {
                "char": char,
                "party_name": party[1],
                "admin": admin}

            try:
                mongo = MongoDB()
                db = mongo.get_manaworld_database()

                db.ManaWorldDB.update(
                    {"charachters.char_name": char},
                    {"$push": {"charachters.$.parties": party_user}},
                )

            except Exception:
                print Exception
                return False

        return True


    def save_party_text(self, party):
        """
        Method that checks if party exists and if exists then replaces members with new ones
        :param party:
        """
        with open(self.party_text_file, "wb") as searchfile:
            if os.stat(self.party_text_file).st_size == 0:
                searchfile.write(party[1] + self.write_party_members(party) + "\n")
                searchfile.close()
                return False

            for line in searchfile:
                if party[1] in line:
                    searchfile.write(line.replace(line, party[1] + self.write_party_members(party) + "\n"))
                    print "replacing current" + line + "with " + party[1] + self.write_party_members(party) + "\n"
                    searchfile.close()
                    return True

                else:
                    searchfile.write(party[1] + self.write_party_members(party) + "\n")
                    print "writing new one" + party[1] + self.write_party_members(party) + "\n"
                    searchfile.close()
                    return False

    def replace_local_parties_file(self):
        """
        Method that copies original account file to local copy which we use to calculate hash
        """
        shutil.copyfile(self.party_new, self.party_saved)

    def write_party_members(self, party):
        party_members = self.get_party_members(party)
        result = "\t"
        for p in party_members:
            result += p + ","
        return result

    def get_party_members(self, party):
        """
        Method that parses party so we could get only members
        :param party:
        :return:
        """
        return party[3:][1::2]

    def get_party_admins(self, party):
        admin = []
        party = party[3:]
        associative_party = [i + j for i, j in zip(party[::2], party[1::2])]

        for element in associative_party:
            element = element.split(",")
            if element[1][0] == "1":
                admin_name = element[1][1:]
                admin.append(admin_name)
        return admin


if __name__ == '__main__':
    party = Party()
    if not party.check_hash():
        party.get_new_users()

    else:
        print "Nothing to do here..."
