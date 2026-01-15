"""
Functions for the Monte-Carlo simulations of BRDF
"""

"""
    Reflectance will be measured with a set x and y axis.
        Light from directly above the soil will have angle 0, and horizontal would
        be +pi/2 and -pi/2
        Viewing zenith angle will be measured similarly
        Incoming light angle will most likely be solar zenith angle

    Paper: https://ntrs.nasa.gov/api/citations/20080023443/downloads/20080023443.pdf

    BRDF = dL_r(theta_i, phi_i, theta_r, phi_r; E_i) / dE_i(theta_i, phi_i)

    BRDF = (P_r/omega) / (P_i * cos(theta_r))
        P_r reflected detected radiant power
        omega solid angle
        P_i incident total radiant power
        theta_r reflected zenith angle

    omega = A/(R^2)
        A is the area of detector aperture
        R is the radius from the sample to the detector

    Spectral BRDF R_lambda
    R_lambda(theta, theta_0, phi) = (pi * I_lambda(theta, theta_0, phi)) / (mu_0 * F_lambda)
        I_lambda is measured intensity
        F_lambda is solar flux density on top of atmosphere
            This is a constant. Generally 1361-1370 W/m^2
        theta is viewing zenith angle
        theta_0 is incident zenith angle
        phi is azimuthal angle between viewing and incidental light
        mu_0 is cos(theta_0)

    This R_lambda is equal to BRDF times pi.

    To get soil reflectances, will use a perfect soil sample from csv files.
"""

# Assumptions:
"""
    - Viewing angle is the same for all points; detector is sufficiently far away to neglect small angle changes
"""

import numpy as np
from scipy.differentiate import derivative


def calc_wavelength_BRDF(incoming_light_angle, received_intensity: list):
    """
        Notes
        - This function returns pi times the actual BRDF, and is dimensionless.
        - F_lambda: approximated, as it lies between 1361 and 1370 W/m^2
    """
    F_lambda = 1365                     # W/m^2
    theta_0 = incoming_light_angle      # Radians
    # theta = viewing_angle               # Radians
    # phi = azimuthal_angle               # Radians
    I_lambda = calc_measured_intensity(received_intensity)  # Watts
    mu_0 = np.cos(theta_0)
    return (np.pi * I_lambda) / (mu_0 * F_lambda)


def calc_measured_intensity(received_intensity: list):
    return sum(received_intensity)/len(received_intensity)


def calc_point_measured_intensity(viewing_angle, incoming_intensity, soil_shape_function, x_point):
    theta = viewing_angle               # Radians
    lambert_multiplier = calc_point_lambertian_multiplier(viewing_angle=theta, 
                                                          soil_shape_function=soil_shape_function, 
                                                          x_point=x_point)
    # Calculate incoming intensity by lambert's cosine law.
    return incoming_intensity * lambert_multiplier


def calc_point_lambertian_multiplier(viewing_angle, soil_shape_function, x_point):
    shape_func = soil_shape_function
    dy_dx = derivative(shape_func, x_point)
    # New angle will be the 'angle' of the new plane compared to the horizontal axis.
    # i.e. arctan of dy/dx divided by 1.
    varphi = np.arctan(dy_dx['df'])
    vartheta = viewing_angle + varphi

    # Calculate intensity multiplier by Lambert's cosine law
    # Intention: Received intensity will be the product of I_0 and this multiplier
    # Note: Need value to be positive. If the value is negative, return 0.
    if np.cos(vartheta) < 0:
        return 0
    else:
        return np.cos(vartheta)

"""
def soil_shape_function(x):
    # Will only consider soil shapes that do not go vertical.
    # such that a derivative exists.
    return np.sin(x)
"""

def ray_trace(incoming_angle, soil_shape_function, x_max, y_i, x_i):
    """
        This function returns the x-value of where the light first interacts with the surface, if it interacts
            - Bool: True if interacts, False if out of bounds

        x_max is the maximum absolute distace from 0 that the soil shape considers. (positive)
        For these purposes, maybe x_max = 1 meter.

        y_i is the origin of the ray in the y-axis, usually somewhere far away.
        x_i is the origin of the ray in the x-axis.
    """
    # 3 possibilities: Angle is positive or negative, or 0
    dx = 0.1
    x_max = abs(x_max)
    x = x_i

    if incoming_angle == 0:
        return True, x
    elif incoming_angle > 0:
        # Positive
        dx = -dx
        dy_dx = 1/(np.arctan(incoming_angle))
    else:
        # Negative
        dx = dx
        dy_dx = -1/(np.arctan(incoming_angle))
        
    while abs(x) <= x_max:
        y_check = y_i + (dy_dx * (abs(x)-x_i))
        if y_check <= soil_shape_function(x):
            return True, x
        x += dx
    return False, 0

# print(ray_trace(
#     incoming_angle=np.pi/4, soil_shape_function=soil_shape_function, x_max=2, y_i = 1, x_i=1
# ))

# print(calc_point_measured_intensity(
#     viewing_angle           = 1,
#     incoming_intensity      = 1,
#     soil_shape_function     = soil_shape_function,
#     x_point                 = 0
#     ))
