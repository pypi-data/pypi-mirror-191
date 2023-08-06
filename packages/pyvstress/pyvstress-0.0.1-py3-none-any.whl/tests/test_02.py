from pyvstress import SoilLayer, SoilProfile

# Description: Test layer subdivision at the depth of the groundwater table


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


def test_gwt_layer1():
    # test subdivision of a layer at the depth of groundwater table
    # test 1: when the watertable is in the first layer
    # depth to groundwater
    zw = 0.5
    soilprofile = soil_profile(zw)
    outputs = []
    for layer in soilprofile.layers:
        outputs.append([layer.thickness, layer.gamma_bulk, layer.gamma_sat])

    # required output
    required_outputs = [
        [0.5, 110, 120],
        [4.5, 110, 120],
        [7, 115, 115],
        [4, 115, 122],
        [1, 112, 112],
        [10, 125, 125],
    ]

    assert outputs == required_outputs


def test_gwt_layer2():
    # test subdivision of a layer at the depth of groundwater table
    # test 1: when the watertable is in the second layer
    # depth to groundwater
    zw = 7
    soilprofile = soil_profile(zw)
    outputs = []
    for layer in soilprofile.layers:
        outputs.append([layer.thickness, layer.gamma_bulk, layer.gamma_sat])

    # required output
    required_outputs = [
        [5, 110, 120],
        [2, 115, 115],
        [5, 115, 115],
        [4, 115, 122],
        [1, 112, 112],
        [10, 125, 125],
    ]

    assert outputs == required_outputs


def test_gwt_layer4():
    # test subdivision of a layer at the depth of groundwater table
    # test 1: when the watertable is in the fourth layer
    # depth to groundwater
    zw = 19.0
    soilprofile = soil_profile(zw)
    outputs = []
    for layer in soilprofile.layers:
        outputs.append([layer.thickness, layer.gamma_bulk, layer.gamma_sat])

    # required output
    required_outputs = [
        [5, 110, 120],
        [7, 115, 115],
        [4, 115, 122],
        [1, 112, 112],
        [2, 125, 125],
        [8, 125, 125],
    ]

    assert outputs == required_outputs


def test_gwt_layer5():
    # test subdivision of a layer at the depth of groundwater table
    # test 1: when the watertable is in the fourth layer
    # depth to groundwater
    zw = 16.5
    soilprofile = soil_profile(zw)
    outputs = []
    for layer in soilprofile.layers:
        outputs.append([layer.thickness, layer.gamma_bulk, layer.gamma_sat])

    # required output
    required_outputs = [
        [5, 110, 120],
        [7, 115, 115],
        [4, 115, 122],
        [0.5, 112, 112],
        [0.5, 112, 112],
        [10, 125, 125],
    ]

    assert outputs == required_outputs


def test_gwt_boundary1():
    # test subdivision of a layer at the depth of groundwater table
    # test 1: when the watertable is at the boundary of layer 1 and layer 2
    # depth to groundwater
    zw = 5
    soilprofile = soil_profile(zw)
    outputs = []
    for layer in soilprofile.layers:
        outputs.append([layer.thickness, layer.gamma_bulk, layer.gamma_sat])

    # required output
    required_outputs = [
        [5, 110, 120],
        [7, 115, 115],
        [4, 115, 122],
        [1, 112, 112],
        [10, 125, 125],
    ]

    assert outputs == required_outputs


def test_gwt_boundary2():
    # test subdivision of a layer at the depth of groundwater table
    # test 1: when the watertable is at the boundary of layer 3 and layer 4
    # depth to groundwater
    zw = 16
    soilprofile = soil_profile(zw)
    outputs = []
    for layer in soilprofile.layers:
        outputs.append([layer.thickness, layer.gamma_bulk, layer.gamma_sat])

    # required output
    required_outputs = [
        [5, 110, 120],
        [7, 115, 115],
        [4, 115, 122],
        [1, 112, 112],
        [10, 125, 125],
    ]

    assert outputs == required_outputs


def test_gwt_boundary3():
    # test subdivision of a layer at the depth of groundwater table
    # test 1: when the watertable is at the bottom of the soil profile
    # depth to groundwater
    zw = 27
    soilprofile = soil_profile(zw)
    outputs = []
    for layer in soilprofile.layers:
        outputs.append([layer.thickness, layer.gamma_bulk, layer.gamma_sat])

    # required output
    required_outputs = [
        [5, 110, 120],
        [7, 115, 115],
        [4, 115, 122],
        [1, 112, 112],
        [10, 125, 125],
    ]

    assert outputs == required_outputs
