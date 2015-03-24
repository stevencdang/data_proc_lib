#!/usr/bin/python

import os

DATADIR = '/tmp/conceptmapping/data'
DATA_FILE = "/tmp/conceptmapping/cm_data.csv"
# DATA_FILE = "/tmp/conceptmapping/all_cm_data.csv"
ELM_DELIMITER = "<A5T$>"
LINE_DELIMITER = "<A5T^>"
DOC1_FILE = "cm_doc1.txt"
DOC2_FILE = "cm_doc2.txt"
PROTO1_FILE = "cm_proto1.txt"
PROTO2_FILE = "cm_proto2.txt"
OUTFILE = "cm_data.csv"
PARTICIPANTFILE = "cm_participant_info.csv"
UNFINISHEDPARTFILE = "cm_unfinished_info.csv"
ALTUSESFILE = "cm_combined_alt_uses.txt"
ALL_FILES = [DATA_FILE, DOC1_FILE, DOC2_FILE, PROTO1_FILE, PROTO2_FILE]
TIME = {'alt_use': 3, 'doc1': 8, 'doc2': 15,
        'proto1': 8, 'proto2': 20}


class Participant:

    ELM_DELIMITER = "<A5T$>"
    LINE_DELIMITER = "<A5T^>"
    CSV_DELIMITER = "`"

    pid = 0
    first_name = None
    last_name = None
    email = None
    condition = 0
    alt_use = ""
    doc1 = ""
    doc2 = ""
    proto1 = ""
    proto2 = ""
    alt_use_time = 0
    doc1_time = 0
    doc2_time = 0
    proto1_time = 0
    proto2_time = 0
    cd_training_time = 0
    tool_training_time = 0
    proto_training_time = 0

    def __str__(self):
        return str(self.pid) + Participant.CSV_DELIMITER + \
            self.last_name + Participant.CSV_DELIMITER + \
            self.first_name + Participant.CSV_DELIMITER + \
            self.email + Participant.CSV_DELIMITER + \
            str(self.condition) + Participant.CSV_DELIMITER + \
            self.doc1 + Participant.CSV_DELIMITER + \
            self.doc2 + Participant.CSV_DELIMITER + \
            self.proto1 + Participant.CSV_DELIMITER + \
            self.proto2

    def info(self):
        return str(self.pid) + Participant.CSV_DELIMITER + \
            self.last_name + Participant.CSV_DELIMITER + \
            self.first_name + Participant.CSV_DELIMITER + \
            self.email

    @staticmethod
    def info_header():
        return "PID" + Participant.CSV_DELIMITER + \
            "last name" + Participant.CSV_DELIMITER + \
            "first name" + Participant.CSV_DELIMITER + \
            "email"

    def unfinished_info(self):
        return str(self.pid) + Participant.CSV_DELIMITER + \
            self.percent_complete() + Participant.CSV_DELIMITER + \
            self.last_name + Participant.CSV_DELIMITER + \
            self.first_name + Participant.CSV_DELIMITER + \
            self.email + Participant.CSV_DELIMITER + \
            self.debug() + Participant.CSV_DELIMITER + \
            self.time()

    @staticmethod
    def unfinished_header():
        return "pid" + Participant.CSV_DELIMITER + \
            "progress" + Participant.CSV_DELIMITER + \
            "last name" + Participant.CSV_DELIMITER + \
            "first name" + Participant.CSV_DELIMITER + \
            "email" + Participant.CSV_DELIMITER + \
            Participant.debug_header() + \
            Participant.time_header()

    def time(self):
        return str(self.alt_use_time) + Participant.CSV_DELIMITER + \
            str(self.cd_training_time) + Participant.CSV_DELIMITER + \
            str(self.tool_training_time) + Participant.CSV_DELIMITER + \
            str(self.doc1_time) + Participant.CSV_DELIMITER + \
            str(self.doc2_time) + Participant.CSV_DELIMITER + \
            str(self.proto_training_time) + Participant.CSV_DELIMITER + \
            str(self.proto1_time) + Participant.CSV_DELIMITER + \
            str(self.proto2_time)

    @staticmethod
    def time_header():
        return "Alt use time" + Participant.CSV_DELIMITER + \
            "CD training" + Participant.CSV_DELIMITER + \
            "tool training" + Participant.CSV_DELIMITER + \
            "doc1" + Participant.CSV_DELIMITER + \
            "doc2" + Participant.CSV_DELIMITER + \
            "proto training" + Participant.CSV_DELIMITER + \
            "proto1" + Participant.CSV_DELIMITER + \
            "proto2"

    def data(self):
        return str(self.pid) + Participant.CSV_DELIMITER + \
            str(self.condition) + Participant.CSV_DELIMITER + \
            self.print_alt_uses(';') + Participant.CSV_DELIMITER + \
            self.doc1 + Participant.CSV_DELIMITER + \
            self.doc2 + Participant.CSV_DELIMITER + \
            self.proto1 + Participant.CSV_DELIMITER + \
            self.proto2 + Participant.CSV_DELIMITER + \
            self.time()

    @staticmethod
    def data_header():
        return "PID" + Participant.CSV_DELIMITER + \
            "condition" + Participant.CSV_DELIMITER + \
            "Alt uses" + Participant.CSV_DELIMITER + \
            "doc1" + Participant.CSV_DELIMITER + \
            "doc2" + Participant.CSV_DELIMITER + \
            "proto1" + Participant.CSV_DELIMITER + \
            "proto2" + Participant.CSV_DELIMITER + \
            Participant.time_header()

    def debug(self):
        dbg_doc1 = True if self.doc1 == '' else False
        dbg_doc2 = True if self.doc2 == '' else False
        doc1_eq_doc2 = True if self.doc1 == self.doc2 else False
        proto1_eq_proto2 = True if self.proto1 == self.proto2 else False
        return str(dbg_doc1) + Participant.CSV_DELIMITER + \
            str(dbg_doc2) + Participant.CSV_DELIMITER + \
            str(doc1_eq_doc2) + Participant.CSV_DELIMITER + \
            str(proto1_eq_proto2) + Participant.CSV_DELIMITER

    @staticmethod
    def debug_header():
        return "doc1 empty" + Participant.CSV_DELIMITER + \
            "doc2 empty" + Participant.CSV_DELIMITER + \
            "doc1 = doc2" + Participant.CSV_DELIMITER + \
            "proto1 = proto2"

    def print_alt_uses(self, delimiter):
        out = ""
        for use in self.alt_use:
            out += use + delimiter
        return out

    def is_valid(self):
        if self.alt_use_time > 0 and \
           self.doc1_time > 0 and \
           self.doc2_time > 0 and \
           self.proto1_time > 0 and \
           self.proto2_time > 0 and \
           self.alt_use != '' and \
           self.doc1 != '' and \
           self.doc2 != '' and \
           self.proto1 != '' and \
           self.proto2 != '' and \
           self.doc1 != self.doc2 and \
           self.proto1 != self.proto2:
            return True
        else:
            return False

    def percent_complete(self):
        total = 0
        # times = ['alt_use', 'doc1', 'doc2', 'proto1', 'proto2']
        # all_fields = self.__dict__
        # for time in times:
            # if all_fields[time] > 0:
                # total += TIME[time]
        if self.alt_use_time > 0:
            total += TIME['alt_use']
        if self.doc1_time > 0:
            total += TIME['doc1']
        if self.doc2_time > 0:
            total += TIME['doc2']
        if self.proto1_time > 0:
            total += TIME['proto1']
        if self.proto2_time > 0:
            total += TIME['proto2']
        if total == 54:
            return '100%'
        else:
            percent = (total * 100) / 60
            return str(percent) + '%'

    @staticmethod
    def parse_alt_use(raw_uses):
        uses = raw_uses.split('\n')
        # remove empty element after last new line
        return uses[:-1]

    @staticmethod
    def parse_part_data(part_data):
        """
        Takes a data string with all data for 1 participant
        and parses it

        """
        def num_to_str(num, func):
            try:
                result = func(num)
                return result
            except ValueError:
                return 0
        data = part_data.split(Participant.ELM_DELIMITER)
        prt = Participant()
        prt.pid = num_to_str(data[0], int)
        prt.email = data[1]
        prt.first_name = data[2]
        prt.last_name = data[3]
        prt.condition = num_to_str(data[4], int)
        prt.alt_use = Participant.parse_alt_use(data[5])
        prt.alt_use_time = num_to_str(data[6], float)
        prt.doc1 = data[7]
        prt.doc1_time = num_to_str(data[8], float)
        prt.doc2 = data[9]
        prt.doc2_time = num_to_str(data[10], float)
        prt.proto1 = data[11]
        prt.proto1_time = num_to_str(data[12], float)
        prt.proto2 = data[13]
        prt.proto2_time = num_to_str(data[14], float)
        # prt.cd_training_time = float(data[15])
        prt.tool_training_time = num_to_str(data[16], float)
        prt.proto_training_time = num_to_str(data[17], float)
        return prt

    @staticmethod
    def parse_data(file_name):
        f = open(file_name, 'r')
        data = f.read()
        f.close()
        rows = data.split(LINE_DELIMITER)
        for row in rows[:-1]:
            yield row


def write_to_file(participants):
    # Output to combined CSV
    dirname = DATADIR
    if not os.path.exists(DATADIR):
        os.mkdir(DATADIR)

    # Output participant info
    newfile = os.path.join(dirname, PARTICIPANTFILE)
    f = open(newfile, 'w')
    f.write(Participant.info_header() + '\n')
    for pid, participant in participants.items():
        if participant.is_valid():
            f.write(participant.info() + '\n')
    f.close()

    # Output list of unfinished and invalid participants
    newfile = os.path.join(dirname, UNFINISHEDPARTFILE)
    f = open(newfile, 'w')
    f.write(Participant.unfinished_header() + '\n')
    for pid, participant in participants.items():
        if not participant.is_valid():
            f.write(participant.unfinished_info() + '\n')
    f.close()

    # Output anonymous info
    newfile = os.path.join(dirname, OUTFILE)
    f = open(newfile, 'w')
    f.write(Participant.data_header() + '\n')
    for pid, participant in participants.items():
        if participant.is_valid():
            # print "Saved Participant with id: " + str(pid)
            f.write(participant.data() + '\n')
    f.close()

    # Output combined list of all alt uses
    newfile = os.path.join(dirname, ALTUSESFILE)
    f = open(newfile, 'w')
    for pid, participant in participants.items():
        f.write(participant.print_alt_uses('\n') + '\n')
    f.close()

    # Output doc2, proto1, proto2 to separate files
    for pid, participant in participants.items():
        if participant.is_valid():

            # create folder with pid
            dirname = os.path.join(DATADIR, "%03d" % pid)
            if not os.path.exists(dirname):
                os.mkdir(dirname)

            # Write Alternative Uses
            altusefile = os.path.join(dirname, 'altuse.html')
            f = open(altusefile, 'w')
            f.write(participant.print_alt_uses('</br>'))
            f.close()

            # Write doc2
            doc2file = os.path.join(dirname, 'doc2.html')
            f = open(doc2file, 'w')
            f.write(participant.doc2)
            f.close()

            # Write proto1
            newfile = os.path.join(dirname, 'proto1.xml')
            f = open(newfile, 'w')
            f.write(participant.proto1)
            f.close()

            # Write proto2
            newfile = os.path.join(dirname, 'proto2.xml')
            f = open(newfile, 'w')
            f.write(participant.proto2)
            f.close()


if __name__ == "__main__":
    #initialize list of participants
    participants = {}
    part_data = Participant.parse_data(DATA_FILE)
    for part in part_data:
        new_part = Participant.parse_part_data(part)
        participants[new_part.pid] = new_part
    write_to_file(participants)
