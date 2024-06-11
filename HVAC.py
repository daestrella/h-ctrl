class Environment:
    pass

class Sensor:
    def __init__(self):
        self.history = []

    def temperature(self):
        self.history.append(Environment.temperature)
        return Environment.temperature

class Controller:
    def __init__(self, target, max_increment):
        from mf import trimf, zbimf, sbimf, trapmf

        self.target = target
        self.previous_error = 0
        self.max = max_increment

        # fuzzy set membership functions for hot and cold based on error
        self.currently_hot = zbimf(-3, 0)
        self.currently_cold = sbimf(0, 3)
        self.currently_at_target = trimf(-0.1, 0, 0.1)

        self.getting_cooler = sbimf(0, 3)
        self.getting_warmer = zbimf(-3, 0)
        self.no_change = trimf(-1, 0, 1)
        
        self.run_heater = sbimf(0, 5)
        self.run_cooler = zbimf(-5, 0)
        self.do_nothing = trapmf(-1, -0.75, 0.75, 1)

    def regulate(self, temperature):
        from fuzzyops import Fuzzy, Rule

        error = self.target - temperature
        delta = (error - self.previous_error)
        
        power = Fuzzy.defuzzify(Fuzzy.aggregate([
            Rule((self.currently_hot(error), min, self.getting_warmer(delta)), self.run_cooler),
            Rule((self.currently_hot(error), min, self.no_change(delta)), self.run_cooler),
            Rule((self.currently_hot(error), min, self.getting_cooler(delta)), self.run_cooler),

            Rule((self.currently_cold(error), min, self.getting_warmer(delta)), self.run_heater),
            Rule((self.currently_cold(error), min, self.no_change(delta)), self.run_heater),
            Rule((self.currently_cold(error), min, self.getting_cooler(delta)), self.run_heater),

            Rule((self.currently_at_target(error), min, self.getting_warmer(delta)), self.run_heater),
            Rule((self.currently_at_target(error), min, self.no_change(delta)), self.do_nothing),
            Rule((self.currently_at_target(error), min, self.getting_cooler(delta)), self.run_cooler),
            ]), startpos=-abs(error), endpos=abs(error)
        )

        #print(f'Currently = {temperature:.2f}; Error = {error:.2f}; Error-dot = {delta:.2f}; Power = {power:.2f}\n'
        #      f'\thot? {self.currently_hot(error):.2f}; cold? {self.currently_cold(error):.2f}; close? {self.currently_at_target(error):.2f}\n'
        #      f'\twarmer? {self.getting_warmer(delta):.2f}; cooler? {self.getting_cooler(delta):.2f}; no_change? {self.no_change(delta):.2f}\n'
        #      f'R1: {min(self.currently_hot(error), self.getting_warmer(delta)):.2f}; R2: {min(self.currently_hot(error), self.no_change(delta)):.2f}; '
        #      f'R3: {min(self.currently_hot(error), self.getting_cooler(delta)):.2f}; R4: {min(self.currently_cold(error), self.getting_warmer(delta)):.2f}; '
        #      f'R5: {min(self.currently_cold(error), self.no_change(delta)):.2f}; R6: {min(self.currently_cold(error), self.getting_cooler(delta)):.2f}; '
        #      f'R7: {min(self.currently_at_target(error), self.getting_warmer(delta)):.2f}; R8: {min(self.currently_at_target(error), self.no_change(delta)):.2f}; '
        #      f'R9: {min(self.currently_at_target(error), self.getting_cooler(delta)):.2f}\n')

        self.previous_error = error
        Environment.temperature = temperature + power



        





