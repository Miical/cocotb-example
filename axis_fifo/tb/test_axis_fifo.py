'''
First read "register/tb/test_register.py"
Then read this file
'''

import random
import numpy as np

NUM_DATA = 1000

import sys
sys.path.append('/home/miical/Projects/cocotb-example/axis_fifo/hdl/')
sys.path.append("/home/miical/Projects/PyMLVP/src/")

import mlvp
import asyncio
from mlvp import *
from mlvp.triggers import *
from ovip import UTaxis_fifo
from custom_axis import axis_source, axis_sink

'''
1. Testbench
'''

async def axis_fifo_tb(dut):
    global NUM_DATA

    '''
    Clock Generation
    '''
    mlvp.create_task(mlvp.start_clock(dut, dut.aclk))

    '''Drive reset'''
    dut.aresetn.value = 0
    await ClockCycles(dut, 2)
    dut.aresetn.value = 1

    '''Create a numpy array'''
    data_in = np.random.randint(0, 255, size=(NUM_DATA), dtype=np.uint8)

    '''Start the two functions in two parallel threads'''
    task_source = mlvp.create_task(axis_source(dut, data_in, NUM_DATA)) # Drives values
    task_sink = mlvp.create_task(axis_sink(dut, data_in, NUM_DATA)) # Compares values

    '''Wait until both functions end'''
    await asyncio.gather(task_source, task_sink)



'''
2. Pytest Setup
'''

def test_axis_fifo():
    dut = UTaxis_fifo(0, None)
    mlvp.run(axis_fifo_tb(dut))
