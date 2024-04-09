# ALPS
A collection of scripts for parsing logfiles in android
Version: 1.0

Note: This is a work in progress, and this version may contain errors. Use at your own risk and verify your results.

A program/collection of scripts for parsing and displaying log files from android.

	*******************
	* Usage make_case *
	*******************
python3 make_case.py -f <logfile> -t <type> 

This will create a database containing the data from the log files.

Note: a log named addLog.log will be added to the current working directory with creation-time and displaying the files that are added to the case and when.

supported types:
nbs	|	newbatterystats
*btc	|	bt_conf.bak 

	**********************
	* Usage display_case *
	**********************
*in development



Supported logfiles:
/data/log/batterystats/* (*multiple files named newbatterystats)

In development: 
/data/misc/bluedroid/bt_conf.bak
