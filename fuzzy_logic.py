import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

class Fuzzy_assembler:
    def __init__(self):
        # Inputs
        self.difficulty = ctrl.Antecedent(np.arange(0, 11, 1), 'difficulty')
        self.load = ctrl.Antecedent(np.arange(0, 11, 1), 'load')
        # Output
        self.assembly_time = ctrl.Consequent(np.arange(0, 11, 1), 'assembly_time')

        # Membership functions
        self.difficulty.automf(3, names = ["poor", "average", "good"])
        self.load.automf(3, names = ["poor", "average", "good"])

        self.assembly_time['short'] = fuzz.trimf(self.assembly_time.universe, [0, 0, 5])
        self.assembly_time['medium'] = fuzz.trimf(self.assembly_time.universe, [2, 5, 8])
        self.assembly_time['long'] = fuzz.trimf(self.assembly_time.universe, [5, 10, 10])

        # Rules
        rule1 = ctrl.Rule(self.difficulty['poor'] & self.load['poor'], self.assembly_time['short'])
        rule2 = ctrl.Rule(self.difficulty['good'] & self.load['average'], self.assembly_time['medium'])
        rule3 = ctrl.Rule(self.difficulty['good'] & self.load['good'], self.assembly_time['long'])
        rule4 = ctrl.Rule(self.difficulty['average'] | self.load['average'], self.assembly_time['medium'])

        # Control system
        self.controller = ctrl.ControlSystem([rule1, rule2, rule3, rule4])
        self.simulator = ctrl.ControlSystemSimulation(self.controller)

    def get_assembly_time(self, difficulty_value, load_value):
        self.simulator.input['difficulty'] = difficulty_value
        self.simulator.input['load'] = load_value
        self.simulator.compute()
        return self.simulator.output['assembly_time']

