import mysql.connector
import os
import sys
import math
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
    password="password" #CHANGE THIS PASSWORD
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
print("Creating Table: [id, battery, heading, light]")
query = "CREATE TABLE stats "
cells = "(id INT AUTO_INCREMENT PRIMARY KEY, battery VARCHAR(25), heading VARCHAR(25), light VARCHAR(255))"
mycursor.execute(query + cells)
query = "INSERT INTO SPARKI.stats (battery, heading, light) VALUES (\"no\", \"no\", \"no\")"
mycursor.execute(query)


async def calculateHeading():

    magnetometer_reading = await rvr.get_magnetometer_reading()
    if(magnetometer_reading["x_axis"] == 0):
        if(magnetometer_reading["y_axis"] < 0):
            return "90 Degrees West"
        else:
            return "0 Degrees North"

    direction = (270-math.atan(magnetometer_reading["x_axis"]/ magnetometer_reading["y_axis"])*180/3.14)
    if(direction > 360):
        direction = direction - 360
    elif(direction < 0):
        direction = direction + 360

    return str(direction)[:6] + " Degrees from North"

async def main():
    """ This program demonstrates how to retrieve the battery state of RVR.
    """

    await rvr.wake()

    # Give RVR time to wake up
    await asyncio.sleep(2)

    

    # battery_voltage_state = await rvr.get_battery_voltage_state()
    # print('Voltage state: ', battery_voltage_state)

    while(True):
        heading = await calculateHeading()
        battery_percentage = await rvr.get_battery_percentage()
        lightLevel = await rvr.get_ambient_light_sensor_value()
        ## Store battery level in database
        query = "UPDATE SPARKI.stats SET battery = %s"
        values= ("Battery: " + str(battery_percentage.get("percentage")) + "%",)
        mycursor.execute(query, values)

        query = "UPDATE SPARKI.stats SET heading = %s"
        values= (heading,)
        mycursor.execute(query, values)

        query = "UPDATE SPARKI.stats SET light = %s"
        values= (str(lightLevel.get("ambient_light_value"))[:5],)
        mycursor.execute(query, values)

        mydb.commit()

        mycursor.execute("SELECT * FROM SPARKI.stats")
        records = mycursor.fetchall() ## it returns list of tables present in the database
        for record in records:
            print(record)
        await asyncio.sleep(60)



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

        loop.run_until_complete(
            rvr.close()
        )