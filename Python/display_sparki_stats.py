import mysql.connector
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../')))

import asyncio
from sphero_sdk import SpheroRvrAsync
from sphero_sdk import SerialAsyncDal
from sphero_sdk import BatteryVoltageStatesEnum as VoltageStates

#Define variables
DATABASE_NAME = "SPARKI"
loop = asyncio.get_event_loop()
rvr = SpheroRvrAsync(dal=SerialAsyncDal(loop))

#Connect to mysql
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="password"
)

#A cursor is just an object that lets you interact with a database, like a mouse -> computer
mycursor = mydb.cursor()

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

#Creating table meesages with cells msg
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
    mycursor.execute("INSERT INTO stats (battery) VALUES (%s)", battery_percentage)
    mydb.commit()

    # state_info = '[{}, {}, {}, {}]'.format(
    #     '{}: {}'.format(VoltageStates.unknown.name, VoltageStates.unknown.value),
    #     '{}: {}'.format(VoltageStates.ok.name, VoltageStates.ok.value),
    #     '{}: {}'.format(VoltageStates.low.name, VoltageStates.low.value),
    #     '{}: {}'.format(VoltageStates.critical.name, VoltageStates.critical.value)
    # )
    # print('Voltage states: ', state_info)

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
            loop.close()