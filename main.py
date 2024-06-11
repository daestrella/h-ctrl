import curses
from time import sleep
from init import init
from HVAC import Sensor, Controller

sensor, controller, graph = init()
delta_t = 0.1

screen = curses.initscr()
curses.noecho()
curses.cbreak()
screen.keypad(True)
screen.nodelay(True)

try:
    while True:
        char = screen.getch()

        if char == ord('q'):
            break

        controller.regulate(sensor.temperature())
        graph.plot(sensor.history, controller.target, delta_t,
                   legend1='temperature', legend2='target')
        sleep(delta_t)

finally:
    curses.nocbreak()
    screen.keypad(0)
    curses.echo()
    curses.endwin()
        
