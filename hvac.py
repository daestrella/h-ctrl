class Environment:
    pass

class Sensor:
    def __init__(self):
        self.history = []

    def temperature(self):
        self.history.append(Environment.temperature)
        return Environment.temperature

class Controller:
    def __init__(self):
        from mf import trimf, zbimf, sbimf, trapmf

        self.previous_error = 0
        # fuzzy set membership functions for hot and cold based on error
        self.currently_hot = zbimf(-1, 0)
        self.currently_cold = sbimf(0, 1)
        self.currently_at_target = trimf(-1, 0, 1)

        self.getting_cooler = sbimf(0, 1)
        self.getting_warmer = zbimf(-1, 0)
        self.no_change = trapmf(-1, -0.1, 0.1, 1)
        
        self.run_heater = sbimf(0, 0.5)
        self.run_cooler = zbimf(-0.5, 0)
        self.do_nothing = trimf(-0.5, 0, 0.5)

    def change_target(self, temperature):
        self.target = temperature

    def regulate(self, temperature):
        from fuzzyops import Fuzzy, Rule

        error = self.target - temperature
        delta = (self.previous_error - error)
        
        power = Fuzzy.defuzzify(Fuzzy.aggregate([
            Rule((self.currently_hot(error), min, self.getting_warmer(delta)), self.run_cooler),
            Rule((self.currently_hot(error), min, self.no_change(delta)), self.run_cooler),
            Rule((self.currently_hot(error), min, self.getting_cooler(delta)), self.run_cooler),

            Rule((self.currently_cold(error), min, self.getting_warmer(delta)), self.run_heater),
            Rule((self.currently_cold(error), min, self.no_change(delta)), self.run_heater),
            Rule((self.currently_cold(error), min, self.getting_cooler(delta)), self.run_heater),

            Rule((self.currently_at_target(error), min, self.getting_warmer(delta)), self.run_cooler),
            Rule((self.currently_at_target(error), min, self.no_change(delta)), self.do_nothing),
            Rule((self.currently_at_target(error), min, self.getting_cooler(delta)), self.run_heater),
            ]), startpos=-abs(error)-0.5, endpos=abs(error)+0.5
        )

        self.previous_error = error
        Environment.temperature = temperature + power



        





