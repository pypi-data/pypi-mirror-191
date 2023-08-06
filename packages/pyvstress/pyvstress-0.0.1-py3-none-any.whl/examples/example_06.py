# import sys
import numpy as np

# import random
import matplotlib.pyplot as plt
from pathlib import Path

# module_path = Path(r"../pyvstress/")
# module_path = module_path.resolve()
# sys.path.append(str(module_path))

# from soil import SoilLayer, SoilProfile
from pyvstress import SoilLayer, SoilProfile
import pyvstress.utility_functions as utf

# Description: lateral earth pressure over the depth of the profile and plot
# for a handcalcs version please check the notebooks folder


def add_marker_text(ax, results, x_idx):
    """Add text next to the markers"""

    if x_idx == 2:
        aligneff = ["left", "center"]
        alignt = ["right", "center"]
        deltas = [
            [-15, -5],
            [-25, 10],
            [-25, -15],
            [50, 10],
            [50, 10],
            [-10, 20],
            [-10, 20],
        ]
    else:
        aligneff = ["right", "center"]
        alignt = ["left", "center"]
        deltas = [
            [20, -2],
            [25, 10],
            [25, -10],
            [-50, -5],
            [-50, -10],
            [20, 20],
            [-30, 30],
        ]

    if len(results) != len(deltas):
        raise ValueError(
            f"The lenght of deltas is not the same as the length of the points"
        )
    # annotate effective stresses points
    for row in results:
        ax.text(
            row[1],
            row[0],
            str(row[1]),
            verticalalignment=aligneff[1],
            horizontalalignment=aligneff[0],
            transform=ax.transData,
            color="k",
            fontsize=10,
        )

    # plot lateral stresses
    for row, deltas in zip(results, deltas):
        # print(f")
        print(f"x: {row[x_idx]}, y: {row[0]}, dx: {deltas[0]}, dy: {deltas[1]}")
        ax.annotate(
            str(row[x_idx]),
            xy=(row[x_idx], row[0]),
            xycoords="data",
            xytext=(deltas[0], deltas[1]),
            textcoords="offset points",
            arrowprops=dict(arrowstyle="->", connectionstyle="arc3"),
            horizontalalignment=alignt[0],
            verticalalignment=alignt[1],
        )

    return ax


def add_markers_and_text(ax, results, idx_x, show_text):
    """Add markers at calculated stress points, and texts"""

    # add markers
    ax.plot(results[:, 1], results[:, 0], ls="None", marker="o", color="C1")
    ax.plot(results[:, idx_x], results[:, 0], ls="None", marker="s", color="k")

    # add text
    if show_text:
        ax = add_marker_text(ax, results, idx_x)

    return ax


def plot_stresses(ax, results, stress_type="active_pressure", show_text=False):

    if stress_type == "active_pressure":
        x_idx = 2
        label = r"Active pressure, $\sigma^'_{ha}$"
    elif stress_type == "passive_pressure":
        x_idx = 3
        label = r"Passive pressure, $\sigma^'_{hp}$"
    else:
        raise ValueError(f"Invalid stress_type given.")

    # draw effective stress
    ax.plot(
        results[:, 1],
        results[:, 0],
        ls="-.",
        color="C1",
        label=r"Effective stress, $\sigma^'_v$",
    )
    # draw either active or passive pressure
    ax.plot(
        results[:, x_idx],
        results[:, 0],
        ls="-",
        color="k",
        label=label,
    )
    ax = add_markers_and_text(ax, results, x_idx, show_text)
    return ax


def main():
    # paths for saving the figure
    root_dir = Path(r"./")
    plt_dir = root_dir / "plt"
    figname = "example_06_passive_pressure.png"
    ffig = plt_dir.joinpath(figname)

    # Create layers with optional arguments for lateral earth pressure calculations
    layer1 = SoilLayer(5, 100, 110, phi=26, c=50)
    layer2 = SoilLayer(10, 110, 120, phi=30, c=0)
    layer3 = SoilLayer(7, 120, 130, phi=34, c=0)
    layers = [layer1, layer2, layer3]

    # create soil profile, with watertable at 13 feet from the ground surface
    soilprofile = SoilProfile(layers, zw=13.0, gammaw=62.4)

    # lateral earth pressure calculation the long way
    # points for lateral earth pressure profile
    pts = utf.stress_profile_points(soilprofile, "lateral")

    # compute vertical stresses
    soilprofile.vertical_stresses(pts)

    # get the phi and c value for lateral earth pressure calculation
    keylist = ["phi", "c"]
    # this will return the phi and c value for the layer in which the pt falls
    params = np.asarray(soilprofile.get_params(pts, keylist))
    # extract vertical stresses in an array
    vstress = np.asarray(
        [[pt.z, pt.total_stress, pt.pore_pressure, pt.effective_stress] for pt in pts]
    )

    # compute lateral stresses
    latstress = np.zeros((vstress.shape[0], 3))
    latstress[:, 0] = vstress[:, 0]
    latstress[:, 1] = utf.calc_active_earth_pressure(
        vstress[:, 3], params[:, 0], params[:, 1]
    )
    latstress[:, 2] = utf.calc_passive_earth_pressure(
        vstress[:, 3], params[:, 0], params[:, 1]
    )
    results = np.c_[vstress[:, 0], vstress[:, 3], latstress[:, 1:]]
    # convert results to numpy array for easy manipulation
    results = np.round(results, 1)

    np.set_printoptions(suppress=True)
    print(np.around(results, decimals=2))
    # for pt in pts:
    #     print(pt.z, pt.effective_stress, pt.active_pressure, pt.passive_pressure)

    # now time to plot the stresses
    scale = 1.0
    figw = 5.0
    figh = figw / 1.618
    fsize = (scale * figw, scale * figh)
    fig, ax = plt.subplots(figsize=fsize)

    # add marker and text
    # stress_type = either "active_pressure" or "passive_pressure"
    ax = plot_stresses(ax, results, stress_type="passive_pressure", show_text=True)

    # manipulate figure properties
    ax.invert_yaxis()
    ax.grid(visible=True, which="major", axis="both", ls="-", color="grey", alpha=0.5)
    ax.set_xlabel(r"Stress values, $\sigma_v$, $\sigma^'_h$ [psf]")
    ax.set_ylabel(r"Depth, $z$ [ft]")
    ax.legend(frameon=False)
    fig.savefig(ffig, format="png", bbox_inches="tight")


if __name__ == "__main__":
    main()
