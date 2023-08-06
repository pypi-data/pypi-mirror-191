# import numpy as np
# import sys
# from pathlib import Path

# module_path = Path(r"../pyvstress/")
# module_path = module_path.resolve()
# sys.path.append(str(module_path))

from pyvstress import Point, SoilLayer, SoilProfile

# Description: Test calculation of total stress, pore pressure, and effective stress


def test_stress_calc_01():
    # testing total stresses, porepressure, and effectives stresses when the watertable is
    # at the ground surface.

    # soillayers
    layer1 = SoilLayer(5, 110, 120)
    layer2 = SoilLayer(7, 115, 125)
    layer3 = SoilLayer(4, 115, 122)
    layer4 = SoilLayer(1, 112, 120)
    layer5 = SoilLayer(10, 125, 135)
    layers = [layer1, layer2, layer3, layer4, layer5]

    # soil profile
    soilprofile = SoilProfile(layers, zw=0, q=0, gammaw=62.4)

    # location of point below the ground surface
    zs = [0, 1, 5, 10, 12, 15, 16, 16.5, 17, 20, 27]
    pts = [Point(z) for z in zs]

    soilprofile.vertical_stresses(pts)

    round_off = 1
    results = []
    for pt in pts:
        results.append(
            [
                round(pt.z, round_off),
                round(pt.total_stress, round_off),
                round(pt.pore_pressure, round_off),
                round(pt.effective_stress, round_off),
            ]
        )

    # required results
    required_results = [
        [0.0, 0.0, 0.0, 0.0],
        [1.0, 120.0, 62.4, 57.6],
        [5.0, 600.0, 312.0, 288.0],
        [10.0, 1225.0, 624.0, 601.0],
        [12.0, 1475.0, 748.8, 726.2],
        [15.0, 1841.0, 936.0, 905.0],
        [16.0, 1963.0, 998.4, 964.6],
        [16.5, 2023.0, 1029.6, 993.4],
        [17.0, 2083.0, 1060.8, 1022.2],
        [20.0, 2488.0, 1248.0, 1240.0],
        [27.0, 3433.0, 1684.8, 1748.2],
    ]

    assert results == required_results


def test_stress_calc_02():
    # testing total stresses, porepressure, and effectives stresses when the watertable is
    # in the first layer.

    # soillayers
    layer1 = SoilLayer(5, 110, 120)
    layer2 = SoilLayer(7, 115, 125)
    layer3 = SoilLayer(4, 115, 122)
    layer4 = SoilLayer(1, 112, 120)
    layer5 = SoilLayer(10, 125, 135)
    layers = [layer1, layer2, layer3, layer4, layer5]

    # soil profile
    soilprofile = SoilProfile(layers, zw=1, q=0, gammaw=62.4)

    # location of point below the ground surface
    zs = [0, 1, 5, 10, 12, 15, 16, 16.5, 17, 20, 27]
    pts = [Point(z) for z in zs]

    soilprofile.vertical_stresses(pts)

    round_off = 1
    results = []
    for pt in pts:
        results.append(
            [
                round(pt.z, round_off),
                round(pt.total_stress, round_off),
                round(pt.pore_pressure, round_off),
                round(pt.effective_stress, round_off),
            ]
        )

    # required results
    required_results = [
        [0.0, 0.0, 0.0, 0.0],
        [1.0, 110.0, 0.0, 110.0],
        [5.0, 590.0, 249.6, 340.4],
        [10.0, 1215.0, 561.6, 653.4],
        [12.0, 1465.0, 686.4, 778.6],
        [15.0, 1831.0, 873.6, 957.4],
        [16.0, 1953.0, 936.0, 1017.0],
        [16.5, 2013.0, 967.2, 1045.8],
        [17.0, 2073.0, 998.4, 1074.6],
        [20.0, 2478.0, 1185.6, 1292.4],
        [27.0, 3423.0, 1622.4, 1800.6],
    ]

    assert results == required_results


def test_stress_calc_03():
    # testing total stresses, porepressure, and effectives stresses when the watertable is
    # at the bottom of the first layer watertable at 5 ft depth

    # soillayers
    layer1 = SoilLayer(5, 110, 120)
    layer2 = SoilLayer(7, 115, 125)
    layer3 = SoilLayer(4, 115, 122)
    layer4 = SoilLayer(1, 112, 120)
    layer5 = SoilLayer(10, 125, 135)
    layers = [layer1, layer2, layer3, layer4, layer5]

    # soil profile
    soilprofile = SoilProfile(layers, zw=5, q=0, gammaw=62.4)

    # location of point below the ground surface
    zs = [0, 1, 5, 10, 12, 15, 16, 16.5, 17, 20, 27]
    pts = [Point(z) for z in zs]

    soilprofile.vertical_stresses(pts)

    round_off = 1
    results = []
    for pt in pts:
        results.append(
            [
                round(pt.z, round_off),
                round(pt.total_stress, round_off),
                round(pt.pore_pressure, round_off),
                round(pt.effective_stress, round_off),
            ]
        )

    # required results
    required_results = [
        [0.0, 0.0, 0.0, 0.0],
        [1.0, 110.0, 0.0, 110.0],
        [5.0, 550.0, 0.0, 550.0],
        [10.0, 1175.0, 312.0, 863.0],
        [12.0, 1425.0, 436.8, 988.2],
        [15.0, 1791.0, 624.0, 1167.0],
        [16.0, 1913.0, 686.4, 1226.6],
        [16.5, 1973.0, 717.6, 1255.4],
        [17.0, 2033.0, 748.8, 1284.2],
        [20.0, 2438.0, 936.0, 1502.0],
        [27.0, 3383.0, 1372.8, 2010.2],
    ]

    assert results == required_results


def test_stress_calc_04():
    # testing total stresses, porepressure, and effectives stresses when the watertable is
    # at the bottom of a middle layer, watertable at 16 ft depth

    # soillayers
    layer1 = SoilLayer(5, 110, 120)
    layer2 = SoilLayer(7, 115, 125)
    layer3 = SoilLayer(4, 115, 122)
    layer4 = SoilLayer(1, 112, 120)
    layer5 = SoilLayer(10, 125, 135)
    layers = [layer1, layer2, layer3, layer4, layer5]

    # soil profile
    soilprofile = SoilProfile(layers, zw=16, q=0, gammaw=62.4)

    # location of point below the ground surface
    zs = [0, 1, 5, 10, 12, 15, 16, 16.5, 17, 20, 27]
    pts = [Point(z) for z in zs]

    soilprofile.vertical_stresses(pts)

    round_off = 1
    results = []
    for pt in pts:
        results.append(
            [
                round(pt.z, round_off),
                round(pt.total_stress, round_off),
                round(pt.pore_pressure, round_off),
                round(pt.effective_stress, round_off),
            ]
        )

    # required results
    required_results = [
        [0.0, 0.0, 0.0, 0.0],
        [1.0, 110.0, 0.0, 110.0],
        [5.0, 550.0, 0.0, 550.0],
        [10.0, 1125.0, 0.0, 1125.0],
        [12.0, 1355.0, 0.0, 1355.0],
        [15.0, 1700.0, 0.0, 1700.0],
        [16.0, 1815.0, 0.0, 1815.0],
        [16.5, 1875.0, 31.2, 1843.8],
        [17.0, 1935.0, 62.4, 1872.6],
        [20.0, 2340.0, 249.6, 2090.4],
        [27.0, 3285.0, 686.4, 2598.6],
    ]

    assert results == required_results


def test_stress_calc_05():
    # testing total stresses, porepressure, and effectives stresses when the watertable is
    # at the middle of a middle layer, watertable at 14 ft depth

    # soillayers
    layer1 = SoilLayer(5, 110, 120)
    layer2 = SoilLayer(7, 115, 125)
    layer3 = SoilLayer(4, 115, 122)
    layer4 = SoilLayer(1, 112, 120)
    layer5 = SoilLayer(10, 125, 135)
    layers = [layer1, layer2, layer3, layer4, layer5]

    # soil profile
    soilprofile = SoilProfile(layers, zw=14, q=0, gammaw=62.4)

    # location of point below the ground surface
    zs = [0, 1, 5, 10, 12, 14, 15, 16, 16.5, 17, 20, 27]
    pts = [Point(z) for z in zs]

    soilprofile.vertical_stresses(pts)

    round_off = 1
    results = []
    for pt in pts:
        results.append(
            [
                round(pt.z, round_off),
                round(pt.total_stress, round_off),
                round(pt.pore_pressure, round_off),
                round(pt.effective_stress, round_off),
            ]
        )

    # required results
    required_results = [
        [0.0, 0.0, 0.0, 0.0],
        [1.0, 110.0, 0.0, 110.0],
        [5.0, 550.0, 0.0, 550.0],
        [10.0, 1125.0, 0.0, 1125.0],
        [12.0, 1355.0, 0.0, 1355.0],
        [14.0, 1585.0, 0.0, 1585.0],
        [15.0, 1707.0, 62.4, 1644.6],
        [16.0, 1829.0, 124.8, 1704.2],
        [16.5, 1889.0, 156.0, 1733.0],
        [17.0, 1949.0, 187.2, 1761.8],
        [20.0, 2354.0, 374.4, 1979.6],
        [27.0, 3299.0, 811.2, 2487.8],
    ]

    assert results == required_results


def test_stress_calc_06():
    # testing total stresses, porepressure, and effectives stresses when the watertable is
    # at the top of the last layer, watertable at 17 ft depth

    # soillayers
    layer1 = SoilLayer(5, 110, 120)
    layer2 = SoilLayer(7, 115, 125)
    layer3 = SoilLayer(4, 115, 122)
    layer4 = SoilLayer(1, 112, 120)
    layer5 = SoilLayer(10, 125, 135)
    layers = [layer1, layer2, layer3, layer4, layer5]

    # soil profile
    soilprofile = SoilProfile(layers, zw=17, q=0, gammaw=62.4)

    # location of point below the ground surface
    zs = [0, 1, 5, 10, 12, 14, 15, 16, 16.5, 17, 20, 27]
    pts = [Point(z) for z in zs]

    soilprofile.vertical_stresses(pts)

    round_off = 1
    results = []
    for pt in pts:
        results.append(
            [
                round(pt.z, round_off),
                round(pt.total_stress, round_off),
                round(pt.pore_pressure, round_off),
                round(pt.effective_stress, round_off),
            ]
        )

    # required results
    required_results = [
        [0.0, 0.0, 0.0, 0.0],
        [1.0, 110.0, 0.0, 110.0],
        [5.0, 550.0, 0.0, 550.0],
        [10.0, 1125.0, 0.0, 1125.0],
        [12.0, 1355.0, 0.0, 1355.0],
        [14.0, 1585.0, 0.0, 1585.0],
        [15.0, 1700.0, 0.0, 1700.0],
        [16.0, 1815.0, 0.0, 1815.0],
        [16.5, 1871.0, 0.0, 1871.0],
        [17.0, 1927.0, 0.0, 1927.0],
        [20.0, 2332.0, 187.2, 2144.8],
        [27.0, 3277.0, 624.0, 2653.0],
    ]

    assert results == required_results


def test_stress_calc_07():
    # testing total stresses, porepressure, and effectives stresses when the watertable is
    # at the middle of the last layer, watertable at 19 ft depth

    # soillayers
    layer1 = SoilLayer(5, 110, 120)
    layer2 = SoilLayer(7, 115, 125)
    layer3 = SoilLayer(4, 115, 122)
    layer4 = SoilLayer(1, 112, 120)
    layer5 = SoilLayer(10, 125, 135)
    layers = [layer1, layer2, layer3, layer4, layer5]

    # soil profile
    soilprofile = SoilProfile(layers, zw=19, q=0, gammaw=62.4)

    # location of point below the ground surface
    zs = [0, 1, 5, 10, 12, 14, 15, 16, 16.5, 17, 19, 20, 27]
    pts = [Point(z) for z in zs]

    soilprofile.vertical_stresses(pts)

    round_off = 1
    results = []
    for pt in pts:
        results.append(
            [
                round(pt.z, round_off),
                round(pt.total_stress, round_off),
                round(pt.pore_pressure, round_off),
                round(pt.effective_stress, round_off),
            ]
        )

    # required results
    required_results = [
        [0.0, 0.0, 0.0, 0.0],
        [1.0, 110.0, 0.0, 110.0],
        [5.0, 550.0, 0.0, 550.0],
        [10.0, 1125.0, 0.0, 1125.0],
        [12.0, 1355.0, 0.0, 1355.0],
        [14.0, 1585.0, 0.0, 1585.0],
        [15.0, 1700.0, 0.0, 1700.0],
        [16.0, 1815.0, 0.0, 1815.0],
        [16.5, 1871.0, 0.0, 1871.0],
        [17.0, 1927.0, 0.0, 1927.0],
        [19.0, 2177.0, 0.0, 2177.0],
        [20.0, 2312.0, 62.4, 2249.6],
        [27.0, 3257.0, 499.2, 2757.8],
    ]

    assert results == required_results


def test_stress_calc_08():
    # testing total stresses, porepressure, and effectives stresses when the watertable is
    # at the bottom of the last layer, watertable at 27 ft depth

    # soillayers
    layer1 = SoilLayer(5, 110, 120)
    layer2 = SoilLayer(7, 115, 125)
    layer3 = SoilLayer(4, 115, 122)
    layer4 = SoilLayer(1, 112, 120)
    layer5 = SoilLayer(10, 125, 135)
    layers = [layer1, layer2, layer3, layer4, layer5]

    # soil profile
    soilprofile = SoilProfile(layers, zw=27, q=0, gammaw=62.4)

    # location of point below the ground surface
    zs = [0, 1, 5, 10, 12, 14, 15, 16, 16.5, 17, 19, 20, 27]
    pts = [Point(z) for z in zs]

    soilprofile.vertical_stresses(pts)

    round_off = 1
    results = []
    for pt in pts:
        results.append(
            [
                round(pt.z, round_off),
                round(pt.total_stress, round_off),
                round(pt.pore_pressure, round_off),
                round(pt.effective_stress, round_off),
            ]
        )

    # required results
    required_results = [
        [0.0, 0.0, 0.0, 0.0],
        [1.0, 110.0, 0.0, 110.0],
        [5.0, 550.0, 0.0, 550.0],
        [10.0, 1125.0, 0.0, 1125.0],
        [12.0, 1355.0, 0.0, 1355.0],
        [14.0, 1585.0, 0.0, 1585.0],
        [15.0, 1700.0, 0.0, 1700.0],
        [16.0, 1815.0, 0.0, 1815.0],
        [16.5, 1871.0, 0.0, 1871.0],
        [17.0, 1927.0, 0.0, 1927.0],
        [19.0, 2177.0, 0.0, 2177.0],
        [20.0, 2302.0, 0.0, 2302.0],
        [27.0, 3177.0, 0.0, 3177.0],
    ]

    assert results == required_results


def test_stress_calc_09():
    # testing total stresses, porepressure, and effectives stresses when the watertable is
    # at the middle of the middle layer, watertable at 14 ft depth + 100 psf surface surcharge

    # soillayers
    layer1 = SoilLayer(5, 110, 120)
    layer2 = SoilLayer(7, 115, 125)
    layer3 = SoilLayer(4, 115, 122)
    layer4 = SoilLayer(1, 112, 120)
    layer5 = SoilLayer(10, 125, 135)
    layers = [layer1, layer2, layer3, layer4, layer5]

    # soil profile
    soilprofile = SoilProfile(layers, zw=14, q=100, gammaw=62.4)

    # location of point below the ground surface
    zs = [0, 1, 5, 10, 12, 14, 15, 16, 16.5, 17, 19, 20, 27]
    pts = [Point(z) for z in zs]

    soilprofile.vertical_stresses(pts)

    round_off = 1
    results = []
    for pt in pts:
        results.append(
            [
                round(pt.z, round_off),
                round(pt.total_stress, round_off),
                round(pt.pore_pressure, round_off),
                round(pt.effective_stress, round_off),
            ]
        )

    # required results
    required_results = [
        [0.0, 100.0, 0.0, 100.0],
        [1.0, 210.0, 0.0, 210.0],
        [5.0, 650.0, 0.0, 650.0],
        [10.0, 1225.0, 0.0, 1225.0],
        [12.0, 1455.0, 0.0, 1455.0],
        [14.0, 1685.0, 0.0, 1685.0],
        [15.0, 1807.0, 62.4, 1744.6],
        [16.0, 1929.0, 124.8, 1804.2],
        [16.5, 1989.0, 156.0, 1833.0],
        [17.0, 2049.0, 187.2, 1861.8],
        [19.0, 2319.0, 312.0, 2007.0],
        [20.0, 2454.0, 374.4, 2079.6],
        [27.0, 3399.0, 811.2, 2587.8],
    ]

    assert results == required_results
