import numpy as np
import matplotlib.pyplot as plt
from pyvstress import SoilLayer, SoilProfile
import pyvstress.utility_functions as utf
from pathlib import Path

# Description: vertical stresses over the profile and plot


def add_marker_text(ax, results, zw, stress_type):
    """Add text next to the markers"""

    idx_zw = np.where(abs(results[:, 0] - zw) < 0.001)[0][0]
    if stress_type == "total_stress":
        start_row = 0
        x_idx = 1
        halign = "left"
    elif stress_type == "pore_pressure":
        start_row = idx_zw + 1
        x_idx = 2
        halign = "right"
    elif stress_type == "effective_stress":
        start_row = idx_zw + 1
        x_idx = 3
        halign = "right"
    else:
        print(f"Invalid stress_type.")

    for row in results[start_row:]:
        ax.text(
            row[x_idx],
            row[0],
            str(row[x_idx]),
            verticalalignment="bottom",
            horizontalalignment=halign,
            transform=ax.transData,
            color="k",
            fontsize=10,
        )
    return ax


def add_markers_and_text(ax, results, zw, show_text=False):
    """Add markers at calculated stress points, and texts"""

    # add markers
    ax.plot(results[:, 1], results[:, 0], ls="None", marker="s", color="k")
    ax.plot(results[:, 2], results[:, 0], ls="None", marker="o", color="C0")
    ax.plot(results[:, 3], results[:, 0], ls="None", marker="^", color="C1")

    # add text
    if show_text:
        ax = add_marker_text(ax, results, zw, "total_stress")
        ax = add_marker_text(ax, results, zw, "pore_pressure")
        ax = add_marker_text(ax, results, zw, "effective_stress")

    return ax


def main():
    # paths for saving the figure
    root_dir = Path(r"./")
    plt_dir = root_dir / "plt"
    figname = "example_03_vertical_stresses.png"
    ffig = plt_dir.joinpath(figname)

    # Create layers with optional arguments for lateral earth pressure calculations
    layer1 = SoilLayer(5, 100, 110, phi=26, c=100)
    layer2 = SoilLayer(7, 115, 125, phi=28, c=100)
    layer3 = SoilLayer(4, 115, 122, phi=30)
    layer4 = SoilLayer(1, 110, 115, phi=25, c=25)
    layer5 = SoilLayer(10, 125, 135, phi=35)
    layers = [layer1, layer2, layer3, layer4, layer5]

    # create soil profile, with watertable at 7 feet from the ground surface
    soilprofile = SoilProfile(layers, zw=7.0, gammaw=62.4)

    # get the points for creating vertical stresse profile
    # Point objects are returned
    pts = utf.stress_profile_points(soilprofile)

    # compute vertical stresses at the above points, the stresses computed are stored in the pts
    # and can be retrieved with pt.total_stress, pt.pore_pressure, pt.effective_stress
    soilprofile.vertical_stresses(pts)
    results = []
    for pt in pts:
        results.append([pt.z, pt.total_stress, pt.pore_pressure, pt.effective_stress])

    # print("Vertical stresses:")
    # print(
    #     f"{'z':>5s}, {'Total stress':>15s}, {'Pore press.':>15s}, {'Eff. stress':>15s}"
    # )
    # for pt in pts:
    #     print(
    #         f"{pt.z:>5.2f}, {pt.total_stress:>15.2f}, {pt.pore_pressure:>15.2f}, {pt.effective_stress:>15.2f}"
    #     )

    # convert results to numpy array for easy manipulation
    results = np.asarray(results)

    # now time to plot the stresses
    scale = 1.0
    figw = 5.0
    figh = figw / 1.618
    fsize = (scale * figw, scale * figh)
    fig, ax = plt.subplots(figsize=fsize)

    # draw the lines
    ax.plot(
        results[:, 1],
        results[:, 0],
        ls="-",
        color="k",
        label=r"Total stress, $\sigma_v$",
    )
    ax.plot(
        results[:, 2], results[:, 0], ls="--", color="C0", label=r"Pore pressure, $u$"
    )
    ax.plot(
        results[:, 3],
        results[:, 0],
        ls="-.",
        color="C1",
        label=r"Effective stress, $\sigma^'_v$",
    )

    # add marker and text
    ax = add_markers_and_text(ax, results, soilprofile.zw, show_text=True)

    # manipulate figure properties
    ax.invert_yaxis()
    ax.grid(visible=True, which="major", axis="both", ls="-", color="grey", alpha=0.5)
    ax.set_xlabel(r"Stress values, $\sigma_v$, $u$, $\sigma^'_v$ [psf]")
    ax.set_ylabel(r"Depth, $z$ [ft]")
    ax.legend(frameon=False)
    fig.savefig(ffig, format="png", bbox_inches="tight")


if __name__ == "__main__":
    main()
