from pyvstress import Point, SoilLayer, SoilProfile

# Description: Test Point.is_in() function. If the point, zp, is ztop > zp < zbot
# the function should return True


def test_point_01():

    # soillayers
    layer1 = SoilLayer(5, 110, 120)
    layer2 = SoilLayer(7, 115, 125)
    layer3 = SoilLayer(4, 115, 122)
    layer4 = SoilLayer(1, 112, 120)
    layer5 = SoilLayer(10, 125, 135)
    layers = [layer1, layer2, layer3, layer4, layer5]

    # soil profile
    soilprofile = SoilProfile(layers, zw=12, q=0, gammaw=62.4)

    # location of point below the ground surface
    pt1 = Point(z=15.5)

    output = []
    for ztop, zbot, layer in zip(
        soilprofile.ztops, soilprofile.zbots, soilprofile.layers
    ):
        output.append(
            [
                ztop,
                zbot,
                pt1.is_in(layer),
            ]
        )

    # required output
    required_output = [
        [0, 5, False],
        [5, 12, False],
        [12, 16, True],
        [16, 17, False],
        [17, 27, False],
    ]

    assert output == required_output
