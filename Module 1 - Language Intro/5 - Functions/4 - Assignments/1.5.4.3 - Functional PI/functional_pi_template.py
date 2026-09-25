import math


def my_pi(target_error):
    """
    Implementation of Gauss–Legendre algorithm to approximate PI from https://en.wikipedia.org/wiki/Gauss%E2%80%93Legendre_algorithm

    :param target_error: Desired error for PI estimation
    :return: Approximation of PI to specified error bound
    """

    ### YOUR CODE HERE ###
    a = 1.0
    b = 1.0 / math.sqrt(2)
    t = 0.25
    p = 1.0

    while True:
        a_new = (a + b) / 2
        b_new = math.sqrt(a * b)
        t_new = t - p * (a - a_new) ** 2
        p_new = 2 * p

        if abs(math.pi - (a + b) ** 2 / (4 * t)) < target_error:
            break

        a, b, t, p = a_new, b_new, t_new, p_new

    pi_approximation = (a + b) ** 2 / (4 * t)

    # change this so an actual value is returned
    
    return pi_approximation


desired_error = 1E-10

approximation = my_pi(desired_error)

print("Solution returned PI=", approximation)

error = abs(math.pi - approximation)

if error < abs(desired_error):
    print("Solution is acceptable")
else:
    print("Solution is not acceptable")
