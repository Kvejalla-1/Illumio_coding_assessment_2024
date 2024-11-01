
import sys
import csv
import os

# handles the input arguments
# prints and error message and exits if the program is not run correctly
# if run correctly, it returns break all the input file names and returns them\
#
# Return type
#	(string, string, string, string)
def handleArgs(arguments):
	if len(arguments) != 4:
		print("program takes 4 and exactly 4 inputs as command line arguments as input.")
		print("1st Input = the log file (.txt)")
		print("2nd Input = the look up table file (.csv).")
		print("3rd Input = a destination file to output the count of matches for each tag (.csv)")
		print("4th Input = a destination file to output the count of matches for each port/protocol combination (.csv)")
		print("example: python3 main.py logs.txt lookup.csv tag_counts.csv port_protocol_counts.csv")
		print("Please try again correclty.")
		sys.exit()
	if not arguments[0].endswith(".txt"):
		print("the 1st input argument must be the log file -- a .txt file")
		print("Please try again correclty.")
		sys.exit()
	if not arguments[1].endswith(".csv"):
		print("the 2nd input argument must be the lookup table file -- a .csv file")
		print("Please try again correclty.")
		sys.exit()
	if not arguments[2].endswith(".csv"):
		print("the 3rd input argument must be an output file to write the count of matches for each tag -- a .csv file")
		print("Please try again correclty.")
		sys.exit()
	if not arguments[3].endswith(".csv"):
		print("the 4th input argument must be an output file to write the count of port/protocol combinations for each tag -- a .csv file")
		print("Please try again correclty.")
		sys.exit()
	logs_file = arguments[0]
	lookup_file = arguments[1]
	tag_counts_output_file = arguments[2]
	port_protocol_counts_output_file = arguments[3]
	return logs_file, lookup_file, tag_counts_output_file, port_protocol_counts_output_file


# a CSV file containg mappings of protocol numbers to their names exists in a file called protocol-numbers.csv
# we simply parse that file and create a hashmap of this mapping
# 
# Return type
#	hashmap[int] = string
def getProtocolMappings():
	# key = protocol number -- int (ex : 6)
	# value = protocol type -- string (ex : tcp)
	protocols = {} 
	# PROTOCOL-NUMBERS.csv file contains the mapping of protocol numbers to their respective names
	# the CSV file is from https://www.iana.org/assignments/protocol-numbers/protocol-numbers.xhtml
	with open("PROTOCOL-NUMBERS.csv", 'r') as file:
		reader = csv.reader(file)
		next(reader)  # Skip header row
		for row in reader:
			if row[0] != "147-252":
				protocol_num = int(row[0])
				protocol_str = row[1].lower()
				if protocol_str.strip() == "":
					protocol_str = "unassigned"
				protocols[protocol_num] = protocol_str
	for i in range(147, 252+1, 1):
		protocols[i] = "unassigned"
	return protocols

# The 2nd command-line argument should be a csv file containg a mapping for destination protocol pairs to their tags
# we simply parse that file and create a hashmap of this mapping
# 
# Input type
#		filename = string
# Return type
#	hashmap[(int, string)] = string
def getTagsMap(filename):
	# key = (destination port, protocol type) -- (int, string) (ex : (25, tcp) )
	# value = protocol type -- string (ex : sv_p2)
	tags = {}
	with open(filename, 'r') as file:
		reader = csv.reader(file)
		next(reader)  # Skip header row
		for row in reader:
			if len(row) >= 2:
				dstport = int(row[0])
				protocol = row[1].lower()
				tag = row[2].lower()
				tags[ (dstport, protocol) ] = tag
	return tags



def main():
	# get the files from command line arguments
	logs_file, lookup_file, tag_counts_output_file, port_protocol_counts_output_file = handleArgs(sys.argv[1:])

	# get mapping of protocol numbers to protocol names from https://www.iana.org/assignments/protocol-numbers/protocol-numbers.xhtml
	protocol_map = getProtocolMappings()
	# get python hashmap represenation of the lookup table in lookup_file (2nd input argument csv file)
	tags_map = getTagsMap(lookup_file)

	tag_count = {} # map to keep track of how many of each tag we saw while parsing log file
	port_protocol_count = {} # map to keep track of how many of each (port, protocol) pairs we saw while parsing log file
	# parse all the logs from the input log file
	with open(logs_file, 'r') as file:
	    for line in file:
	        cur_log = line.strip().split(" ")
	        if len(cur_log) < 8: # must have at least 8 elements because protocol_num will be at 8th position (using 1st-indexing)
	        	continue # skip the line
	        dstport = int(cur_log[6]) # the destination port will be at the 6th index in the log
	        protocol_num = int(cur_log[7]) # the protocol number will be at the 7th index in the log
	        # get the protocol name from the protocol number
	        if protocol_num in protocol_map:
	        	protocol_str = protocol_map[protocol_num]
	        else:
	        	protocol_str = "unassigned"
	        # get the tag using the destination port and protocol name
	        if (dstport, protocol_str) in tags_map:
	        	cur_tag = tags_map[ (dstport, protocol_str) ]
	        else:
	        	cur_tag = "untagged"
	        # update the tag count
	        if cur_tag not in tag_count:
	        	tag_count[cur_tag] = 0
	        tag_count[cur_tag] += 1
	        # update the port protocol combination count
	        if (dstport, protocol_str) not in port_protocol_count:
	        	port_protocol_count[ (dstport, protocol_str) ] = 0
	        port_protocol_count[ (dstport, protocol_str) ] += 1

	# write the tag counts to the output file
	with open(tag_counts_output_file, 'w') as f:  
		writer = csv.writer(f)
		writer.writerow(["Tag", "Count"])
		for tag, count in tag_count.items():
			writer.writerow([tag, count])

	# write the destination port & protocol combination counts to the output file
	with open(port_protocol_counts_output_file, 'w') as f:  
		writer = csv.writer(f)
		writer.writerow(["Port", "Protocol", "Count"])
		for key, count in port_protocol_count.items():
			port = key[0]
			protocol = key[1]
			writer.writerow([port, protocol, count])

	print("Finished -- output files generated")

# Driver code
if __name__ == "__main__":
	print("\n")
	main()
	print("\n")
	





#======================================================================================================================================================================================
#======================================================================================================================================================================================
#======================================================================================================================================================================================
#======================================================================================================================================================================================
#======================================================================================================================================================================================
#======================================================================================================================================================================================
#======================================================================================================================================================================================

# SCRATCH -- PLEASE IGNORE
# I was going to delete this but i thought it would be helpful because this is where i generated my stress tests
'''
    CODE TO GENERATE STRESS TESTS 
    # upto 10000 mappings
	lookup_stress_test_file = "lookup_sample_files/lookup_stress_test.csv"
	with open(lookup_stress_test_file, 'w') as f:  
		writer = csv.writer(f)
		writer.writerow(["dstport", "protocol", "tag"]) # write the header
		for i in range(0, 10000, 1):
			writer.writerow([i, "tcp", "tag" + str(i)])

	# log file can be upto 10 MB 
	logs_stress_test_file = "logs_sample_files/logs_stress_test_2.txt"
	with open(logs_stress_test_file, 'w') as f:
		count = 0
		while os.path.getsize(logs_stress_test_file) < 10000000:
			#log = "2 123456789012 eni-5e6f7g8h 192.168.1.101 198.51.100.3 25 " + str(count) +  " 6 10 8000 1620140761 1620140821 ACCEPT OK"
			log = "2 1 en 1.1.1.1 1.1.1.3 1 " + str(count) +  " 6 1 8 2 6 A K"
			f.write(log)
			f.write("\n")
			count += 1
'''


# output files should be .CSV files
# python3 main.py logs_sample_files/logs_1.txt lookup_sample_files/lookup_1.csv tag_counts.csv port_protocol_counts.csv

# STRESS TESTING
# python3 main.py logs_sample_files/logs_stress_test_2.txt lookup_sample_files/lookup_stress_test.csv tag_counts.csv port_protocol_counts.csv 
# python3 main.py logs_sample_files/logs_stress_test_1.txt lookup_sample_files/lookup_stress_test.csv tag_counts.csv port_protocol_counts.csv    

# EDGE CASE TESTING
# python3 main.py logs_sample_files/logs_empty.txt lookup_sample_files/lookup_stress_test.csv tag_counts.csv port_protocol_counts.csv  
# python3 main.py logs_sample_files/logs_stress_test_2.txt lookup_sample_files/lookup_empty.csv tag_counts.csv port_protocol_counts.csv 
# python3 main.py logs_sample_files/logs_empty.txt lookup_sample_files/lookup_empty.csv tag_counts.csv port_protocol_counts.csv  


'''

	for key in tag_count:
		print(key, end=" : ")
		print(tag_count[key])

	print("")

	for key in port_protocol_count:
		print(key, end=" : ")
		print(port_protocol_count[key])
'''


