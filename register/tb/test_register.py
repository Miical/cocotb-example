'''
A cocotb-pytest test (this file) has two parts:

1. Testbench
    - Any python function decorated with @cocotb.test()
    - Drives signals into pins of the design, reads the output/intermediate pins and compares with expected results
    - Uses async-await:
        - Declared as def async
        - when "await Event()", simulator advances in simulation time until the Event() happens
    - You can have multiple such testbenches too. Pytest would find and run them all
2. PyTest
    - The setup that connects the simulator of your choice,
    - Feeds the design files,
    - Finds your testbenches (1),
    - Parametrizes them to generate multiple versions of the designs & tests
    - Runs all such tests and prints a report of pass & fails
'''



import sys
sys.path.append('/home/miical/Projects/cocotb-example/register/hdl/')
sys.path.append("/home/miical/Projects/PyMLVP/src/")

import mlvp
from mlvp import *
from mlvp.triggers import *
from ovip import UTregister


import random
# import numpy as np

'''
1. Testbench
'''

async def register_tb(dut):

    ''' Clock Generation '''
    mlvp.create_task(mlvp.start_clock(dut, dut.clk))
    print("Clock started")

    ''' Assign random values to input, wait for a clock and verify output '''
    for i in range(100): # 100 experiments

        exact = random.randint(0, 255) # generate randomized input
        dut.d.value = exact # drive pins

        await ClockCycles(dut, 2)

        computed = dut.q.value # Read pins as unsigned integer.
        # computed = dut.q.value.signed_integer # Read pins as signed integer.

        assert exact == computed, f"Failed on the {i}th cycle. Got {computed}, expected {exact}" # If any assertion fails, the test fails, and the string would be printed in console
        print(f"Driven value: {exact} \t received value: {computed}")



'''
2. Pytest Setup
'''


def test_register():
    dut = UTregister(0, None)
    mlvp.run(register_tb(dut))
