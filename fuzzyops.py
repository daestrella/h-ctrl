from functools import reduce
import numpy as np

class Fuzzy:
    @staticmethod
    def complement(mf):
        ''' Applies fuzzy complement of the given mf '''
        return lambda x: 1 - mf(x)

    @staticmethod
    def intersection(*mfs):
        ''' Applies fuzzy intersection by applying the min function to all input mfs '''
        return lambda x: reduce(min, [mf(x) for mf in mfs])

    @staticmethod
    def union(*mfs):
        ''' Applies fuzzy union by applying the max function to all input mfs '''
        return lambda x: reduce(max, [mf(x) for mf in mfs])

    @staticmethod
    def aggregate(rules):
        ''' Aggregates rules by applying a Mamdani inference system. '''
        from mf import constmf
        rule_mfs = [Fuzzy.intersection(constmf(rule.generate_antecedent()),
                                       rule.consequent) for rule in rules]

        return reduce(Fuzzy.union, rule_mfs) # Generates a crease [membership] function

    @staticmethod
    def defuzzify(mf, startpos, endpos):
        ''' Defuzzifying fuzzy set using the centroid defuzzification '''
        try:
            xvals = np.arange(startpos, endpos+1, 0.01)
            yvals = np.vectorize(mf, otypes=[float])(xvals)

            with np.errstate(divide='ignore', invalid='ignore'):
                return np.nan_to_num(np.sum(xvals * yvals)/np.sum(yvals))
        except (ZeroDivisionError, ValueError):
            return 0

class Rule:
    def __init__(self, antecedent, consequent):
        ''' Generates a rule for inference

        Keyword arguments:
        antecedent -- tuple of floats (odd elements) and Fuzzy set operations (even)
        consequent -- function
        '''
        self.consequent = consequent
        self.antecedent = antecedent

    def generate_antecedent(self):
        const = self.antecedent[0]

        for function, value in zip(self.antecedent[1::2], self.antecedent[2::2]):
            const = function(const, value)

        return const
