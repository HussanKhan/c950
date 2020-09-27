# just sotring values in an array
# and retrieving those values by using 
# index position

import random

# A classic hash table, one key leads to one
# value, if collison, tables resizes
class HashTable():

    def __init__(self, initLength):
        self.table = [None] * initLength
        self.testDict = {}

    # returns hash and new index position
    # O(1)
    def hash(self, key):
        hashed = abs(hash(key))
        index = abs(hash(key)) % len(self.table)
        return hashed, index

    # doubles table size
    # O(N), were N is size of new table
    def expandTable(self):

        oldTable = self.table
        
        # double the table size
        self.table = [None]* (len(self.table)*2)
        newSize = len(self.table)
        
        for value in oldTable:
            
            if value is not None:

                lastHash = value[1]
                newIndex = lastHash % newSize
                self.table[newIndex] = value

    # O(1) if space in table, else O(N) if table is resized
    def insert(self, key, value, resized=0):
        
        hashed, index = self.hash(key)
        
        if self.table[index] is None:
            self.table[index] = (value, hashed)
            self.testDict[key] = value
        else:
            # first resize table then raise error if issue still present
            if resized < 10:
                self.expandTable()
                self.insert(key, value, resized=resized+1)
            else:
                raise ValueError('Key already in hash table. Use update instead to change value {}'.format(self.get(key)))
    
    # update entry in hash table
    # O(1)
    def update(self, key, value):

        hashed, index = self.hash(key)

        if self.table[index] is not None:
            self.table[index] = (value, hashed)
            self.testDict[key] = value
        else:
            raise ValueError('Key value pair does not exist in hash table')
    
    def get(self, key):
        hashed, index = self.hash(key)
        
        if self.table[index] is not None:
            return self.table[index][0]
        else:
            raise ValueError('No entry for that key')

# hashMap = HashTable(100)

# alpha = ['1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 
# 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 
# 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y','z'] + ['1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 
# 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 
# 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y','z']

# for i in range(0, 5000):
#     WordOne = ""
#     WordTwo = ""

#     for i in range(0, random.randint(10, 50)):
#         WordOne += alpha[random.randint(0, len(alpha)-1)]
        
    
#     for i in range(0, random.randint(10, 50)):
#         WordTwo += alpha[random.randint(0, len(alpha)-1)]

#     try:
#         hashMap.insert(WordOne, WordTwo)
#         print("passed")
#     except Exception as e:
#         print(e)

# # check
# for k, v in hashMap.testDict.items():
#     if hashMap.get(k) == v:
#         print("pass")
#     else:
#         print(k, v, hashMap.get(k))
#         print("fail")
#         exit()
      

# # hashMap.insert('Tao', 'The Way')
# # hashMap.insert('Pooh', 'Tao')

# # print(hashMap.table)
# print(len(hashMap.table))


