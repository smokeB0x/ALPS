#!/usr/bin/env python

# A script for parcing the file newbatterystats from android smartphones
# For now it only changes the "+" time with an actual date/time and outputs the list in a csv-type format
# Made by NAE001 DPA Øst

import re
from datetime import datetime
import sys


batterystats_file = sys.argv[-1]                                                            # Defines the file to be the last argument in the command line
file = open(batterystats_file, "r")                                                         # Opens file in read mode
text = file.read()
sourceFile = batterystats_file                                                              # Put filename into a variable

print("Time|Unknown Value|Battery percentage|Data|Source")                                  # Create the headlines for the output


def rootTimestamp():                                                                        # Defines the function that converts the root time to a timestamp
    pattern = re.search(r'\d{4}([-]\d{2}){5}',text)                                         # Regex to search for first instance of dateTime
    root_date = pattern.group()                                                             # Show only the date
    
    year = root_date[0:4]                                                                   # Take each value into their own variable
    month = root_date[5:7]
    day = root_date[8:10]
    hour = root_date[11:13]
    minute = root_date[14:16]
    seconds = root_date[17:19]
    
    converted_rootDate = ("%s-%s-%s %s:%s:%s" % (month, day, year, hour, minute, seconds))  # Rearranges the dateTime
    
    datetime_object = datetime.strptime(converted_rootDate, '%m-%d-%Y %H:%M:%S')            # Converts to "python datetime" readable format
    
    timestamp1 = datetime.timestamp(datetime_object)                                        # Converts dateTime to timestamp
    return timestamp1                                                                       # returns the output from the function, so that it can be used in function 2

    file.close()                                                                            # Closes the file


def convertAndPrint(timestamp):                                                             # Defines the function that converts the plus-time and prints the converted lines
    file = open(batterystats_file, "r")
    lines = [[x.rstrip('\n')] for x in file][2:]                                            # splitting the file data into lines, skip n [2:] lines (irrelevant data in these lines)
    
    for line in lines:                                                                      # "For loop" start. What happens after this will be done against every line in the file
        joint_lines = (' '.join(line))
        split_lines = joint_lines.split()
        
        line_lenght = len(split_lines)                                                      # Counts elements in each line
        
        if line_lenght <= 0:                                                                # Checks that the line is not empty (lenght not equal to or less than 0)
            continue                                                                        # If it is, skip that line
            
        else:                                                                               # If not, proceed with the calculation/conversion
            plus_time = split_lines[0]                                                      # Adds row 1 in each line to a variable
            x = plus_time[0]                                                                # Add first letter to variable x
    
            if(bool(re.match('^[+]*$',x))==False):                                          # Check if variable x == + and skip that line if the return is false.
                continue
            else:                                                                           # Continue with the conversion/calculation if the line starts with "+"
                split_plus_time = re.split('\+|d|h|ms|m|s', plus_time)                      # Separates every values in plus_time based on multiple delimiters
                unknown_value = split_lines[1]                                              # Adds row 2 in each line to a variable, etc
                battery_percentage = split_lines[2]
                data = split_lines[3:]
            
                list_size = len(split_plus_time)                                            # Counts the elements in each timestamp list
                
                if list_size < 4:                                                           # Only extracts the elements present in the list, the variable is else set to "0" as something had to be in it
                    ms = split_plus_time[-2]
                    s = 0
                    m = 0
                    h = 0
                    d = 0
                
                elif list_size < 5:
                    ms = split_plus_time[-2]
                    s = split_plus_time[-3]
                    m = 0
                    h = 0
                    d = 0
            
                elif list_size < 6:
                    ms = split_plus_time[-2]
                    s = split_plus_time[-3]
                    m = split_plus_time[-4]
                    h = 0
                    d = 0
                    
                elif list_size < 7:
                    ms = split_plus_time[-2]
                    s = split_plus_time[-3]
                    m = split_plus_time[-4]
                    h = split_plus_time[-5]
                    d = 0
                    
                else:
                    ms = split_plus_time[-2]
                    s = split_plus_time[-3]
                    m = split_plus_time[-4]
                    h = split_plus_time[-5]
                    d = split_plus_time[-6]
            
                t_ms = (float(ms)*0.001)                                                        # Calculation to convert the numbers to seconds. Also specifies the type of data
                t_s = (int(s)*1)
                t_m = (int(m)*60)
                t_h = (int(h)*3600)
                t_d = (int(d)*86400)
                
                plus_timestamp = (t_d + t_h + t_m + t_s + t_ms)                                 # Add all the times together
                
                new_timestamp = (timestamp + plus_timestamp)                                    # Add plus timestamp to original timestamp
                new_time = datetime.fromtimestamp(new_timestamp).strftime("%d-%m-%Y %H:%M:%S")  # Convert new timestamp to time in the specified format
                
                print(new_time,"|",unknown_value,"|",battery_percentage,"|",data, "|", sourceFile)               # Print the new line in the specified csv-format with pipe as delimiter

    file.close()

convertAndPrint(rootTimestamp())                                                                # Calls for the seccond function (where the first function is included because of the timestamp variable)
