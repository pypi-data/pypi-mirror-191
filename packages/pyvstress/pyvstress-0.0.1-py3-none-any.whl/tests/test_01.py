from pyvstress import SoilLayer, SoilProfile

# Description: Test the order of layers and that gamma_sat will be assigned gamma_bulk
# if gamma_sat is missing


def test_soilprofile_missing_gamma_sat():

    # soil layers
    layer1 = SoilLayer(5, 110, 120)
    layer2 = SoilLayer(7, 115)
    layer3 = SoilLayer(4, 115, 122)
    layer4 = SoilLayer(1, 112)
    layer5 = SoilLayer(10, 125)

    # soil profile with water depth at the s
    soilprofile = SoilProfile(
        [layer1, layer2, layer3, layer4, layer5], zw=0, gammaw=62.4
    )

    output = []
    for layer in soilprofile.layers:
        output.append([layer.thickness, layer.gamma_bulk, layer.gamma_sat])

    required_ouput = [
        [5, 110, 120],
        [7, 115, 115],
        [4, 115, 122],
        [1, 112, 112],
        [10, 125, 125],
    ]
    assert output == required_ouput
