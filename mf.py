def check_if_sorted(*values):
    if not all(values[i] <= values[i+1] for i in range(len(values)-1)):
        raise ValueError(f'Inputs must be sorted in ascending order '
                         f'to create a membership function. '
                         f'Inputs given: {values}')

def trapmf(a, b, c, d):
    ''' Generates a trapezoidal membership function '''
    check_if_sorted(a, b, c, d)
    return lambda x: max(0, min((x-a)/(b-a), 1, (d-x)/(d-c)))

def trimf(a, b, c):
    ''' Generates a triangular membership function '''
    check_if_sorted(a, b, c)
    return lambda x: max(0, min((x-a)/(b-a), (c-x)/(c-b)))

def zbimf(a, b):
    ''' Generates a z-shaped membership function '''
    check_if_sorted(a, b)
    return lambda x: max(0, min(1, (b-x)/(b-a)))

def sbimf(a, b):
    ''' Generates a s-shaped membership function '''
    check_if_sorted(a, b)
    return lambda x: max(0, min(1, (x-a)/(b-a)))

def gaussmf(c, sigma):
    ''' Generates a Gaussian membership function '''
    from math import e
    return lambda x: e ** ((-(x - c) ** 2) / (2 * sigma ** 2))

def constmf(const):
    ''' Generates a constant membership function '''
    return lambda x: const
