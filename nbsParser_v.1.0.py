"""A script/function for parcing the file newbatterystats from android smartphones.
Changes the + time in the file into the actual datetime, removes lines demed irrelevant, and 
writes the contents into a database

Version: 1.0
Created: 19.01.23
Last modified: 04.02.23
"""

def nbsParcer():                                                                                # Define the function that parses the newbatterystats-file
    import re
    from datetime import datetime
    import sys
    import sqlite3
    from modules import alpsModules
    
    batterystats_file = sys.argv[-1]                                                            # Defines the file to be the last argument in the command line
    file = open(batterystats_file, "r")                                                         # Opens file in read mode
    text = file.read()
    current_datetime = datetime.now()                                                           # Gets the current date (to be used in the logfile)
    
    conn = sqlite3.connect('ALPS_main.db')                                                      # Set the database name to be "ALPS_main" 
    c = conn.cursor()
    
    c.execute('''
              CREATE TABLE IF NOT EXISTS newbatterystats
              ([Timestamp] REAL, [unknown_value] TEXT, [battery_level] INTEGER, [data] TEXT, [explanation] TEXT, [Source] TEXT)
              ''')                                                                          # Create a table and headlines in table.  Define the different values.
                         
    conn.commit()

    alpsModules.logger(batterystats_file, current_datetime)                                 # Run the logger function in modules
##### Find and donvert 0-timestamp start                 
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
    
    timestamp = datetime.timestamp(datetime_object)                                         # Converts dateTime to timestamp

    file.close()                                                                            # Closes the file

### Find and convert 0-timestamp end
### Parse the logfile start
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
                    
                elif list_size >= 7:
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
### Explanation list start
                explanation = alpsModules.explainer(data)                                       # Run the explainer function in modules
### Explanation list end
                data = str(data)                                                                # Needed to define this as a string after the "explainer" had used the list
                    
                c.execute("INSERT INTO newbatterystats (Timestamp, unknown_value, battery_level, data, explanation, source) VALUES (?, ?, ?, ?, ?, ?)",
                          (new_time, unknown_value, battery_percentage, data, explanation, batterystats_file)) # Insert the varables into the different columns in 
  
                conn.commit()
                

    file.close()
    c.close()
    conn.close()
    
    print(batterystats_file, "added to database")
nbsParcer()                                                                                     # Run the function present in this script
### Parce the logfile end
