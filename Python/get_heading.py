import os
import sys
import math
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

import asyncio
from sphero_sdk import SpheroRvrAsync
from sphero_sdk import SerialAsyncDal


loop = asyncio.get_event_loop()

rvr = SpheroRvrAsync(
    dal=SerialAsyncDal(
        loop
    )
)


async def main():
    """ This program demonstrates how to get a reading from the magnetometer on RVR.
    """

    await rvr.wake()

    # Give RVR time to wake up
    await asyncio.sleep(2)

    magnetometer_reading = await rvr.get_magnetometer_reading()
    print(type(magnetometer_reading))
    print(270-math.atan(magnetometer_reading["x_axis"]/ magnetometer_reading["y_axis"])*180/3.14)
    print('Magnetometer reading: ', magnetometer_reading)

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
