#!/usr/bin/python

import sys

fw_dmesg_file = sys.argv[1]
data_msc_file = sys.argv[2]

dmesg_file = open(fw_dmesg_file, "r+")
msc_file = open(data_msc_file, "r+")

while True:
	dmesg_line = dmesg_file.readline()
	if (dmesg_line == ""):
		break

	dmesg_word_list = dmesg_line.split()

	found_message_id = 0
	for position, message_id in enumerate(dmesg_word_list):
		if (message_id == "message_id"):
			found_message_id = 1
			break

	if not found_message_id:
		print "Not a FW message"
		continue

	message_id = dmesg_word_list[position + 1]
	parsed_line = dmesg_line[:dmesg_line.find("message_id")]

	message_id_not_found = 0
	msc_file.seek(0, 0)
	while True:
		msc_line = msc_file.readline()
		msc_word_list = msc_line.split(",")
		if (message_id == msc_word_list[0]):
			break
		if (msc_line == ""):
			message_id_not_found = 1
			break
	
	if message_id_not_found:
		message_id_not_found = 0
		continue

	arg_count = len(msc_word_list[1])

	msc_line = ",".join(msc_line.split(',')[2:])
	parsed_line += msc_line
	parsed_line = parsed_line.rstrip() 

	arg_start = dmesg_line.find('(')
	arg_end = dmesg_line.find(')')
	arg_line = dmesg_line[arg_start + 2 : arg_end - 1]

	parsed_line = parsed_line + " (" + arg_line + ")"

	print parsed_line

	if (arg_line == ""):
		continue

msc_file.close()
dmesg_file.close()
