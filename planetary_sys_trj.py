from scipy.optimize import fsolve
import math
import numpy as np

# write xyz file of trajectory of planets
# moving around the sun in the xy plane

# Kepler's laws
# 1. path of planets around sun is ellipse, sun at one focus
# 2. sun-planet line sweeps out equal areas in equal times
# 3. T_a^2/T_b^2 = d_a^3/d_b^3, T = period, d = average distance from sun

# solutions of equations of motion:
# https://en.wikipedia.org/wiki/Kepler's_laws_of_planetary_motion#Position_as_a_function_of_time

# data for planetary orbits
# https://www.windows2universe.org/our_solar_system/planets_orbits_table.html
# Planet Period (in years), Average Distance from the sun (in astronomical units), eccentricity 
planets = {
 'Mercury': {'period': 0.241, 'semimajor_axis': 0.39,  'eccentricity': 0.206, 'symbol': 1},
 'Venus':   {'period': 0.615, 'semimajor_axis': 0.72,  'eccentricity': 0.007, 'symbol': 2},
 'Earth':   {'period': 1.000, 'semimajor_axis': 1.00,  'eccentricity': 0.017, 'symbol': 3},
 'Mars':    {'period': 1.88,  'semimajor_axis': 1.53,  'eccentricity': 0.093, 'symbol': 4},
 'Jupiter': {'period': 11.9,  'semimajor_axis': 5.20,  'eccentricity': 0.048, 'symbol': 5},
 'Saturn':  {'period': 29.5,  'semimajor_axis': 9.54,  'eccentricity': 0.056, 'symbol': 6},
 'Uranus':  {'period': 84,    'semimajor_axis': 19.19, 'eccentricity': 0.046, 'symbol': 7},
 'Neptune': {'period': 165,   'semimajor_axis': 30.06, 'eccentricity': 0.010, 'symbol': 8},
 'Pluto':   {'period': 248,   'semimajor_axis': 39.53, 'eccentricity': 0.248, 'symbol': 9},
 #'Moon':    {'period': 27/365,'semimajor_axis': 0.0026,'eccentricity': 0.0549, 'symbol': 1}}  # approx!
 'Moon':    {'period': 27/365,'semimajor_axis': 0.26,'eccentricity': 0.0549, 'symbol': 1}}  # approx!

rescale_factor = 40  # rescale for visualisation in vmd


def main():

    # # xyz file of the trajectory of planets in the referentiel of the sun
    # planets_to_print = ['Mercury', 'Venus', 'Earth', 'Mars']
    # n_earth_years = 10  
    # xyz_sun_and_planets(planets_to_print, n_earth_years)

    # xyz file of the trajectory of planets in the referentiel of the sun
    n_earth_years = 10  
    xyz_earth_moon_sun(n_earth_years)


def xyz_earth_moon_sun(n_earth_years):
    '''output an xyz file of the trajectory of the earth and
    the moon in the referentiel of the sun

    Length of trajectory: n_earth_years

    Supposes moon-earth and earth-sun orbits are in same plane'''

    nbodies = 3

    xyzfile = open('earth_moon_sun.xyz', 'w')

    # loop over time in units of earth year
    start = 0.0
    stop = n_earth_years
    step = 0.005
    for t in np.arange(start, stop, step):

        # print xyz file header
        xyzfile.write(str(nbodies)+'\n')
        xyzfile.write('earth moon sun system\n')

        # print sun
        xyzfile.write('30 0.0 0.0 0.0\n')
        
        # earth in referentiel of sun
        symbol, x, y, z = get_coordinates('Earth', t)
        xyzfile.write('{} {} {} {}\n'.format(symbol, x*rescale_factor, y*rescale_factor, z))

        # moon in referentiel of earth
        symbol, x_moon, y_moon, z_moon = get_coordinates('Moon', t)
        x_moon, y_moon, z_moon = change_referentiel(x_moon, y_moon, z_moon, x, y, z)
        xyzfile.write('{} {} {} {}\n'.format(symbol, x_moon*rescale_factor, y_moon*rescale_factor, z_moon))

    xyzfile.close()
   

def xyz_sun_and_planets(planets_to_print, n_earth_years):
    '''output an xyz file of the trajectory of the planets
    listed in planets_to_print, in the referentiel of the sun

    Length of trajectory: n_earth_years'''

    nbodies = len(planets_to_print) + 1  # nplanets + the sun

    xyzfile = open('planets.xyz', 'w')

    # loop over time in units of earth year
    start = 0.0
    stop = n_earth_years
    step = 0.005
    for t in np.arange(start, stop, step):

        # print xyz file header
        xyzfile.write(str(nbodies)+'\n')
        xyzfile.write('planetary system\n')

        # print sun
        xyzfile.write('30 0.0 0.0 0.0\n')
        
        # loop over planets
        for planet_name in planets_to_print:

            symbol, x, y, z = get_coordinates(planet_name, t)
            xyzfile.write('{} {} {} {}\n'.format(symbol, x*rescale_factor, y*rescale_factor, z))

    xyzfile.close()


def get_coordinates(planet_name, t):
    '''get cartesian coordinates of planet at time t in
    referential defined in the dictionary planets'''

    period = planets[planet_name]['period']
    semimajor_axis = planets[planet_name]['semimajor_axis']
    eccentricity = planets[planet_name]['eccentricity']
    symbol = planets[planet_name]['symbol']
    
    r, theta = planetary_position(t, period, semimajor_axis, eccentricity)
    x, y = polar_to_cartesian_coordinates(r, theta)
    z = 0.0

    return symbol, x, y, z


def change_referentiel(x, y, z, x_ref, y_ref, z_ref):

    x += x_ref
    y += y_ref
    z += z_ref

    return x, y, z


def ecc_anomaly_equation(E, eccentricity, M):
    '''
    equation to be solved to get E when we know eccentricity and M

    E: eccentric anomaly
    eccentricity: eccentricity of ellipse
    M: mean anomaly
    M = E - eccentricity * sin(E)
    we solve for E
    '''
    f = E - eccentricity * math.sin(E) - M

    return f


def true_anomaly_equation(theta, eccentricity, E):
    '''
    equation to be solved to get theta when we know eccentricity and E

    E: eccentric anomaly
    eccentricity: eccentricity of ellipse
    theta: true anomaly
    (1 - eccentricity) * tan2(theta/2) = (1 + eccentricity) * tan2(E/2)
    we solve for theta
    '''
    f = (1 - eccentricity) * pow(math.tan(theta / 2), 2) - (1 + eccentricity) * pow(math.tan(E / 2), 2)

    return f


def planetary_position(t, period, semimajor_axis, eccentricity):
    '''
    Gets the position of a planet at time t, in polar coordinates
    with the sun at the origin

    t: time since perihelion
    perihelion: point when planet is closest to Sun
    P: period
    n: mean motion, n = 2*pi/P
    M: mean anomaly, M = n*t
    E: eccentric anomaly, M = E - eccentricity * sin(E)
    eccentricity: eccentricity of the ellipse, eccentricity = (rmax-rmin)/(rmax+rmin)
    semimajor_axis: average of rmin and rmax
    r: vector from sun to planet
    theta: angle between current r and r at perihelion
    '''

    # mean motion (rad / unit time)
    n = 2 * np.pi / period

    # mean anomaly (rad)
    M = n * t

    # eccentric anomaly
    if eccentricity < 0.8:  # rule of thumb for setting initial value
        initial_value = M
    else:
        initial_value = np.pi
    E = fsolve(ecc_anomaly_equation, initial_value, args=(eccentricity, M))[0]

    # check equation has been correctly solved
    if (abs(E - eccentricity * math.sin(E) - M) > 0.000001):
        print('Warning, problem with value of E')

    # true anomaly (theta)
    initial_value = E
    theta = fsolve(true_anomaly_equation, initial_value, args=(eccentricity, E))[0]

    # check equation has been correctly solved
    lhs = (1 - eccentricity) * pow(math.tan(theta / 2), 2)
    rhs = (1 + eccentricity) * pow(math.tan(E / 2), 2)
    if (abs(lhs - rhs) > 0.000001):
        print('Warning, problem with value of theta')

    # heliocentric distance
    r = semimajor_axis * (1 - eccentricity * math.cos(E))

    return r, theta


def polar_to_cartesian_coordinates(r, theta):
    x = r * math.cos(theta)
    y = r * math.sin(theta)
    return x, y
    

if __name__ == '__main__':
    main()
