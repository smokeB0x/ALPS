"""Functions/module to be used in the ALPS program

Version: 1.1
Created: 28.02.23
Last modified: 15.03.23
"""


def explainer (_data):
    """
    Looks for patterns in the data columns in nbsParcer and writes an explanation based on the contents
    The list will be expanded based on test results
    """
    
    import re
    i = len(_data)
    if i == 0:                                                                      
        explanation = 'no data'
    elif re.search(r'\+top', str(_data)) and re.search('com.sec.android.app.launcher', str(_data)):
        explanation = 'system function'
    elif re.search(r'\-top', str(_data)) and re.search('com.sec.android.app.launcher', str(_data)):
        explanation = 'system function'
    elif re.search(r'\+top', str(_data)):
        explanation = "app in focus"
    elif re.search(r'\-top', str(_data)):
        explanation = "app out of focus"
    elif re.search(r'\+camera', str(_data)):
        explanation = "camera in focus"
    elif re.search(r'\-camera', str(_data)):
        explanation = "camera out of focus"
    elif re.search(r'\+screen', str(_data)):
        explanation = "screen on"
    elif re.search(r'\-screen', str(_data)):
        explanation = "screen off"
    elif re.search(r'\status=charging', str(_data)):
        explanation = "Charging started"
    else: 
        explanation = " "
    return explanation


def logger (_file, _datetime):
    """
    Creates a logfile and inputs filename, date of file added, and md5sum into logfile
    """
    
    import hashlib
    md5sum = hashlib.md5(open(_file, 'rb').read()).hexdigest()
    logfile = open('addLog.log', 'a')                                                          # Writes to a log file (append 'a' is used instead of 'w' to not overwrite the file every time) 
    print("adding", _file, "to database")
    print("File added to database", file = logfile)
    print("File: ", _file, file = logfile)
    print("Time: ", _datetime, file = logfile)
    print("MD5: ", md5sum, file = logfile)
    print("---------------------------------------------", file = logfile)
    logfile.close()
