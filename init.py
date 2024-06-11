import argparse
from graph import Graph
from HVAC import Sensor, Controller, Environment

def init():
    parser = argparse.ArgumentParser(
            prog='t-ctrl',
            description=f'Simulates HVAC temperature regulator using fuzzy sets.')

    parser.add_argument('init', type=float,
                        help='initial temperature in degrees Celcius')
    parser.add_argument('target', type=float,
                        help='target temperature in degrees Celcius')

    temperatures = parser.parse_args()

    Environment.temperature = temperatures.init
    return Sensor(), Controller(temperatures.target, 0.5), Graph(title=f'Temperature', winsize=(12, 6), xlabel='time', ylabel='temperature')
