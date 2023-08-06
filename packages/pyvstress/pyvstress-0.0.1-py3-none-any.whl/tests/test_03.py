from pyvstress import SoilLayer, SoilProfile

# Description: Test layer subdivision at the depth of the groundwater table
# including layer depths from the surface and saturation flag


def soil_profile(zw):

    # soillayers
    layer1 = SoilLayer(5, 110, 120)
    layer2 = SoilLayer(7, 115)
    layer3 = SoilLayer(4, 115, 122)
    layer4 = SoilLayer(1, 112)
    layer5 = SoilLayer(10, 125)
    layers = [layer1, layer2, layer3, layer4, layer5]

    # soil profile
    soilprofile = SoilProfile(layers, zw=zw, gammaw=62.4)

    return soilprofile


def test_gwt_surface():
    # test 1: when the groundwater table is at the surface
    # depth to groundwater
    zw = 0
    soilprofile = soil_profile(zw)
    outputs = []
    for ztop, zbot, layer in zip(
        soilprofile.ztops, soilprofile.zbots, soilprofile.layers
    ):
        outputs.append([ztop, zbot, layer.gamma_bulk, layer.gamma_sat, layer.sat])

    # required output
    required_outputs = [
        [0, 5, 110, 120, True],
        [5, 12, 115, 115, True],
        [12, 16, 115, 122, True],
        [16, 17, 112, 112, True],
        [17, 27, 125, 125, True],
    ]

    assert outputs == required_outputs


def test_gwt_layer1():
    # test 2: when the groundwater table is in the first layer
    # depth to groundwater
    zw = 0.5
    soilprofile = soil_profile(zw)
    outputs = []
    for ztop, zbot, layer in zip(
        soilprofile.ztops, soilprofile.zbots, soilprofile.layers
    ):
        outputs.append([ztop, zbot, layer.gamma_bulk, layer.gamma_sat, layer.sat])

    # required output
    required_outputs = [
        [0, 0.5, 110, 120, False],
        [0.5, 5, 110, 120, True],
        [5, 12, 115, 115, True],
        [12, 16, 115, 122, True],
        [16, 17, 112, 112, True],
        [17, 27, 125, 125, True],
    ]

    assert outputs == required_outputs


def test_gwt_layer2():
    # test 3: when the groundwater table is in the last layer
    # depth to groundwater
    zw = 19
    soilprofile = soil_profile(zw)
    outputs = []
    for ztop, zbot, layer in zip(
        soilprofile.ztops, soilprofile.zbots, soilprofile.layers
    ):
        outputs.append([ztop, zbot, layer.gamma_bulk, layer.gamma_sat, layer.sat])

    # required output
    required_outputs = [
        [0, 5, 110, 120, False],
        [5, 12, 115, 115, False],
        [12, 16, 115, 122, False],
        [16, 17, 112, 112, False],
        [17, 19, 125, 125, False],
        [19, 27, 125, 125, True],
    ]

    assert outputs == required_outputs


def test_gwt_layer3():
    # test 4: when the groundwater table is in an interior layer
    # depth to groundwater
    zw = 14
    soilprofile = soil_profile(zw)
    outputs = []
    for ztop, zbot, layer in zip(
        soilprofile.ztops, soilprofile.zbots, soilprofile.layers
    ):
        outputs.append([ztop, zbot, layer.gamma_bulk, layer.gamma_sat, layer.sat])

    # required output
    required_outputs = [
        [0, 5, 110, 120, False],
        [5, 12, 115, 115, False],
        [12, 14, 115, 122, False],
        [14, 16, 115, 122, True],
        [16, 17, 112, 112, True],
        [17, 27, 125, 125, True],
    ]

    assert outputs == required_outputs


def test_gwt_boundary2():
    # test 5: when the groundwater table is at layer 1 and layer 2
    # depth to groundwater
    zw = 5
    soilprofile = soil_profile(zw)
    outputs = []
    for ztop, zbot, layer in zip(
        soilprofile.ztops, soilprofile.zbots, soilprofile.layers
    ):
        outputs.append([ztop, zbot, layer.gamma_bulk, layer.gamma_sat, layer.sat])

    # required output
    required_outputs = [
        [0, 5, 110, 120, False],
        [5, 12, 115, 115, True],
        [12, 16, 115, 122, True],
        [16, 17, 112, 112, True],
        [17, 27, 125, 125, True],
    ]

    assert outputs == required_outputs


def test_gwt_boundary3():
    # test 6: when the groundwater table is at layer 4 and layer 5
    # depth to groundwater
    zw = 17
    soilprofile = soil_profile(zw)
    outputs = []
    for ztop, zbot, layer in zip(
        soilprofile.ztops, soilprofile.zbots, soilprofile.layers
    ):
        outputs.append([ztop, zbot, layer.gamma_bulk, layer.gamma_sat, layer.sat])

    # required output
    required_outputs = [
        [0, 5, 110, 120, False],
        [5, 12, 115, 115, False],
        [12, 16, 115, 122, False],
        [16, 17, 112, 112, False],
        [17, 27, 125, 125, True],
    ]

    assert outputs == required_outputs


def test_gwt_boundary4():
    # test 7: when the groundwater table is an inner layer boundary
    # depth to groundwater
    zw = 16
    soilprofile = soil_profile(zw)
    outputs = []
    for ztop, zbot, layer in zip(
        soilprofile.ztops, soilprofile.zbots, soilprofile.layers
    ):
        outputs.append([ztop, zbot, layer.gamma_bulk, layer.gamma_sat, layer.sat])

    # required output
    required_outputs = [
        [0, 5, 110, 120, False],
        [5, 12, 115, 115, False],
        [12, 16, 115, 122, False],
        [16, 17, 112, 112, True],
        [17, 27, 125, 125, True],
    ]

    assert outputs == required_outputs


def test_gwt_boundary5():
    # test 8: when the groundwater table is at the bottom of the soil profile
    # depth to groundwater
    zw = 27
    soilprofile = soil_profile(zw)
    outputs = []
    for ztop, zbot, layer in zip(
        soilprofile.ztops, soilprofile.zbots, soilprofile.layers
    ):
        outputs.append([ztop, zbot, layer.gamma_bulk, layer.gamma_sat, layer.sat])

    # required output
    required_outputs = [
        [0, 5, 110, 120, False],
        [5, 12, 115, 115, False],
        [12, 16, 115, 122, False],
        [16, 17, 112, 112, False],
        [17, 27, 125, 125, False],
    ]

    assert outputs == required_outputs