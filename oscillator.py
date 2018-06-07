import numpy as np


# numeric simulation of probability distribution of
# a particle in a classical harmonic oscillator

# outputs p(x), <x>, <x^2>, <energy>

# x0 = 0, k = 1

# numerical solution:
# p(x) = 1 / (pi * sqrt(A^2 - x^2))
# <x> = 0
# <x^2> = A^2 / 2


def x(t, A, omega):
    '''harmonic oscillator position function'''
    return A * np.cos(omega * t)


A = 2  # amplitude 
omega = 1  # frequency
period = 2 * np.pi / omega

n_samples = 1000000
x_sampled = []

# sample time from uniform distribution, get particle position
for i in range(n_samples):
    time = np.random.uniform(low=0, high=period)
    x_i = x(time, A, omega)
    x_sampled.append(x_i)

x_sampled = np.asarray(x_sampled)

# probability density function of position
hist, coords = np.histogram(x_sampled, bins=10000, normed=True)

# recenter bins
binwidth = (coords[1]-coords[0])
halfbinwidth = 0.5 * binwidth
bin_centers = coords + halfbinwidth

# energy = 0.5 * k * x^2
# <energy> \propto int(x^2 * p(x))
integral = np.trapz(bin_centers[:-1]**2 * hist, dx=binwidth)
print('mean of energy = ', integral)

x_2_sampled = x_sampled**2
print('mean of x = ', np.mean(x_sampled))
print('mean of x2 = ', np.mean(x_2_sampled))

# print histogram
for c, h in zip(coords, hist):
    print c+halfbinwidth, h 
