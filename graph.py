from matplotlib import pyplot

class Graph:
    
    def __init__(self, title, winsize, xlabel, ylabel):
        pyplot.rcParams['toolbar'] = 'None'
        pyplot.xlabel(xlabel)
        pyplot.ylabel(ylabel)
        pyplot.title(title)
        pyplot.grid(True)
        self.temps = None

    def plot(self, temperatures, target, delta_t, legend1=None, legend2=None):
        time = [delta_t * i for i in range(len(temperatures))]

        if not self.temps:
            self.temps,  = pyplot.plot(time, temperatures, label=legend1)
            self.target, = pyplot.plot(time, [target] * len(temperatures), label=legend2)
            pyplot.legend()
        else:
            self.temps.set_data(time, temperatures)
            self.target.set_data(time, [target] * len(temperatures))

        pyplot.xlim(0, max(0.1, delta_t*(len(temperatures)-1)))
        pyplot.ylim(min(temperatures + [target-2]), max(temperatures + [target+2]))
        pyplot.draw()
        pyplot.show(block=False)
        pyplot.pause(0.01)
