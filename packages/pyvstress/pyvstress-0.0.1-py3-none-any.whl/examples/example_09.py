import numpy as np
from pyvstress import Point, SoilLayer, SoilProfile

# Description: The profile_lateral_earth_pressures(), is only for lateral earth pressure profile
# but if we want at other locations then we will have to get the parameters from the soil layers
# and write the function to compute lateral stresses.
# Steps
# 1) Create soil profile. Provided both c and phi, if both c and phi are to be used to calculate
# lateral stresses. If c = 0, then provide c = 0.
# 2) Create Point instances at the required depths. We will not place our points at layer boundaries
# because at layer boundaries we would need two points for lateral stresses. If points at layer
# boundaries are required then use stress_profile_points(soil_profile,analysis_type="lateral") and then
# maybe add your other points too and sort them. This one maybe for a lateral example.
# 3) Extract the value of c and phi at the locations of the points.
# 4) Once you have the points and the required parameters at those points then custom functions
# can be written for any further analysis


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


def main():
    # Create layers with optional arguments for lateral earth pressure calculations
    layer1 = SoilLayer(5, 100, 110, phi=26, c=50)
    layer2 = SoilLayer(10, 110, 120, phi=30, c=0)
    layer3 = SoilLayer(7, 120, 130, phi=34, c=0)
    layers = [layer1, layer2, layer3]

    # create soil profile, with watertable at 5 feet from the ground surface and surcharge
    soilprofile = SoilProfile(layers, zw=6.0, q=250, gammaw=62.4)

    # depth at which to calculate vertical and lateral stresses
    # again do not choose layer boundaries for lateral earth pressures
    # but if you are only interested in vertical stresses then it is alright to choose layer
    # boundaries depths
    # the second layer will be subdivided into two layers at the groundwater level but that ok
    # because both the layers obove and below that boundary have the same parameters so one pont
    # at that boundary is alright
    zs = [0, 3.0, 6.0, 10.0, 16.0, 20.0, 22.0]

    # convert the depth to points
    pts = [Point(z) for z in zs]

    # compute vertical total stress, porewater pressure, and effective stresses
    soilprofile.vertical_stresses(pts)

    # if you are only interested in vertical stresses then you can view them
    # for pt in pts:
    #     print(pt.z, pt.total_stress, pt.pore_pressure, pt.effective_stress)
    # and if you want it as an numpy aarray
    vstresses = np.asarray(
        [[pt.z, pt.total_stress, pt.pore_pressure, pt.effective_stress] for pt in pts]
    )

    # next step is extract layer parameters at those points
    # we require c and phi for lateral earth pressures and we have supplied c and phi as
    # layer parameters. The parameter names must match and every layer should be given those
    # parameters even if the value of the parameter is 0, e.g. if c = 0, you need to initialize
    # soil layer with c = 0.
    keylist = ["c", "phi"]
    params = soilprofile.get_params(pts, keylist)
    # params is a list, convert into numpy array, the shape of params will be (7,2), seven rowws
    # for the seven points and two columns for the two parameters
    params = np.asarray(params)

    # now use custom functions to perform further analysis in this case we will
    # calculate lateral earth pressure, active and passive pressure at each of those depths
    # initialize the lateral earth pressure array for depth, active and passive pressure
    latstresses = np.zeros((vstresses.shape[0], 3))
    # the first column are the depths of the points
    latstresses[:, 0] = vstresses[:, 0]
    # the second column is the active earth pressure values at those points
    latstresses[:, 1] = calc_active_earth_pressure(
        vstresses[:, 3], params[:, 0], params[:, 1]
    )
    # the third column is the passive earth pressure values at those points
    latstresses[:, 2] = calc_passive_earth_pressure(
        vstresses[:, 3], params[:, 0], params[:, 1]
    )

    print("Vertical stresses:")
    print(
        f"{'z':>5s}, {'Total stress':>15s}, {'Pore press.':>15s}, {'Eff. stress':>15s}"
    )
    for vstress in vstresses:
        print(
            f"{vstress[0]:>5.2f}, {vstress[1]:>15.2f}, {vstress[2]:>15.2f}, {vstress[3]:>15.2f}"
        )

    print("Lateral stresses:")
    print(
        f"{'z':>5s}, {'Active Pressure':>15s}, {'Passive Pressure':>15s}"
    )
    for latstress in latstresses:
        print(
            f"{latstress[0]:>5.2f}, {latstress[1]:>15.2f}, {latstress[2]:>15.2f}"
        )

if __name__ == "__main__":
    main()
