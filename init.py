import argparse

def retrieve_args():
    parser = argparse.ArgumentParser(
            prog='t-ctrl',
            description=f'Simulates HVAC temperature regulator using fuzzy sets.')

    parser.add_argument('init', type=float,
                        help='initial temperature in degrees Celcius')
    parser.add_argument('time', type=float,
                        help='graph speed')

    return parser.parse_args()
