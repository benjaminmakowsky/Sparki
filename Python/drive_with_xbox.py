#A=  (EV_KEY), code 304 (BTN_SOUTH)	 	= Corresponds to Xbox360 button = a
#B=  (EV_KEY), code 305 (BTN_EAST)	 	= Corresponds to Xbox360 button = b
#X=  (EV_KEY), code 307 (BTN_NORTH)	 	= Corresponds to Xbox360 button = x
#Y=  (EV_KEY), code 308 (BTN_WEST)	 	= Corresponds to Xbox360 button = y

#L1= (EV_KEY), code 310 (BTN_TL)	 	= Corresponds to Xbox360 button = lb
#L2= (EV_KEY), code 10 (BTN_TL2) KEY_#312	= Corresponds to Xbox360 button = lt
#R1= (EV_KEY), code 311 (BTN_TR)	 	= Corresponds to Xbox360 button = rb
#R2= (EV_KEY), code 9 (BTN_TR2) KEY_#313	= Corresponds to Xbox360 button = rt

#Start= (EV_KEY), code 315 (BTN_START)	 = Corresponds to Xbox360 button = start
#Select= (EV_KEY), code 314 (BTN_SELECT)	 = Corresponds to Xbox360 button = back

#Digital Up= (EV_ABS), code 17 (ABS_HAT0Y)	 = Corresponds to Xbox360 button = dpad_y
#Digital Down= (EV_ABS), code 17 (ABS_HAT0Y)	 = Corresponds to Xbox360 button = dpad_y
#Digital Left= (EV_ABS), code 16 (ABS_HAT0X)	 = Corresponds to Xbox360 button = dpad_x
#Digital Right= (EV_ABS), code 16 (ABS_HAT0X)	 = Corresponds to Xbox360 button = dpad_x

#Left Analog Up= (EV_ABS), code 1 (ABS_Y)	 	= Corresponds to Xbox360 button = y1
#Left Analog Down= (EV_ABS), code 1 (ABS_Y)	 	= Corresponds to Xbox360 button = y1
#Left Analog Left= (EV_ABS), code 0 (ABS_X)	 	= Corresponds to Xbox360 button = x1
#Left Analog Right= (EV_ABS), code 0 (ABS_X)	 	= Corresponds to Xbox360 button = x1
#Left Analog Button= (EV_KEY), code 317 (BTN_THUMBL)	= Corresponds to Xbox360 button = tl

#Right Analog Up= (EV_ABS), code 5 (ABS_RZ)	 	 = Corresponds to Xbox360 button = y2
#Right Analog Down= (EV_ABS), code 5 (ABS_RZ)	 	 = Corresponds to Xbox360 button = y2
#Right Analog Left= (EV_ABS), code 2 (ABS_Z)	 	 = Corresponds to Xbox360 button = x2
#Right Analog Right= (EV_ABS), code 2 (ABS_Z)	 	 = Corresponds to Xbox360 button = x2
#Right Analog Button= (EV_KEY), code 318 (BTN_THUMBR)	 = Corresponds to Xbox360 button = tr

#imports for finding files
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))


#Standard import statements
import asyncio
from helper_keyboard_input import KeyboardHelper
from sphero_sdk import SpheroRvrAsync
from sphero_sdk import SerialAsyncDal
from evdev import InputDevice, categorize, ecodes

#Global variables used for driving
A_BUTTON = 304
B_BUTTON = 305
X_BUTTON = 307
Y_BUTTON = 308
L_BUMPER = 310
R_BUMPER = 311

key_helper = KeyboardHelper()
current_key_code = -1 #default variable 
driving_keys = [A_BUTTON, B_BUTTON, X_BUTTON, Y_BUTTON, L_BUMPER, R_BUMPER]
speed = 0
heading = 0
flags = 0

loop = asyncio.get_event_loop()
controller = InputDevice('/dev/input/event0')

rvr = SpheroRvrAsync(
    dal=SerialAsyncDal(
        loop
    )
)

#Function used to update button and print statement verifying
def keycode_callback(keycode):
    global current_key_code
    current_key_code = keycode
    print("Key code updated: ", str(current_key_code))

#Main driving method
async def main():
    """
    Runs the main control loop for this demo.  Uses the KeyboardHelper class to read a keypress from the terminal.
    A - Go forward.  Press multiple times to increase speed.
    LB - Decrease heading by -10 degrees with each key press.
    B - Go reverse. Press multiple times to increase speed.
    RB - Increase heading by +10 degrees with each key press.
    X/Y - Reset speed and flags to 0. RVR will coast to a stop
    """
    
    while True:

        if current_key_code == A_BUTTON:  # W
            # if previously going reverse, reset speed back to 64
            if flags == 1:
                speed = 64
            else:
                # else increase speed
                speed += 64
            # go forward
            flags = 0
        elif current_key_code == L_BUMPER:  # A
            heading -= 10
        elif current_key_code == R_BUMPER:  # D
            heading += 10
        elif current_key_code == X_BUTTON:  # SPACE
            # reset speed and flags, but don't modify heading.
            speed = 0
            flags = 0

        # check the speed value, and wrap as necessary.
        if speed > 255:
            speed = 255
        elif speed < -255:
            speed = -255

        # check the heading value, and wrap as necessary.
        if heading > 359:
            heading = heading - 359
        elif heading < 0:
            heading = 359 + heading

        # reset the key code every loop
        #current_key_code = -1

        # issue the driving command
        #await rvr.drive_with_heading(speed, heading, flags)

        # sleep the infinite loop for a 10th of a second to avoid flooding the serial port.
        #await asyncio.sleep(0.1)


def run_loop():
    global loop
    loop.run_until_complete(
        asyncio.gather(
        #    main(),
            read_controller(controller)
        )
    )

async def read_controller(controller):

    global current_key_code
    global speed
    global heading
    global flags

    await rvr.wake()

    await rvr.reset_yaw()

    async for btn_press in controller.async_read_loop():  
        #print("Type: " + str(btn_press.type) + "\tCode: " + str(btn_press.code) + "\tVal: "+ str(btn_press.value))

        if((btn_press.code) == 304 and (btn_press.value) == 1):
            print("A Button Pressed")
            keycode_callback(304)
                        
            if flags == 1:
                speed = 64
            else:
                # else increase speed
                speed += 64
            # go forward
            flags = 0
            print("Speed: " + str(speed))

        
        if((btn_press.code) == 9):
            print("RT Button Pressed")
            keycode_callback(9)
                        
            speed = int((btn_press.value) / 1023 * 255)
            if speed < 15:
                speed = 0
            # go forward
            flags = 0
            print("Speed: " + str(speed))

        if((btn_press.code) == 305 and (btn_press.value) == 1):
            print("B Button Pressed")
            keycode_callback(305)
            speed = 0
             
            

        if((btn_press.code) == 307 and (btn_press.value) == 1):
            print("X Button Pressed")
            keycode_callback(307)
            
            # if previously going forward, reset speed back to 64
            if flags == 0:
                speed = 64
            else:
                # else increase speed
                speed += 64
            # go reverse
            flags = 1
            print("Speed: " + str(speed))


        if((btn_press.code) == 308 and (btn_press.value) == 1):
            print("Y Button Pressed")
            keycode_callback(308)

        if((btn_press.code) == 310 and (btn_press.value) == 1):
            print("LB Button Pressed")
            keycode_callback(308)
            heading -= 10

        # check the speed value, and wrap as necessary.
        if speed > 255:
            speed = 255
        elif speed < -255:
            speed = -255


        # check the heading value, and wrap as necessary.
        if heading > 359:
            heading = heading - 359
        elif heading < 0:
            heading = 359 + heading

        # reset the key code every loop
        current_key_code = -1

        # issue the driving command
        await rvr.drive_with_heading(speed, heading, flags)

        # sleep the infinite loop for a 10th of a second to avoid flooding the serial port.
        await asyncio.sleep(0.05)

if __name__ == "__main__":
    loop.run_in_executor(None, key_helper.get_key_continuous)
    run_loop()
    #try:
    #    run_loop()
    #except KeyboardInterrupt:
    #    print("Keyboard Interrupt...")
    #    key_helper.end_get_key_continuous()
    #finally:
    #    print("Press any key to exit.")
    #    exit(1)



