import numpy as np
import math
from .exceptions import ParamError
from .soil import Point


def check_required(obj, list_params):
    """Check if given parameters are supplied to an object, if all the required parameters are found return True else raise an error.
    ref: https://github.com/eng-tools/geofound/blob/master/geofound/models.py
    obj: object of the class for which to check for the list of parameters
    list_params: list of strings, a list of required parameters
    """
    for param in list_params:
        if not hasattr(obj, param):
            raise ParamError(
                "Parameter {} must be set for {} object".format(
                    param, obj.__class__.__name__
                )
            )
    return True


def calc_rankine_ka(phi):
    """Compute Rankines active earth pressure coefficient
    :param phi: float, Mohr-Coulomb phi parameter"""
    return np.tan(np.radians(45 - phi / 2)) ** 2


def calc_rankine_kp(phi):
    """Compute Rankines passive earth pressure coefficient
    :param c: float, Mohr-Coulomb c parameter"""
    return np.tan(np.radians(45 + phi / 2)) ** 2


def calc_active_earth_pressure(sigma, phi, c):
    """Active earth pressure using both phi and c
    :param sigma: float effective stress
    :param phi: Mohr-Coulomb phi parameter
    :param c: Mohr-Coulomb c parameter"""
    ka = calc_rankine_ka(phi)
    return sigma * ka - 2 * c * np.sqrt(ka)


def calc_passive_earth_pressure(sigma, phi, c):
    """Passive earth pressure using both phi and c
    :param sigma: float effective stress
    :param phi: Mohr-Coulomb phi parameter
    :param c: Mohr-Coulomb c parameter"""

    kp = calc_rankine_kp(phi)
    return sigma * kp + 2 * c * np.sqrt(kp)


def stress_profile_points(soil_profile, analysis_type="vertical"):
    """Returns points for computing vertical stresses / lateral earth pressures for the soil profile.

    :param SoilProfile soil_profile: SoilProfile object
    :param str analysis_type: either "vertical" or  "lateral"
        vertical: assigns a point at the soil profile top, one point each at the layer boundaries, at
        the groundwater table if it is not the same as one of the layer boundaries, and one at the bottom
        of the soil profile.
        lateral: assigns a pont at the soil profile top, two points at each of the layer boundaries, a
        point at the groundwater table if it is not one of the layer boundaries, and one point at the bottom
        of the soil profile. Two points at the interior layer boundaries are required because the top layer and
        the bottom layer have different values of `phi` and `c`, which will result in different lateral stresses.
    """

    # abs to prevent -0.000 after subtracting delta_z and rounding
    ptts = [Point(z) for z in soil_profile._ztops_0]
    ptbs = [Point(z) for z in soil_profile._zbots_0]

    # these are points that fall on the top layer of the layer boundary
    for pt in ptts:
        soil_profile.assign_layer_index(pt)

    # these are points that fall on the bottom layer of the layer boundary
    for pt in ptbs:
        soil_profile.assign_layer_index(pt)

    if analysis_type == "vertical":
        # one point at the top of the profile, layer boundaries, bottom of the profile
        pts = ptts + [ptbs[-1]]
    elif analysis_type == "lateral":
        # reduce the index for all the points excepth the surface point
        for pt in ptts[1:]:
            pt.layer_index -= 1
        # combine the points on either side of the layer boundary
        pts = ptts + ptbs
    else:
        raise ValueError(
            f"{analysis_type} is not one of the acceptable arguments: 'vertical' or 'lateral' "
        )

    # add a point for the watertable if it is not one of the layer boundaries
    if not any([abs(pt.z - soil_profile.zw) < 0.01 for pt in pts]):
        ptz = Point(soil_profile.zw)
        soil_profile.assign_layer_index(ptz)
        pts.append(ptz)

    # sort the points per depth and then layer_index
    pts.sort(key=lambda pt: (pt.z, pt.layer_index))

    return pts


def profile_vertical_stresses(soilprofile):
    """Return vertical stress with depth.

    :param soilprofile: SoilProfile instance"""

    pts = stress_profile_points(soilprofile)
    soilprofile.vertical_stresses(pts)

    return np.asarray(
        [[pt.z, pt.total_stress, pt.pore_pressure, pt.effective_stress] for pt in pts]
    )


def profile_lateral_earth_pressures(soilprofile, use_c=True):
    """Return lateral stresses with depth
    :param soilprofile: SoilProfile instance
    :param use_c: Boolean to indicate if Mohr-Coulomb c should be used in the calculation
    of lateral earth pressures. If False only phi parameter will be used."""

    # soil parameters required for calculating lateral earth pressures
    keylist = ["phi", "c"]

    pts = stress_profile_points(soilprofile, "lateral")

    soilprofile.vertical_stresses(pts)

    params = soilprofile.get_params(pts, keylist)
    params = np.asarray(params)
    if not use_c:
        params[:, 1] = 0

    vstress = np.asarray(
        [[pt.z, pt.total_stress, pt.pore_pressure, pt.effective_stress] for pt in pts]
    )

    latstress = np.zeros((vstress.shape[0], 3))
    latstress[:, 0] = vstress[:, 0]
    latstress[:, 1] = calc_active_earth_pressure(
        vstress[:, 3], params[:, 0], params[:, 1]
    )
    latstress[:, 2] = calc_passive_earth_pressure(
        vstress[:, 3], params[:, 0], params[:, 1]
    )

    return (vstress, latstress)


def generate_regular_points(soil_profile, analysis_type="vertical", dz=0.5):
    """Generate a list of points within the soil profile layer.

    Generate points, when possible, at equal intervals of dz.
    Points may not be dz apart near layer boundaries. Either one or two points
    are generated at internal layer boundaries based on whether the type of
    analysis involves vertical stresses, 1 point per boundary, or lateral stresses
    2 points per boundary.

    :param SoilProfile soilprofile: SoilProfile object
    :param float dz: maximum separation distance between points
    :param str analysis_type: type of analysis either 'vertical' or 'lateral'
    :returns: a list of Point objects, almost equally spaced over the soil profile
    :rtype: [Point]
    """

    # generate boundary points
    ptb = stress_profile_points(soil_profile, analysis_type)
    # depths and indices for interboundary points
    zs = []
    idxs = []
    for layer_idx, layer in enumerate(soil_profile.layers):
        npts = int(math.floor(layer.thickness / dz) - 1)
        zs += [(layer.ztop + (idx + 1) * dz) for idx in range(npts)]
        idxs += [layer_idx] * npts

    # inter boundary points
    pti = [Point(z=z, layer_index=idx) for z, idx in zip(zs, idxs)]
    # all the pionts
    pts = ptb + pti
    pts.sort(key=lambda pt: (pt.z, pt.layer_index))
    return pts
