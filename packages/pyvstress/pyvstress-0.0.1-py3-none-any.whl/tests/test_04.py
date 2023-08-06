import sys
# from pathlib import Path

# module_path = Path(r"../pyvstress/")
# module_path = module_path.resolve()
# sys.path.append(str(module_path))

from pyvstress import SoilLayer, SoilProfile

# Description: Test overburden pressure calculations


def soil_profile(zw, q=0):

    # soillayers
    layer1 = SoilLayer(5, 110, 120)
    layer2 = SoilLayer(7, 115, 125)
    layer3 = SoilLayer(4, 115, 122)
    layer4 = SoilLayer(1, 112, 120)
    layer5 = SoilLayer(10, 125, 135)
    layers = [layer1, layer2, layer3, layer4, layer5]

    # soil profile
    soilprofile = SoilProfile(layers, zw=zw, q=q, gammaw=62.4)
    return soilprofile


def test_overburden_01():
    # test 1: when the groundwater table is at the surface
    # depth to groundwater
    zw = 0
    soilprofile = soil_profile(zw)
    outputs = []
    for ztop, zbot, layer in zip(
        soilprofile.ztops, soilprofile.zbots, soilprofile.layers
    ):
        outputs.append(
            [ztop, zbot, layer.gamma_bulk, layer.gamma_sat, layer.overburden, layer.sat]
        )

    # required output
    required_outputs = [
        [0, 5, 110, 120, 0.0, True],
        [5, 12, 115, 125, 600.0, True],
        [12, 16, 115, 122, 1475.0, True],
        [16, 17, 112, 120, 1963.0, True],
        [17, 27, 125, 135, 2083.0, True],
    ]

    assert outputs == required_outputs


def test_overburden_02():
    # test 2: when the groundwater table at the boundary of first and second layer
    # depth to groundwater
    zw = 5
    soilprofile = soil_profile(zw)
    outputs = []
    for ztop, zbot, layer in zip(
        soilprofile.ztops, soilprofile.zbots, soilprofile.layers
    ):
        outputs.append(
            [ztop, zbot, layer.gamma_bulk, layer.gamma_sat, layer.overburden, layer.sat]
        )

    # required output
    required_outputs = [
        [0, 5, 110, 120, 0.0, False],
        [5, 12, 115, 125, 550.0, True],
        [12, 16, 115, 122, 1425.0, True],
        [16, 17, 112, 120, 1913.0, True],
        [17, 27, 125, 135, 2033.0, True],
    ]

    assert outputs == required_outputs


def test_overburden_03():
    # test 3: when the groundwater table at the boundary of second and third layer
    # depth to groundwater
    zw = 12
    soilprofile = soil_profile(zw)
    outputs = []
    for ztop, zbot, layer in zip(
        soilprofile.ztops, soilprofile.zbots, soilprofile.layers
    ):
        outputs.append(
            [ztop, zbot, layer.gamma_bulk, layer.gamma_sat, layer.overburden, layer.sat]
        )

    # required output
    required_outputs = [
        [0, 5, 110, 120, 0.0, False],
        [5, 12, 115, 125, 550.0, False],
        [12, 16, 115, 122, 1355.0, True],
        [16, 17, 112, 120, 1843.0, True],
        [17, 27, 125, 135, 1963.0, True],
    ]

    assert outputs == required_outputs


def test_overburden_04():
    # test 4: when the groundwater table at the boundary of last layer
    # depth to groundwater
    zw = 17
    soilprofile = soil_profile(zw)
    outputs = []
    for ztop, zbot, layer in zip(
        soilprofile.ztops, soilprofile.zbots, soilprofile.layers
    ):
        outputs.append(
            [ztop, zbot, layer.gamma_bulk, layer.gamma_sat, layer.overburden, layer.sat]
        )

    # required output
    required_outputs = [
        [0, 5, 110, 120, 0.0, False],
        [5, 12, 115, 125, 550.0, False],
        [12, 16, 115, 122, 1355.0, False],
        [16, 17, 112, 120, 1815.0, False],
        [17, 27, 125, 135, 1927.0, True],
    ]

    assert outputs == required_outputs


def test_overburden_05():
    # test 5: when the groundwater table at the bottom of the soil profile
    # depth to groundwater
    zw = 27
    soilprofile = soil_profile(zw)
    outputs = []
    for ztop, zbot, layer in zip(
        soilprofile.ztops, soilprofile.zbots, soilprofile.layers
    ):
        outputs.append(
            [ztop, zbot, layer.gamma_bulk, layer.gamma_sat, layer.overburden, layer.sat]
        )

    # required output
    required_outputs = [
        [0, 5, 110, 120, 0.0, False],
        [5, 12, 115, 125, 550.0, False],
        [12, 16, 115, 122, 1355.0, False],
        [16, 17, 112, 120, 1815.0, False],
        [17, 27, 125, 135, 1927.0, False],
    ]

    assert outputs == required_outputs


def test_overburden_06():
    # test 6: when the groundwater table in the first layer
    # depth to groundwater
    zw = 1
    soilprofile = soil_profile(zw)
    outputs = []
    for ztop, zbot, layer in zip(
        soilprofile.ztops, soilprofile.zbots, soilprofile.layers
    ):
        outputs.append(
            [ztop, zbot, layer.gamma_bulk, layer.gamma_sat, layer.overburden, layer.sat]
        )

    # required output
    required_outputs = [
        [0, 1, 110, 120, 0.0, False],
        [1, 5, 110, 120, 110, True],
        [5, 12, 115, 125, 590.0, True],
        [12, 16, 115, 122, 1465.0, True],
        [16, 17, 112, 120, 1953.0, True],
        [17, 27, 125, 135, 2073.0, True],
    ]

    assert outputs == required_outputs


def test_overburden_07():
    # test 7: when the groundwater table in the second layer
    # depth to groundwater
    zw = 7
    soilprofile = soil_profile(zw)
    outputs = []
    for ztop, zbot, layer in zip(
        soilprofile.ztops, soilprofile.zbots, soilprofile.layers
    ):
        outputs.append(
            [ztop, zbot, layer.gamma_bulk, layer.gamma_sat, layer.overburden, layer.sat]
        )

    # required output
    required_outputs = [
        [0, 5, 110, 120, 0.0, False],
        [5, 7, 115, 125, 550, False],
        [7, 12, 115, 125, 780.0, True],
        [12, 16, 115, 122, 1405.0, True],
        [16, 17, 112, 120, 1893.0, True],
        [17, 27, 125, 135, 2013.0, True],
    ]

    assert outputs == required_outputs


def test_overburden_08():
    # test 8: when the groundwater table in the last layer
    # depth to groundwater
    zw = 19
    soilprofile = soil_profile(zw)
    outputs = []
    for ztop, zbot, layer in zip(
        soilprofile.ztops, soilprofile.zbots, soilprofile.layers
    ):
        outputs.append(
            [ztop, zbot, layer.gamma_bulk, layer.gamma_sat, layer.overburden, layer.sat]
        )

    # required output
    required_outputs = [
        [0, 5, 110, 120, 0.0, False],
        [5, 12, 115, 125, 550.0, False],
        [12, 16, 115, 122, 1355.0, False],
        [16, 17, 112, 120, 1815.0, False],
        [17, 19, 125, 135, 1927.0, False],
        [19, 27, 125, 135, 2177.0, True],
    ]

    assert outputs == required_outputs


def test_overburden_09():
    # test 7: when the groundwater table in the second layer
    # depth to groundwater
    zw = 7
    # surface surcharge
    q = 100
    soilprofile = soil_profile(zw, q)
    outputs = []
    for ztop, zbot, layer in zip(
        soilprofile.ztops, soilprofile.zbots, soilprofile.layers
    ):
        outputs.append(
            [ztop, zbot, layer.gamma_bulk, layer.gamma_sat, layer.overburden, layer.sat]
        )

    # required output
    required_outputs = [
        [0, 5, 110, 120, 100.0, False],
        [5, 7, 115, 125, 650, False],
        [7, 12, 115, 125, 880.0, True],
        [12, 16, 115, 122, 1505.0, True],
        [16, 17, 112, 120, 1993.0, True],
        [17, 27, 125, 135, 2113.0, True],
    ]

    assert outputs == required_outputs
