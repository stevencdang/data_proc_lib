#!/usr/bin/env python

# Author: Steven Dang stevencdang.com

import mongohq
from sets import Set
import logging


logging.basicConfig(format='%(levelname)s:%(message)s',
                    level=logging.DEBUG)


class Db_Manager:
    """
    A class for performing typical data processing operations on
    the ideagens database

    """
    def __init__(self, db_params=mongohq.ideagens):
        """
        Constructor to instantiate references to Ideagens instance
        and its corresponding database

        """
        self.db_params = db_params
        self.db = mongohq.get_db(db_params)

    def set_db(self, db_params=mongohq.ideagenstest):
        """
        Set the db where ideagens data sits

        """
        self.db = mongohq.get_db(db_params)

    def get_prompts(self):
        logging.debug("Get all prompts")
        return self.db['prompts'].find()

    def get_users_in_prompt(self, prompt):
        logging.debug("Get users in prompt")
        ids = prompt['groupIDs']
        groupIDs = Set(ids)
        logging.debug("Found " + str(len(groupIDs)) + " groups with this prompt")
        # Getting all users for the prompt ignoring duplicates across groups
        user_ids = Set([])
        users = []
        for groupID in groupIDs:
            group = self.db['groups'].find({'_id': groupID})[0]
            for user in group['users']:
                if (user['_id'] not in user_ids):
                    user_ids.add(user['_id'])
                    users.append(user)

        logging.info("got " + str(len(users)) + " users in this prompt")
        return users

    def get_ideas_for_user(self, user, prompt):
        logging.debug("Get ideas for user in prompt")
        return self.db['ideas'].find({'userID': user['_id'],
                                     'promptID': prompt['_id']
                                     })

    def get_login_times(self, users):
        logging.debug("Getting login times for users")
        events = []
        for user in users:
            login_events = self.db['events'].find({
                'userID': user['_id'],
                'description': "User logged into experiment"
            })
            logging.debug("looking at user " + user['name'])
            logging.debug(login_events.count())
            events.extend(login_events)
        return events




if __name__ == '__main__':
    # clear_db(mongohq.ideagenstest)
    # dump_db('data/chi1', mongohq.chi1)
    # restore_db('data/chi3_raw', mongohq.ideagenstest)
    db = Db_Manager(mongohq.ideagens)
