# Illumio_coding_assessment_2024
This is my solution for Illumio's coding assessment for SWE position (2024)

This solution is in Python 3

## Assumptions
* Log file
    * This should be a plain text file ending in .txt
    * each line should only contain only 1 full log -- no multiple logs in the same line
    * logs cannot be be broken up into multiple lines -- each log must be contained in 1 line 
    * No empty lines must be present
    * The program will skip over logs that do not have at least 8 items in it (including it will skip over empty lines)
* Look up table file
    * This should be a CSV file. The spec sent to me in the email has a contradiction -- in the beginning it says this file is a csv file and later it says it’s a plain text file. Given this contradiction, I decided to let this file be a CSV file because it made more sense to me
    * This should always contain a header with the column names. Otherwise, the output may be slightly incorrect.
    * This file should never be empty, at the very least it should contain the header (the column names)
    * The 1st column should always be the destination port and should always be an integer
    * The 2nd column should always be the protocol name as a string
    * The 3rd column should always be the tag, also as a string
* We are using the Protocal decimal to protocol key mapping as shown over here → https://www.iana.org/assignments/protocol-numbers/protocol-numbers.xhtml. If we ever encounter a Protocol decimal value not in the mapping in the link, we mark it as “unassigned”
* There is no limitation on what version the log has to be -- it can be any form of log where the destination port needs to be an integer in the 6th position and the protocol needs to be in the 7th position (using 0th indexing). This assumption is based on this → https://docs.aws.amazon.com/vpc/latest/userguide/flow-log-records.html#flow-logs-fields 
* The tags & protocol names in this program are not case-sensitive
When we encounter a destination port & protocol name combination that does not have a mapping in the lookup table, it will be marked as “untagged”

## How to Use the Program 
* The program is in main.py. To run the program you need to run main.py with exactly 4 additional arguments → 
Python3 main.py <arg1> <arg2> <arg3> <arg4>
    * Arg1 = the log file (.txt)
    * Arg2 =  the file that contains the look up table (.csv)
    * Arg3 = a destination file to output the count of matches for each tag (.csv)
    * Arg4 = a destination file to output the count of matches for each port/protocol combination (.csv)
* If any of the input arguments are incorrect, you will get an error and the program will quit.
* If the program ran successfully, it will print "Finished -- output files generated"
* The required output will be written to arg3 and arg4. You can check the results over there

## How the Program Works
* First we get the mapping in the form of a hashmap for protocol number to their names using the CSV in https://www.iana.org/assignments/protocol-numbers/protocol-numbers.xhtml. Let’s call this map1 
* Then we convert arg2, the lookup table fine, into a hashmap where the key, combination of destination port & protocol key, map to a tag. Let’s call this map2
* Then we read through the log file. For every log, we extract the destination port & protocol number. 
* From the protocol number, we get the log’s protocol key using map1
    *  If the protocol number does not have an associated key, we mark the protocol as “unassigned”
* Now, since we have both destination port & protocol key, we use that to get the corresponding tag using map2
    * If it does not have a corresponding tag from the lookup table fine, we label this as “untagged”
* As we look through the logs, we keep track of all the tags we have seen and how many of each. We store this in a map data structure, let’s call it map3
* As we look through the logs, we keep track of each destination port & protocol key combination  we have seen and how many of each we have seen. We store this in a map data structure, let’s call it map4
* We output map3 as a CSV with headers to arg3
* We output map4 as a CSV with headers to arg4

## Testing & Performance 
* I tested this with many test trivial test cases and it worked as expected
* Stress testing 
    * To stress test this, I created very large input files.
    * I created 2 input log files
        * Logs_stress_test_1.csv
            * This is 10MB
            * This contains around 95k logs
        * Logs_stress_test_2.csv
            * This is 10MB
            * 220k logs
            * I was able to fit a lot more logs into this by reducing the number of characters in each log
    * I created 1 input lookup table file that contains 10k mappings
    * I ran my program using the above stress test files as input and the program ran perfectly in 0.3s. The output files matched what was expected
* Edge case testing
    * I tested my program with empty log files and empty lookup files (the lookup file will still contain the header columns, so not 100% empty) and the output produced was correct
