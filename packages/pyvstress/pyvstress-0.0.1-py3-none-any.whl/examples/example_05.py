from pathlib import Path
import numpy as np
import random
import matplotlib.pyplot as plt

from pyvstress import SoilLayer, SoilProfile
import pyvstress.utility_functions as utf

# Description: lateral earth pressure over the depth of the profile and plot
# for the handcalcs version please check the notebooks folder


def generate_random_deltas(ax, a, b):
    """Generate radom deltas as percentage of x-axis and y-axis limits"""
    rnd = random.randint(a, b)
    xlims = ax.get_xlim()
    ylims = ax.get_ylim()
    dxlims = xlims[1] - xlims[0]
    dylims = ylims[1] - ylims[0]
    # print(f"dxlims: {dxlims}, dylims: {dylims}")
    dx = 0.5 * rnd / 100 * dxlims
    dy = 2 * rnd / 100 * dylims
    return (dx, dy)


def add_marker_text(ax, results, x_idx):
    """Add text next to the markers"""

    colors = ["C1", "k"]
    if x_idx == 2:
        aligneff = ["left", "center"]
        alignt = ["right", "center"]
        deltas = [[-15, -2], [-25, 10], [-25, -10], [50, 10], [-30, -10], [-30, 20]]
    else:
        aligneff = ["right", "center"]
        alignt = ["left", "center"]
        deltas = [[20, -2], [25, 10], [25, -10], [-50, -5], [30, -10], [-30, 20]]

    # plot effective stresses
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
        # print(f"dx: {deltas[0]}, dy: {deltas[1]}")
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
        idx_x = 2
        label = r"Active pressure, $\sigma^'_{ha}$"
    elif stress_type == "passive_pressure":
        idx_x = 3
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
        results[:, idx_x],
        results[:, 0],
        ls="-",
        color="k",
        label=label,
    )
    ax = add_markers_and_text(ax, results, idx_x, show_text)
    return ax


def main():
    # paths for saving the figure
    root_dir = Path(r"./")
    plt_dir = root_dir / "plt"
    figname = "example_05_active_pressure.png"
    ffig = plt_dir.joinpath(figname)

    # Create layers with optional arguments for lateral earth pressure calculations
    layer1 = SoilLayer(5, 100, 110, phi=26, c=50)
    layer2 = SoilLayer(10, 110, 120, phi=30, c=0)
    layer3 = SoilLayer(7, 120, 130, phi=34, c=0)
    layers = [layer1, layer2, layer3]

    # create soil profile, with watertable at the bottom of the soil profile
    soilprofile = SoilProfile(layers, zw=22.0, gammaw=62.4)

    # Use the utility_functions profile_lateral_earth_pressures
    # if you want to first create the points and then calculate 
    # the earth pressures then please the profile_lateral_earth_pressures

    vstress, latstress = utf.profile_lateral_earth_pressures(soilprofile)
    results = np.c_[vstress[:, 0], vstress[:, 3,], latstress[:,1:]]
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
    ax = plot_stresses(ax, results, stress_type="active_pressure", show_text=True)

    # manipulate figure properties
    ax.invert_yaxis()
    ax.grid(visible=True, which="major", axis="both", ls="-", color="grey", alpha=0.5)
    ax.set_xlabel(r"Stress values, $\sigma_v$, $\sigma^'_h$ [psf]")
    ax.set_ylabel(r"Depth, $z$ [ft]")
    ax.legend(frameon=False)
    fig.savefig(ffig, format="png", bbox_inches="tight")


if __name__ == "__main__":
    main()
