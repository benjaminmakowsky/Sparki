import mysql.connector
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

import asyncio
from sphero_sdk import SpheroRvrAsync
from sphero_sdk import SerialAsyncDal
from sphero_sdk import BatteryVoltageStatesEnum as VoltageStates

loop = asyncio.get_event_loop()
rvr = SpheroRvrAsync(dal=SerialAsyncDal(loop))


#Define variables
DATABASE_NAME = "SPARKI"


#Connect to mysql
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="YOUR_PASSWORD_HERE" #CHANGE THIS PASSWORD
)

#A cursor is just an object that lets you interact with a database, like a mouse -> computer
mycursor = mydb.cursor()
mycursor.execute("SHOW DATABASES")

#Check if the database already exists
db_exists = False
databases = mycursor.fetchall()
for db in databases: #db is a tuple with only a single element so we need to use indexing
    if (db[0] == DATABASE_NAME):
        db_exists = True

# if databse does not exist create it
if(db_exists == False):
    print("Database not found, Creating now...")
    mycursor.execute("CREATE DATABASE " + DATABASE_NAME)     
else:
    #If database exists, wipe it to start fresh
    print("Database already exists. Deleting and Recreating")
    mycursor.execute("DROP DATABASE " + DATABASE_NAME)
    mycursor.execute("CREATE DATABASE " + DATABASE_NAME)     

#Connect to the database
print("Connecting to DB: " + DATABASE_NAME)
mydb.connect(database=DATABASE_NAME)

#Create a table called: stats with a cell called battery
print("Creating Table: stats with a cell: battery")
mycursor.execute("CREATE TABLE stats (battery VARCHAR(255))")


async def main():
    """ This program demonstrates how to retrieve the battery state of RVR.
    """

    await rvr.wake()

    # Give RVR time to wake up
    await asyncio.sleep(2)

    battery_percentage = await rvr.get_battery_percentage()
    print('Battery percentage: ', battery_percentage)

    # battery_voltage_state = await rvr.get_battery_voltage_state()
    # print('Voltage state: ', battery_voltage_state)


    ## Store battery level in database
    query = "INSERT INTO SPARKI.stats (battery) VALUES (%s)"
    values= ("Battery Level: " + str(battery_percentage.get("percentage")),)
    mycursor.execute(query, values)
    mydb.commit()

    mycursor.execute("SELECT * FROM SPARKI.stats")
    records = mycursor.fetchall() ## it returns list of tables present in the database
    for record in records:
        print(record)

    await rvr.close()


if __name__ == '__main__':
    try:
        loop.run_until_complete(
            main()
        )

    except KeyboardInterrupt:
        print('\nProgram terminated with keyboard interrupt.')

        loop.run_until_complete(
            rvr.close()
        )

    finally:
        if loop.is_running():
            loop.close() terminated with keyboard interrupt.')

        loop.run_until_complete(
            rvr.close()
        )

    finally:
        if loop.is_running():
            loop.close()