""" A selection of functions to read the ALPS database and execute various SQL queries 
More queries can/will be added as needed

Version: 1.0
Created: 04.03.23
Modified: 20.03.23
"""


import sqlite3
from sqlite3 import Error


def select_all(conn):
    """
    Query function: Select everything present in the newbatterystats table in the ALPS database
    """
    cur = conn.cursor()
    cur.execute("SELECT Timestamp, unknown_value, battery_level, data, explanation, Source FROM newbatterystats")
    
    rows = cur.fetchall()
    
    print("Query = Everything")
    print("{:<20}{:^2}{:<4}{:^2}{:>7}{:^2}{:<75}{:^2}{:<20}{:^2}{:<5}".format("Time", "|", "N/A", "|", "Battery", "|", "Data", "|", "Explanation", "|", "Source"))
    
    for row in rows:
        time = row[0]
        unknown = row[1]
        battery = row[2]
        data = row[3]
        explanation = row[4]
        source = row[5]
        
        print("{:<20}{:^2}{:<4}{:^2}{:>7}{:^2}{:<75}{:^2}{:<20}{:^2}{:<5}" .format(time, '|', unknown, '|', battery, '|', data, '|', explanation, '|', source))

def appinfocus(conn):
    """
    Query function: Select the entries in the newbatterystats table in the ALPS database that is connected to app in, and out of, focus 
    """
    cur = conn.cursor()
    cur.execute("SELECT Timestamp, unknown_value, battery_level, data, explanation, Source FROM newbatterystats WHERE explanation = 'app in focus' OR explanation = 'app out of focus'")
    
    rows = cur.fetchall()
    
    print("Query = App in focus")
    print("{:<20}{:^2}{:<4}{:^2}{:>7}{:^2}{:<75}{:^2}{:<20}{:^2}{:<5}".format("Time", "|", "N/A", "|", "Battery", "|", "Data", "|", "Explanation", "|", "Source"))
    
    for row in rows:
        time = row[0]
        unknown = row[1]
        battery = row[2]
        data = row[3]
        explanation = row[4]
        source = row[5]
        
        print("{:<20}{:^2}{:<4}{:^2}{:>7}{:^2}{:<75}{:^2}{:<20}{:^2}{:<5}" .format(time, '|', unknown, '|', battery, '|', data, '|', explanation, '|', source))

def screenstatus(conn):
    """
    Query function: Selects the entries in newbatterystats table in the ALPS database that is connected to screen on/off
    """
    # Insert query here
    cur = conn.cursor()
    cur.execute("SELECT Timestamp, unknown_value, battery_level, data, explanation, Source FROM newbatterystats WHERE explanation = 'screen on' OR explanation = 'screen off'")
    
    rows = cur.fetchall()
    
    print("Query = App in focus")
    print("{:<20}{:^2}{:<4}{:^2}{:>7}{:^2}{:<75}{:^2}{:<20}{:^2}{:<5}".format("Time", "|", "N/A", "|", "Battery", "|", "Data", "|", "Explanation", "|", "Source"))
    
    for row in rows:
        time = row[0]
        unknown = row[1]
        battery = row[2]
        data = row[3]
        explanation = row[4]
        source = row[5]
        
        print("{:<20}{:^2}{:<4}{:^2}{:>7}{:^2}{:<75}{:^2}{:<20}{:^2}{:<5}" .format(time, '|', unknown, '|', battery, '|', data, '|', explanation, '|', source))
    
def wificonnections(conn):
    """
    Query function: Selects the entries in newbatterystats table in the ALPS database that is connected to wifi connects/dissconnects
    """
    # Insert query here
    print("Under development")

def create_connection(_db_file):
    """
    System function, creates a connection with the database
    """
    conn = None
    try:
        conn = sqlite3.connect(_db_file)
    except Error as e:
        print(e)
    return conn

def main():
    """
    System function: The main query that defines the database and ask for what query function that should be run
    """
    database = r"ALPS_main.db"
    
    conn = create_connection(database)
    
    with conn:
        print("1. Query all\n2. App in focus\n3. Screen status\n4. Wifi connections")
        userSelection = int(input("Select query: "))
        if userSelection == 1:
            select_all(conn)
        elif userSelection == 2:
            appinfocus(conn)
        elif userSelection == 3:
            screenstatus(conn)
        elif userSelection == 4:
            wificonnections(conn)
        else:
            print("Not a viable option")

if __name__ == '__main__':
    main()