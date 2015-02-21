__author__ = 'lovro'

import hashlib


class HashChecker:
    BLOCKSIZE = 65536
    hasher = ""

    def __init__(self):
        pass

    def check_file_hash(self, file_first, file_second):

        """
        Method that handles input from methods, two paths of files and compares them
        :rtype : Boolean
        """
        if self.calculate_hash(file_first) == self.calculate_hash(file_second):
            return True
        else:
            return False


    def calculate_hash(self, hashing_file):
        """
        Method that returns hash of the input file
        :rtype : hash of the file
        """
        self.hasher = hashlib.md5()

        with open(hashing_file, 'rb') as afile:
            buf = afile.read(self.BLOCKSIZE)
            while len(buf) > 0:
                self.hasher.update(buf)
                buf = afile.read(self.BLOCKSIZE)

        return self.hasher.hexdigest()