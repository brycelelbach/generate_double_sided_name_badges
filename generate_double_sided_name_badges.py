#! /usr/bin/env python
# -*- coding: utf-8 -*-

###############################################################################
# Copyright (c) 2016 Bryce Adelstein Lelbach aka wash <brycelelbach@gmail.com>
#
# Distributed under the Boost Software License, Version 1.0. (See accompanying
# file LICENSE_1_0.txt or copy at http://www.boost.org/LICENSE_1_0.txt)
###############################################################################

from sys import exit

from optparse import OptionParser

from unicodecsv import writer as csv_writer
from unicodecsv import reader as csv_reader

output_keys = ["First Name", "Last Name", "Conversation Starter", "Attending"] 

op = OptionParser(usage="%prog [input-data] [output-data]")
args = op.parse_args()[1]

if len(args) != 1 and len(args) != 2:
    op.print_help()
    exit(1)

input_data = csv_reader(open(args[0], "r"), encoding="utf-8")

if len(args) == 1:
    output_data = csv_writer(stdout, encoding="utf-8")
else:
    output_data = csv_writer(open(args[1], "w"), encoding="utf-8")

# Maps column names to indices 
legend = {}
num_fields = None

attendees = []

try:
    # Read the header
    header_row = input_data.next()

    num_fields = len(header_row)

    for i in range(0, len(header_row)):
        legend[header_row[i]] = i 

    # Read the data    
    while True:
        row = input_data.next()

        if num_fields != len(row):
            print "ERROR: Record " + str(row) + " does not have " + \
                  str(num_fields) + " fields."
            exit(1)

        attendees.append(row)

except StopIteration:
    pass

# Sort the attendees alphabetically by first name
attendees = sorted(attendees)

# Pad attendees with blank entries to ensure its length is divisible by 10.
if 0 != (len(attendees) % 6):
    for i in range(0, 6 - (len(attendees) % 6)):
        attendees.append([""] * num_fields)

double_sided_attendees = []

# Add a new page after every 6 attendees which has the names of those attendees
# in the correct order for a double sided print. E.g.:
#
# A B    A B  B A
# C D -> C D  D C
# E F    E F  F E
for i in range(0, len(attendees) / 6):
    page = attendees[i * 6 : i * 6 + 6]

    double_page = [ \
        # Front side
        page[0], page[1],\
        page[2], page[3],\
        page[4], page[5],\
        # Back side
        page[1], page[0],\
        page[3], page[2],\
        page[5], page[4] \
    ]

    double_sided_attendees.extend(double_page)

# Output the attendee list. We add a new field - a unique identifier, the
# entry's index in the list - to keep Avery's software from ignoring the empty
# padding entries on the last page.

# Output the header.
output_data.writerow(["UID"] + output_keys)

# Output the attendees
for uid, attendee in enumerate(double_sided_attendees):
    output_data.writerow(
        [uid] + list(attendee[legend[key]] for key in output_keys)
    )

