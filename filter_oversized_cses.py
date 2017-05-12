#! /usr/bin/env python
# -*- coding: utf-8 -*-

###############################################################################
# Copyright (c) 2016 Bryce Adelstein Lelbach aka wash <brycelelbach@gmail.com>
#
# Distributed under the Boost Software License, Version 1.0. (See accompanying
# file LICENSE_1_0.txt or copy at http://www.boost.org/LICENSE_1_0.txt)
###############################################################################

from sys import exit, stdout

from optparse import OptionParser

from unicodecsv import writer as csv_writer
from unicodecsv import reader as csv_reader

target_key    = "Conversation Starter" 
target_length = 45

op = OptionParser(
    usage="%prog [input-data] [regular-output-data] [oversized-output-data]"
    )
args = op.parse_args()[1]

if len(args) != 3:
    op.print_help()
    exit(1)

input_data            = csv_reader(open(args[0], "r"), encoding="utf-8")
regular_output_data   = csv_writer(open(args[1], "w"), encoding="utf-8")
oversized_output_data = csv_writer(open(args[2], "w"), encoding="utf-8")

# Maps column names to indices 
header_row = []
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

# Output the header.
regular_output_data.writerow(header_row)
oversized_output_data.writerow(header_row)

# Sort the attendees alphabetically by first name
for attendee in sorted(attendees):
    if target_length >= len(attendee[legend[target_key]]):
        regular_output_data.writerow(attendee)
    else:
        oversized_output_data.writerow(attendee)


