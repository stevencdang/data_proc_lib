#!/usr/bin/env python

# Author: Steven Dang stevencdang.com

# Requires pymongo
from sets import Set
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError
from os import mkdir, listdir, path
import file_manager
import mongo_settings


def get_db(db=None):
  """
  Returns a handle to an open connection to the mongo db

  """
  if db is None:
      db = ideagenstest
  return get_mongodb(db['url'],
                     db['port'],
                     db['dbName'],
                     db['user'],
                     db['pswd'])


def get_uniq_part(db):
  parts = db.participants.find()
  users = Set()
  # Get set of unique usernames in list of participants
  for part in parts:
    if (part.has_key('user')):
      user = part['user']
      if user != '':
        users.add(user['name'])
  # Perform operations on each username
  # print len(users)
  # for user in users:
      # print user
  return users

def add_excl_parts(db, usernames):
  """
  Add a list of excluded participants based on a set of usernames.
  Can't base on user_id because there are duplicate user_id's with
  the same user name

  """
  desc = "Replicating the effect " + \
          "of priming with common vs rare ideas in individual " + \
          "brainstorming with revised interface"
  exp_id= 'tN33ATDiCukWfj5G7'
  # exps = db.experiments.find()
  exp = db.experiments.find_one({'_id': exp_id})

  db.experiments.update({'_id': exp_id},
      {'$set': {'excludeUsers': list(usernames), 'description': desc}})
  # exp['excludeUsers'] = list(usernames)
  exp = db.experiments.find_one({'_id': exp_id})
  print exp['excludeUsers']
  print exp['description']



def get_mongodb(dbUrl, dbPort, dbName, dbUser=None, dbPswd=None):
  """
  takes db parameters and returns a connected db object usign those
  parameters

  """
  if ((dbUser == None) and (dbPswd == None)):
    dbURI = "mongodb://" + dbUrl + ":" + \
        str(dbPort) + "/" + dbName
  elif ((dbUser == "") and (dbPswd == "")):
    dbURI = "mongodb://" + dbUrl + ":" + \
        str(dbPort) + "/" + dbName
  else:
    dbURI = "mongodb://" + dbUser + ":" + dbPswd + "@" + dbUrl + ":" + \
        str(dbPort) + "/" + dbName
  client = MongoClient(dbURI)
  return client[dbName]


# collections to ignore
default_collections = [
    'system.indexes',
    'system.users',
]


class Data_Utility:
    """
    Utility functions for mass database operations

    """
    def __init__(self, data_path='data', db_params=ideagens):
        """
        Constructor that sets the data root directory of the utility
        and the parameters of the database to operate on

        """
        my_path = path.abspath(data_path)
        self.path = my_path

        self.db_params = db_params
        self.db = get_db(self.db_params)

    def dump_db(self, data_dir=None):
        # Ensure data dump directory exists
        if data_dir is None:
            data_dir = self.path
        if not path.exists(data_dir):
            mkdir(data_dir, 0774)

        # set up the connnection
        allCollections = [col for col in self.db.collection_names() if col not in default_collections]
        print "list of collections: "
        for col in allCollections:
            print "collection name: " + col
            docs = self.db[col].find()
            data = [doc for doc in docs]
            file_manager.write_json_to_file(data, data_dir, col)

    def restore_db(self):
        files = listdir(self.path)
        # col_names = [file.split('.json')[0] for file in files]
        existing_cols = self.db.collection_names()
        for file_name in files:
            file_path = path.join(self.dir_name, file_name)
            col = file_name.split('.json')[0]
            print "writing to data to collection " + col + \
                " in db: " + self.db_params['dbName']
            if col != 'users':
                data = self.decode_json_file(file_path)
                if col not in existing_cols:
                    print "creating collection: " + col
                    self.db.create_collection(col)
                else:
                    print "inserting into existing collection"
                try:
                    if data:
                        self.db[col].insert(data, continue_on_error=True)
                except DuplicateKeyError:
                    print "Attempted insert of document with duplicate key"
                else:
                    print "success"
            else:
                print "not writing users to db"

    def clear_db(self):
        cols = self.db.collection_names()
        clear_cols = [col for col in cols if col not in default_collections]
        for col in clear_cols:
            # Remove all docs from collection
            self.db[col].remove()

    def get_data(self, collection, fields=None, filters=None):
        """
        Get a list of documents from the db collection for specified
        fields only. fields is list of field names for each document.

        """
        data = self.db[collection].find(filters)
        if fields is None:
            return data
        else:
            filtered_data = []
            for doc in data:
                rowDict = {}
                for field in fields:
                    rowDict[field] = doc[unicode(field)]
                filtered_data.append(rowDict)
            return filtered_data

    def join_data(self, base_data, join_data, base_field, join_fields):
        """
        Perform a similar operation to a sql join for 2 sets of data.
        
        @Params
        base_data - list of fields to extend with joined data
        join_data - dictionary of data, indexed by base_field value
        base_field - value to use as key in lookup in join_data 
            dictionary
        join_fields - list of field data to replace the base_field id

        @Return
        The modified base_data list of data

        """
        for data in base_data:
          extra = join_data[data[base_field]]
          for field in join_fields:
            data[field] = extra[field]
        
        return base_data
  
    def get_ideas(self):
        """
        Get a list of all the ideas

        """
        fields = ['content', 'clusterIDs', 'isGamechanger',
                  'userID', 'promptID']
        return self.get_data("ideas", fields)

    def get_clusters(self):
        """
        Get a list of all the ideas

        """
        fields = ['name', ]
        return self.get_data("clusters", fields)

    def get_users(self):
        """
        Get a list of all the ideas

        """
        fields = ['name', ]
        return self.get_data("myUsers", fields)


if __name__ == '__main__':
    # db = get_db(chi1)
    util = Data_Utility('data/facPilot', ideagens)
    util.dump_db()
