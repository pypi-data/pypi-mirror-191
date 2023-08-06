from pyvstress import SoilLayer, SoilProfile

# Description: Subdivision of layer at the depth of groundwater


def main():

    # create soil layers
    layer1 = SoilLayer(5, 110, 120)
    layer2 = SoilLayer(7, 115, 125)
    layer3 = SoilLayer(4, 115)
    layer4 = SoilLayer(1, 112, 120)
    layer5 = SoilLayer(10, 125)
    layers = [layer1, layer2, layer3, layer4, layer5]

    # create soil profile with groundwater within a soil layer
    soilprofile = SoilProfile(layers, zw=10)

    print("The soil layers:")
    print(
        f"{'ztop [ft]':>10s}, {'zbot [ft]':>10s}, {'layer_thickness':>20s}, {'gamma_bulk':>15s}, {'gamma_sat':>15s}"
    )
    for layer in soilprofile:
        print(
            f"{layer.ztop:>10.2f}, {layer.zbot:>10.2f}, {layer.thickness:>20.2f}, {layer.gamma_bulk:>15.2f}, {layer.gamma_sat:>15.2f}"
        )


if __name__ == "__main__":
    main()
