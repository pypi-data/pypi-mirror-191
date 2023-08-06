from pyvstress import SoilLayer, SoilProfile

# Description:


def main():
    # Create layers using the SoilLayer object, with the required parameters
    # SoilLayer(layer_thickness, gamma_bulk, gamma_sat)
    # layer_thickness and gamma_bulk are required soil parameters for each layer
    # if a value for gamma_sat is not provided then the value for gamma_bulk is used
    layer1 = SoilLayer(5, 110, 120)
    layer2 = SoilLayer(7, 115, 125)
    layer3 = SoilLayer(4, 115)
    layer4 = SoilLayer(1, 112, 120)
    layer5 = SoilLayer(10, 125)
    layers = [layer1, layer2, layer3, layer4, layer5]

    # create a soil profile by adding soil layers to the SoilProfile object
    # soil layers can only be added as a list during initialization as shown below.
    # Also required is the depth to groundwater, positive depth is below ground surface
    # and negative depth above the ground surface indicate standing water.
    # The default unit weight of water is 62.4 and thus gammaw can be omitted.
    # No units is assumed in the calculations, so the unit weight of water determines the unit
    soilprofile = SoilProfile(layers, zw=0.0, gammaw=62.4)

    # check the layers in the profile particularly in the second and last layer that
    # gamma_sat = gamma bulk
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
