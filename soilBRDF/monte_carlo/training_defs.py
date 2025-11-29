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

import numpy as np
from scipy.differentiate import derivative

def calc_wavelength_BRDF(incoming_light_angle, viewing_angle, azimuthal_angle):
    """
        Notes
        - This function returns pi times the actual BRDF, and is dimensionless.
        - F_lambda: approximated, as it lies between 1361 and 1370 W/m^2
    """
    F_lambda = 1365                     # W/m^2
    theta_0 = incoming_light_angle      # Radians
    theta = viewing_angle               # Radians
    phi = azimuthal_angle               # Radians
    I_lambda = calc_measured_intensity(theta_0, theta, phi)  # Watts
    mu_0 = np.cos(theta_0)
    return (np.pi * I_lambda) / (mu_0 * F_lambda)

def calc_measured_intensity(incoming_light_angle, viewing_angle, azimuthal_angle):
    F_lambda = 1365                     # W/m^2
    theta_0 = incoming_light_angle      # Radians
    theta = viewing_angle               # Radians
    phi = azimuthal_angle               # Radians
    return 1

def calc_point_lambertian_intensity(incoming_light_angle, viewing_angle, azimuthal_angle, soil_shape_function, x_point):
    shape_func = soil_shape_function
    dy_dx = derivative(shape_func, x_point)
    H = ((dy_dx['df']) ** 2 + 1) ** 0.5
    if H == 0:
        vartheta = 0
    elif dy_dx['df'] > 0:
        vartheta = np.arccos(1/H)
    else:
        vartheta = -np.arccos(1/H)
    
    adjusted_incident_angle = incoming_light_angle + vartheta
    adjusted_viewing_angle = viewing_angle + vartheta
    return (np.sin(adjusted_incident_angle) * np.sin(adjusted_viewing_angle))

def soil_shape_function(x):
    return np.sin(x)

print(calc_point_lambertian_intensity(
    incoming_light_angle    = np.pi/4,
    viewing_angle           = np.pi/3,
    azimuthal_angle         = 1,
    soil_shape_function     = soil_shape_function,
    x_point                 = 0
    ))
