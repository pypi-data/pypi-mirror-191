import numpy as np
from pyvstress import SoilLayer, SoilProfile
import pyvstress.utility_functions as utf
from pathlib import Path
import matplotlib.pyplot as plt


# Description: lateral earth pressure over the depth of the profile and plot


def add_marker_text(ax, results, x_idx):
    """Add text next to the markers"""

    idxs = [1, x_idx]
    colors = ["C1", "k"]
    if x_idx == 2:
        haligns = ["left", "right"]
    else:
        haligns = ["right", "left"]

    for idx, halign, color in zip(idxs, haligns, colors):
        for row in results:
            ax.text(
                row[idx],
                row[0],
                str(row[idx]),
                verticalalignment="bottom",
                horizontalalignment="right",
                transform=ax.transData,
                color="k",
                fontsize=8,
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


def plot_lateral_stresses(ax, vertstress, latstress, stress_type="active_pressure", show_text=False):

    if stress_type == "active_pressure":
        idx_x = 1
        label = r"Active pressure, $\sigma^'_{ha}$"
    elif stress_type == "passive_pressure":
        idx_x = 2
        label = r"Passive pressure, $\sigma^'_{hp}$"
    else:
        raise ValueError(f"Invalid stress_type given.")

    # draw effective stress
    ax.plot(
        vertstress[:, 3],
        vertstress[:, 0],
        ls="-.",
        color="C1",
        label=r"Effective stress, $\sigma^'_v$",
    )
    # draw either active or passive pressure
    ax.plot(
        latstress[:, idx_x],
        latstress[:, 0],
        ls="-",
        color="k",
        label=label,
    )
    ax = add_markers_and_text(ax, latstress, idx_x, show_text)
    return ax


def main():
    # paths for saving the figure
    root_dir = Path(r"./")
    plt_dir = root_dir / "plt"
    figname = "example_04_lateral_stresses.png"
    ffig = plt_dir.joinpath(figname)

    # Create layers with optional arguments for lateral earth pressure calculations
    layer1 = SoilLayer(5, 100, 110, phi=26, c=100)
    layer2 = SoilLayer(7, 115, 125, phi=28, c=100)
    layer3 = SoilLayer(4, 115, 122, phi=30, c=0)
    layer4 = SoilLayer(1, 110, 115, phi=25, c=25)
    layer5 = SoilLayer(10, 125, 135, phi=35, c=0)
    layers = [layer1, layer2, layer3, layer4, layer5]

    # create soil profile, with watertable at 7 feet from the ground surface
    soilprofile = SoilProfile(layers, zw=7.0, gammaw=62.4)

    # use the utility function to compute lateral earth pressures for utility
    vertstresses, latstresses = utf.profile_lateral_earth_pressures(soilprofile)

    print("Vertical stresses:")
    print(
        f"{'z':>5s}, {'Total stress':>15s}, {'Pore press.':>15s}, {'Eff. stress':>15s}"
    )
    for vstress in vertstresses:
        print(
            f"{vstress[0]:>5.2f}, {vstress[1]:>15.2f}, {vstress[2]:>15.2f}, {vstress[3]:>15.2f}"
        )
    
    print("Lateral earth pressures:")
    print(
        f"{'z':>5s}, {'Eff. Stress':>15s}, {'Active Pressure':>15s}, {'Passive Pressure':>15s}"
    )
    for vertstress, latstress in zip(vertstresses, latstresses):
        print(
            f"{latstress[0]:>5.2f}, {vertstress[3]:>15.2f}, {latstress[1]:>15.2f}, {latstress[2]:>15.2f}"
        )
    
    # # convert results to numpy array for easy manipulation
    # latstresses = np.round(latstresses, 1)
    # vertstresses = np.round(vertstresses, 1)
    # print(latstresses)
    # # now time to plot the stresses
    # scale = 1.0
    # figw = 5.0
    # figh = figw / 1.618
    # fsize = (scale * figw, scale * figh)
    # fig, ax = plt.subplots(figsize=fsize)

    # # add marker and text
    # # stress_type = either "active_pressure" or "passive_pressure"
    # ax = plot_lateral_stresses(
    #     ax, vertstresses, latstresses, stress_type="active_pressure", show_text=True
    # )

    # # manipulate figure properties
    # ax.invert_yaxis()
    # ax.grid(visible=True, which="major", axis="both", ls="-", color="grey", alpha=0.5)
    # ax.set_xlabel(r"Stress values, $\sigma_v$, $\sigma^'_h$ [psf]")
    # ax.set_ylabel(r"Depth, $z$ [ft]")
    # ax.legend(frameon=False)
    # fig.savefig(ffig, format="png", bbox_inches="tight")


if __name__ == "__main__":
    main()
