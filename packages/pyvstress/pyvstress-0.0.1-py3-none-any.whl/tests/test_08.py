# import sys
# from pathlib import Path
# import numpy as np

# module_path = Path(r"../pyvstress/")
# module_path = module_path.resolve()
# sys.path.append(str(module_path))

from pyvstress import SoilLayer, SoilProfile
import pyvstress.utility_functions as utf


# Description: Test calculation generation of depths for vertical stress in soil profile
# and for lateral earth pressure diagram


def lateral_earth_pressure_pts(soilprofile, deltah=1e-7):
    """Points for computing lateral earth pressures.
    Generate two points at all interior layer boundaries, one point at the top of the soil profile,
    and one point at the bottom of the soil profile. If the groundwater table is at the layer boundary
    then no additional points are required, but if the groundwater table is within a layer then add an
    additional point at the depth of the groundwater table.

    Two point at interior layer boundaries are required because the top layer and the bottom layer will
    have different values of phi  and c resulting in different lateral streses

    :param soilprofile: SoilProfile object with a list of SoilLayer objects

    :param deltah: float, a tolerance quantity to push the point into the next layer. If the point lies on
    a layer boundary then it will belong to the top layer, so z+deltah will push the point at the same depth
    to the bottom layer if the layer boundary is at depth z.
    """
    ztops = soilprofile._ztops_0
    zbots = soilprofile._zbots_0
    zw = soilprofile.zw

    zinter = [(ztop, ztop + deltah) for ztop in ztops[1:]]
    zs = [ztops[0]] + [z for val in zinter for z in val] + [zbots[-1]]
    if not any([abs(z - zw) < 0.01 for z in (ztops)]):
        zs = zs + [zw]
        zs.sort()
    return zs


def test_vertical_stress_depths_01():
    # testing depths generated for drawing the vertical stresses for the soil profile
    # one point for the top of the soil profile, one at each of the layer boundaries,
    # one at the bottom of the soil profile.
    # if the water table is at one of the layer boundaries no futher action is needed
    # if water table is within a layer then add one more point for the water table
    # water table at one of the boundaries

    # soillayers
    layer1 = SoilLayer(5, 110, 120, phi=26, c=100)
    layer2 = SoilLayer(7, 115, 125, phi=28, c=100)
    layer3 = SoilLayer(4, 115, 122, phi=30, c=0)
    layer4 = SoilLayer(1, 112, 120, phi=25, c=25)
    layer5 = SoilLayer(10, 125, 135, phi=35, c=0)
    layers = [layer1, layer2, layer3, layer4, layer5]

    # soil profile
    soilprofile = SoilProfile(layers, zw=0.0, q=0, gammaw=62.4)

    # depths for vertical stresses in a soil profile
    pts = utf.stress_profile_points(soilprofile)

    results = [pt.z for pt in pts]

    required_results = [0, 5, 12, 16, 17, 27]

    assert results == required_results


def test_lateral_earth_pressure_depths_01():
    # testing points generated for drawing the lateral earth pressure, two point at every
    # layer boundary except at groundwater table depth if the groundwater table lies within a layer,
    # and the soilprofile top and soilprofile bottom.
    # groundwater at one of the layer boundaries

    # soillayers
    layer1 = SoilLayer(5, 110, 120, phi=26, c=100)
    layer2 = SoilLayer(7, 115, 125, phi=28, c=100)
    layer3 = SoilLayer(4, 115, 122, phi=30, c=0)
    layer4 = SoilLayer(1, 112, 120, phi=25, c=25)
    layer5 = SoilLayer(10, 125, 135, phi=35, c=0)
    layers = [layer1, layer2, layer3, layer4, layer5]

    # soil profile
    soilprofile = SoilProfile(layers, zw=0.0, q=0, gammaw=62.4)
    # generate points for lateral earth pressure points
    pts = utf.stress_profile_points(soilprofile, "lateral")
    results = [pt.z for pt in pts]

    required_results = [0, 5.0, 5.0, 12.0, 12.0, 16.0, 16.0, 17.0, 17.0, 27.0]

    assert results == required_results


def test_vertical_stress_depths_02():
    # testing depths generated for drawing the vertical stresses for the soil profile
    # one point for the top of the soil profile, one at each of the layer boundaries,
    # one at the bottom of the soil profile.
    # if the water table is at one of the layer boundaries no futher action is needed
    # if water table is within a layer then add one more point for the water table
    # watertable with a layer

    # soillayers
    layer1 = SoilLayer(5, 110, 120, phi=26, c=100)
    layer2 = SoilLayer(7, 115, 125, phi=28, c=100)
    layer3 = SoilLayer(4, 115, 122, phi=30, c=0)
    layer4 = SoilLayer(1, 112, 120, phi=25, c=25)
    layer5 = SoilLayer(10, 125, 135, phi=35, c=0)
    layers = [layer1, layer2, layer3, layer4, layer5]

    # soil profile
    soilprofile = SoilProfile(layers, zw=16.5, q=0, gammaw=62.4)

    # depths for vertical stresses in a soil profile
    pts = utf.stress_profile_points(soilprofile)

    results = [pt.z for pt in pts]

    required_results = [0.0, 5.0, 12.0, 16.0, 16.5, 17.0, 27.0]

    assert results == required_results


def test_lateral_earth_pressure_depths_02():
    # testing points generated for drawing the lateral earth pressure, two point at every
    # layer boundary except at groundwater table depth if the groundwater table lies within a layer,
    # and the soilprofile top and soilprofile bottom.
    # groundwater within one of the layers

    # soillayers
    layer1 = SoilLayer(5, 110, 120, phi=26, c=100)
    layer2 = SoilLayer(7, 115, 125, phi=28, c=100)
    layer3 = SoilLayer(4, 115, 122, phi=30, c=0)
    layer4 = SoilLayer(1, 112, 120, phi=25, c=25)
    layer5 = SoilLayer(10, 125, 135, phi=35, c=0)
    layers = [layer1, layer2, layer3, layer4, layer5]

    # soil profile
    soilprofile = SoilProfile(layers, zw=16.5, q=0, gammaw=62.4)

    pts = utf.stress_profile_points(soilprofile, "lateral")

    results = [pt.z for pt in pts]

    required_results = [0, 5.0, 5.0, 12.0, 12.0, 16.0, 16.0, 16.5, 17.0, 17.0, 27.0]

    assert results == required_results
