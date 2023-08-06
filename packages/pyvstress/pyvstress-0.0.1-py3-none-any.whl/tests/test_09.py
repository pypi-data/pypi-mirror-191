# import sys
# from pathlib import Path

# module_path = Path(r"../pyvstress/")
# module_path = module_path.resolve()
# sys.path.append(str(module_path))

import numpy as np
from pyvstress import SoilLayer, SoilProfile
import pyvstress.utility_functions as utf

# Description: Tests same as test_07 but using utility functions
# Test calculation of total stress, pore pressure, and effective stress
# and Coulomb's lateral earth pressure


def test_profile_vertical_stresses_01():
    # testing: vertical stresses
    # watertable: on the surface

    # soillayers
    layer1 = SoilLayer(5, 110, 120, phi=26, c=100)
    layer2 = SoilLayer(7, 115, 125, phi=28, c=100)
    layer3 = SoilLayer(4, 115, 122, phi=30, c=0)
    layer4 = SoilLayer(1, 112, 120, phi=25, c=25)
    layer5 = SoilLayer(10, 125, 135, phi=35, c=0)
    layers = [layer1, layer2, layer3, layer4, layer5]

    # soil profile
    soilprofile = SoilProfile(layers, zw=0, q=0, gammaw=62.4)
    results = utf.profile_vertical_stresses(soilprofile)
    results = np.round(results, 1).tolist()

    # required results
    required_results = [
        [0.0, 0.0, 0.0, 0.0],
        [5.0, 600.0, 312.0, 288.0],
        [12.0, 1475.0, 748.8, 726.2],
        [16.0, 1963.0, 998.4, 964.6],
        [17.0, 2083.0, 1060.8, 1022.2],
        [27.0, 3433.0, 1684.8, 1748.2],
    ]

    assert results == required_results


def test_profile_lateral_earth_pressures_01():
    # testing: vertical stresses and lateral stresses.
    # watertable: on the surface

    # soillayers
    layer1 = SoilLayer(5, 110, 120, phi=26, c=100)
    layer2 = SoilLayer(7, 115, 125, phi=28, c=100)
    layer3 = SoilLayer(4, 115, 122, phi=30, c=0)
    layer4 = SoilLayer(1, 112, 120, phi=25, c=25)
    layer5 = SoilLayer(10, 125, 135, phi=35, c=0)
    layers = [layer1, layer2, layer3, layer4, layer5]

    # soil profile
    soilprofile = SoilProfile(layers, zw=0, q=0, gammaw=62.4)
    (vstress, latstress) = utf.profile_lateral_earth_pressures(soilprofile)
    results = np.c_[vstress, latstress[:, 1:]]
    results = np.round(results, 1).tolist()

    # required results
    required_results = [
        [0.0, 0.0, 0.0, 0.0, -125.0, 320.1],
        [5.0, 600.0, 312.0, 288.0, -12.5, 1057.7],
        [5.0, 600.0, 312.0, 288.0, -16.2, 1130.6],
        [12.0, 1475.0, 748.8, 726.2, 142.0, 2344.3],
        [12.0, 1475.0, 748.8, 726.2, 242.1, 2178.6],
        [16.0, 1963.0, 998.4, 964.6, 321.5, 2893.8],
        [16.0, 1963.0, 998.4, 964.6, 359.6, 2455.2],
        [17.0, 2083.0, 1060.8, 1022.2, 383.0, 2597.1],
        [17.0, 2083.0, 1060.8, 1022.2, 277.0, 3772.1],
        [27.0, 3433.0, 1684.8, 1748.2, 473.7, 6451.2],
    ]

    assert results == required_results


def test_profile_vertical_stresses_02():
    # testing: vertical stresses and lateral stresses
    # watertable: 5.0 ft from the ground surface.

    # soillayers
    layer1 = SoilLayer(5, 110, 120, phi=26, c=100)
    layer2 = SoilLayer(7, 115, 125, phi=28, c=100)
    layer3 = SoilLayer(4, 115, 122, phi=30, c=0)
    layer4 = SoilLayer(1, 112, 120, phi=25, c=25)
    layer5 = SoilLayer(10, 125, 135, phi=35, c=0)
    layers = [layer1, layer2, layer3, layer4, layer5]

    # soil profile
    soilprofile = SoilProfile(layers, zw=5, q=0, gammaw=62.4)
    # vertical stresses with depth
    results = utf.profile_vertical_stresses(soilprofile)
    results = np.round(results, 1).tolist()

    # required results
    required_results = [
        [0.0, 0.0, 0.0, 0.0],
        [5.0, 550.0, 0.0, 550.0],
        [12.0, 1425.0, 436.8, 988.2],
        [16.0, 1913.0, 686.4, 1226.6],
        [17.0, 2033.0, 748.8, 1284.2],
        [27.0, 3383.0, 1372.8, 2010.2],
    ]

    assert results == required_results


def test_profile_lateral_earth_pressure_02():
    # testing: vertical stresses and lateral stresses
    # watertable: 5.0 ft from the ground surface.

    # soillayers
    layer1 = SoilLayer(5, 110, 120, phi=26, c=100)
    layer2 = SoilLayer(7, 115, 125, phi=28, c=100)
    layer3 = SoilLayer(4, 115, 122, phi=30, c=0)
    layer4 = SoilLayer(1, 112, 120, phi=25, c=25)
    layer5 = SoilLayer(10, 125, 135, phi=35, c=0)
    layers = [layer1, layer2, layer3, layer4, layer5]

    # soil profile
    soilprofile = SoilProfile(layers, zw=5, q=0, gammaw=62.4)

    # points for lateral earth pressure calculations
    (vstress, latstress) = utf.profile_lateral_earth_pressures(soilprofile)
    results = np.c_[vstress, latstress[:, 1:]]
    results = np.round(results, 1).tolist()

    # required results
    required_results = [
        [0.0, 0.0, 0.0, 0.0, -125.0, 320.1],
        [5.0, 550.0, 0.0, 550.0, 89.8, 1728.7],
        [5.0, 550.0, 0.0, 550.0, 78.4, 1856.3],
        [12.0, 1425.0, 436.8, 988.2, 236.6, 3070.0],
        [12.0, 1425.0, 436.8, 988.2, 329.4, 2964.6],
        [16.0, 1913.0, 686.4, 1226.6, 408.9, 3679.8],
        [16.0, 1913.0, 686.4, 1226.6, 466.0, 3100.7],
        [17.0, 2033.0, 748.8, 1284.2, 489.3, 3242.6],
        [17.0, 2033.0, 748.8, 1284.2, 348.0, 4738.9],
        [27.0, 3383.0, 1372.8, 2010.2, 544.7, 7418.0],
    ]

    assert results == required_results


def test_profile_vertical_stresses_03():
    # testing: vertical stresses with depth
    # water table: 16.5 ft depth from the surface

    # soillayers
    layer1 = SoilLayer(5, 110, 120, phi=26, c=100)
    layer2 = SoilLayer(7, 115, 125, phi=28, c=100)
    layer3 = SoilLayer(4, 115, 122, phi=30, c=0)
    layer4 = SoilLayer(1, 112, 120, phi=25, c=25)
    layer5 = SoilLayer(10, 125, 135, phi=35, c=0)
    layers = [layer1, layer2, layer3, layer4, layer5]

    # soil profile
    soilprofile = SoilProfile(layers, zw=16.5, q=0, gammaw=62.4)

    # vertical stresses with depth
    results = utf.profile_vertical_stresses(soilprofile)
    results = np.round(results, 1).tolist()

    # required results
    required_results = [
        [0.0, 0.0, 0.0, 0.0],
        [5.0, 550.0, 0.0, 550.0],
        [12.0, 1355.0, 0.0, 1355.0],
        [16.0, 1815.0, 0.0, 1815.0],
        [16.5, 1871.0, 0.0, 1871.0],
        [17.0, 1931.0, 31.2, 1899.8],
        [27.0, 3281.0, 655.2, 2625.8],
    ]

    assert results == required_results


def test_profile_lateral_earth_pressures_03():
    # testing: vertical stresses and lateral stresses
    # water table: 16.5 ft depth from the surface

    # soillayers
    layer1 = SoilLayer(5, 110, 120, phi=26, c=100)
    layer2 = SoilLayer(7, 115, 125, phi=28, c=100)
    layer3 = SoilLayer(4, 115, 122, phi=30, c=0)
    layer4 = SoilLayer(1, 112, 120, phi=25, c=25)
    layer5 = SoilLayer(10, 125, 135, phi=35, c=0)
    layers = [layer1, layer2, layer3, layer4, layer5]

    # soil profile
    soilprofile = SoilProfile(layers, zw=16.5, q=0, gammaw=62.4)

    # vertical and lateral earth pressurs with depth
    (vstress, latstress) = utf.profile_lateral_earth_pressures(soilprofile)
    results = np.c_[vstress, latstress[:, 1:]]
    results = np.round(results, 1).tolist()

    # required results
    required_results = [
        [0.0, 0.0, 0.0, 0.0, -125.0, 320.1],
        [5.0, 550.0, 0.0, 550.0, 89.8, 1728.7],
        [5.0, 550.0, 0.0, 550.0, 78.4, 1856.3],
        [12.0, 1355.0, 0.0, 1355.0, 369.0, 4086.0],
        [12.0, 1355.0, 0.0, 1355.0, 451.7, 4065.0],
        [16.0, 1815.0, 0.0, 1815.0, 605.0, 5445.0],
        [16.0, 1815.0, 0.0, 1815.0, 704.8, 4550.5],
        [16.5, 1871.0, 0.0, 1871.0, 727.5, 4688.5],
        [17.0, 1931.0, 31.2, 1899.8, 739.2, 4759.4],
        [17.0, 1931.0, 31.2, 1899.8, 514.8, 7010.6],
        [27.0, 3281.0, 655.2, 2625.8, 711.6, 9689.7],
    ]

    assert results == required_results


def test_profile_vertical_stresses_04():
    # testing: vertical stresses with depth
    # water table: 16.5 ft depth
    # surchage: 250 psf

    # soillayers
    layer1 = SoilLayer(5, 110, 120, phi=26, c=100)
    layer2 = SoilLayer(7, 115, 125, phi=28, c=100)
    layer3 = SoilLayer(4, 115, 122, phi=30, c=0)
    layer4 = SoilLayer(1, 112, 120, phi=25, c=25)
    layer5 = SoilLayer(10, 125, 135, phi=35, c=0)
    layers = [layer1, layer2, layer3, layer4, layer5]

    # soil profile
    soilprofile = SoilProfile(layers, zw=16.50, q=250, gammaw=62.4)

    # vertical stresses with depth
    results = utf.profile_vertical_stresses(soilprofile)
    results = np.round(results, 1).tolist()

    # required results
    required_results = [
        [0.0, 250.0, 0.0, 250.0],
        [5.0, 800.0, 0.0, 800.0],
        [12.0, 1605.0, 0.0, 1605.0],
        [16.0, 2065.0, 0.0, 2065.0],
        [16.5, 2121.0, 0.0, 2121.0],
        [17.0, 2181.0, 31.2, 2149.8],
        [27.0, 3531.0, 655.2, 2875.8],
    ]

    assert results == required_results


def test_profile_lateral_earth_pressures_04():
    # testing: vertical stresses and lateral stresses
    # water table: 16.5 ft depth
    # surchage: 250 psf

    # soillayers
    layer1 = SoilLayer(5, 110, 120, phi=26, c=100)
    layer2 = SoilLayer(7, 115, 125, phi=28, c=100)
    layer3 = SoilLayer(4, 115, 122, phi=30, c=0)
    layer4 = SoilLayer(1, 112, 120, phi=25, c=25)
    layer5 = SoilLayer(10, 125, 135, phi=35, c=0)
    layers = [layer1, layer2, layer3, layer4, layer5]

    # soil profile
    soilprofile = SoilProfile(layers, zw=16.50, q=250, gammaw=62.4)

    # vertical and lateral earth pressurs with depth
    (vstress, latstress) = utf.profile_lateral_earth_pressures(soilprofile)
    results = np.c_[vstress, latstress[:, 1:]]
    results = np.round(results, 1).tolist()

    # required results
    required_results = [
        [0.0, 250.0, 0.0, 250.0, -27.4, 960.3],
        [5.0, 800.0, 0.0, 800.0, 187.4, 2368.9],
        [5.0, 800.0, 0.0, 800.0, 168.7, 2548.7],
        [12.0, 1605.0, 0.0, 1605.0, 459.3, 4778.4],
        [12.0, 1605.0, 0.0, 1605.0, 535.0, 4815.0],
        [16.0, 2065.0, 0.0, 2065.0, 688.3, 6195.0],
        [16.0, 2065.0, 0.0, 2065.0, 806.2, 5166.5],
        [16.5, 2121.0, 0.0, 2121.0, 829.0, 5304.4],
        [17.0, 2181.0, 31.2, 2149.8, 840.7, 5375.4],
        [17.0, 2181.0, 31.2, 2149.8, 582.6, 7933.1],
        [27.0, 3531.0, 655.2, 2875.8, 779.3, 10612.2],
    ]

    assert results == required_results
