from hvac import Sensor, Controller, Environment
from graph import Graph
from init import retrieve_args
from time import sleep
import curses

def get_target_temp(stdscr, prompt):
    stdscr.clear()
    curses.echo()
    stdscr.addstr(0, 0, prompt)
    stdscr.refresh()
    temp = int(stdscr.getstr(0, len(prompt), 3))
    curses.noecho()
    return temp

def main(stdscr):
    args = retrieve_args()

    Environment.temperature = args.init
    dt = args.time
    sensor = Sensor()
    controller = Controller()
    graph = Graph(title=f'Temperature', winsize=(12, 6),
                  xlabel='time', ylabel='temperature')

    while True:
        stdscr.nodelay(0)
        controller.change_target(get_target_temp(stdscr, "Enter target: "))

        while True:
            stdscr.nodelay(1)
            key = stdscr.getch()
            if key == ord('q'):
                return

            if key == 27:
                break

            controller.regulate(sensor.temperature())
            graph.plot(sensor.history, controller.target, dt,
                       legend1='temperature', legend2='target')
        
            sleep(dt)

stdscr = curses.initscr()
curses.noecho()
curses.cbreak()
main(stdscr)
curses.nocbreak()
curses.echo()
curses.endwin()
