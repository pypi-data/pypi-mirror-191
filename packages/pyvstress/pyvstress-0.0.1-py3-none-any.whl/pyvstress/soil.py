import copy
from .exceptions import ParamError

# I have freely borrowed ideas from PYSRA may have even copied small parts of the code.
# ref: https://github.com/arkottke/pysra/blob/master/pysra/site.py


class AbsPoint:
    """Abstract point class"""

    def __init__(
        self,
        z=0,
        total_stress=0.0,
        pore_pressure=0.0,
        effective_stress=0.0,
        layer_index=0,
    ):
        """In most cases initilize with only the depth of the point and the rest are computed based on the location of the point in the soil layer.

        :param float z: distance below the ground surface.
        :param float total_stress: vertical total stress at the point
        :param float pore_pressure: porewater pressure at the point
        :param float effective_stress: vertical effective stress at the point
        :param int layer_index: index of the layer in which the point lies. 
        """

        self._z = z
        self._total_stress = total_stress
        self._pore_pressure = pore_pressure
        self._effective_stress = effective_stress
        self._layer_index = layer_index

    @property
    def z(self):
        """Return the depth of the point from the ground surface."""
        return self._z

    @property
    def total_stress(self):
        """Return the vertical total stress at the point."""
        return self._total_stress

    @total_stress.setter
    def total_stress(self, val):
        self._total_stress = val

    @property
    def pore_pressure(self):
        """Return the porewater pressure at the point."""
        return self._pore_pressure

    @pore_pressure.setter
    def pore_pressure(self, val):
        self._pore_pressure = val

    @property
    def effective_stress(self):
        """Return the vertical effective stress at the point."""
        return self._effective_stress

    @effective_stress.setter
    def effective_stress(self, val):
        self._effective_stress = val

    @property
    def layer_index(self):
        """Return the index of the layer in which the point lies"""
        return self._layer_index

    @layer_index.setter
    def layer_index(self, val):
        self._layer_index = val

    def is_in(self, layer):
        """Check if the point is within a layer. Points lying at the top of the layer is not considered within the layer.
        A separate special case is required for point lying at the bottom of the soil layer.
        layer: instance of layer object"""

        if ((self.z > layer.ztop) or abs(self.z - layer.ztop) < 0.01) and (
            self.z < layer.zbot
        ):
            return True
        else:
            return False

    def __repr__(self):
        return f"<Point(depth={self.z:0.2f}, total_stress={self.total_stress:0.2f}, pore_pressure={self.pore_pressure:0.2f}, effective_stress={self.effective_stress:0.2f})>"


class Point(AbsPoint):
    def __init__(self, z=0.0, layer_index=0):
        super().__init__(z=z, layer_index=layer_index)


class SoilLayer:
    """Class for soil layers, with layer properties."""

    def __init__(self, layer_thickness, gamma_bulk, gamma_sat=None, **kwargs):
        """
        :param float layer_thickness: thickness of the layer.
        :param float gamma_bulk: bulk unit weight of the layer.
        :param float gamma_sat: saturated unit weight of the layer.
        :param float phi: slope of the Mohr-Coulomb failure envelope, an effective stress strength parameter.
        :param float c: intercept of the Mohr-Coulomb, an effecitve stress strength parameter.
        :param float su: undrained shear strength, a total stress strength parameter.
        :param float fc: fines content, will be used for liquefaction triggering analysis.
        :param str soiltype: soil description, to be used in correlations.

        Use bulk unit weights for soil layers above the water table and saturated unit weights for layers below the water table
        """

        self._layer_thickness = layer_thickness
        self._gamma_bulk = gamma_bulk
        self._gamma_sat = gamma_bulk if gamma_sat == None else gamma_sat

        # saturated: Boolean, flag to indicate if the layer is saturated
        self._sat = False
        # these other properties are assigned by the Profile using layer update
        # the depth of the top and bottom of the layer in the soil profile, the top of the first profile has depth = 0
        self._ztop = 0
        self._zbot = 0
        # the vertical stress at the top of the layer
        self._overburden = 0

        # when kwargs are present
        self.__dict__.update(kwargs)

    def __getitem__(self, val):
        return self.__dict__[val]

    @property
    def thickness(self):
        """Depth to the top of the layer"""
        return self._layer_thickness

    @thickness.setter
    def thickness(self, val):
        """Set the layer thickness for the layer"""
        self._layer_thickness = val

    @property
    def gamma_bulk(self):
        """Bulk unit weight of the layer"""
        return self._gamma_bulk

    @property
    def gamma_sat(self):
        """Saturated unit weight of the layer"""
        return self._gamma_sat

    @property
    def ztop(self):
        """Return the depth of the top of the layer from the ground surface."""
        return self._ztop

    @ztop.setter
    def ztop(self, val):
        """Set the depth for layer top, ztop, from the ground surface."""
        self._ztop = val

    @property
    def zbot(self):
        """Return the depth of the bottom of the layer from the ground surface."""
        return self._zbot

    @zbot.setter
    def zbot(self, val):
        """Set the depth for layer bottom, zbot, from the ground surface."""
        self._zbot = val

    @property
    def sat(self):
        """Return if the saturation status of the layer"""
        return self._sat

    @sat.setter
    def sat(self, val):
        """Set the saturation status of the layer"""
        self._sat = val

    @property
    def overburden(self):
        """Return the total vertical stress at the top of the layer."""
        return self._overburden

    @overburden.setter
    def overburden(self, q):
        """Set the value for ztop vertical stress"""
        self._overburden = q

    def calc_inlayer_vertical_stress(self, depth):
        """Return total stress at a specified point within a layer
        depth: float, depth of the point below the top of the surface
        """
        if depth > self.thickness:
            raise ValueError(
                f"Depth {depth} cannot be greater than the layer thickness {self.thickness}."
            )

        if depth < 0:
            raise ValueError(
                f"Depth {depth} cannot be less than 0 (zero) {self.layer}."
            )
        if self.sat:
            return self.overburden + depth * self.gamma_sat
        else:
            return self.overburden + depth * self.gamma_bulk

    def __repr__(self):
        return f"<SoilLayer(layer_thickness={self._layer_thickness:0.1f}, gamma_bulk={self._gamma_bulk:0.2f}, gamma_sat={self._gamma_sat:0.2f}, overburden={self._overburden:0.2f}>"


class SoilProfile:
    def __init__(self, layers=[], zw=0, q=0.0, gammaw=62.4):
        """
        :param [] layers: a list of :class: `SoilLayer` objects.
        :param float zw: depth to groundwater, positive depth below groundlevel, negative depths above groundlevel
        :param float surcharge: surface surchage load
        :param float gammaw: float, unit weight of water, use consistent units, the units of the the computations is the units of `gammaw`
        """

        self._layers = layers
        self._zw = zw
        self._gammaw = gammaw
        self._saturation_zone = zw
        self._ztops = []
        self._zbots = []
        self._surcharge = q + self.water_stress()
        # compute layer top and layer bottom depths
        self.update_layer_depths()
        # save the soil layers depths before any subdivision, this will be only for internal use
        self._ztops_0 = [ztop for ztop in self.ztops]
        self._zbots_0 = [zbot for zbot in self.zbots]

        # divide the layers at the location of the groundwater table,
        # compute the depths to the top and bottom of the layer,
        # and compute overburden stress at the top of each layer
        self.update_profile()
        # self.assign_saturation_status()

    def __iter__(self):
        return iter(self._layers)

    def __contains__(self, value):
        return value in self._layers
        # return value in self.__dict__.keys()

    def __len__(self):
        return len(self._layers)

    def __getitem__(self, key):
        return self._layers[key]

    def index(self, layer):
        return self._layers.index(layer)

    def add_layer(self, layer):
        """Add a :class: `SoilLayer` to the end of the :class: `SoilProfile`
        
        :param layer: :class: `SoilLayer` instance
        """
        self._layers.append(layer)

    def insert(self, index, layer):
        """Insert a SoilLayer object into a list of SoilLayer objects in SoilProfile object."""
        self._layers.insert(index, layer)
        # self.update_profile(index)
        return self

    @property
    def layers(self):
        return self._layers

    @property
    def zw(self):
        return self._zw

    @property
    def saturation_zone(self):
        return self._saturation_zone

    @saturation_zone.setter
    def saturation_zone(self, val):
        if val > self.zw:
            raise ValueError(
                f"Saturation zone depth {self._saturation_zone:0.2f} must be at or above the water table depth {self.zw:0.2f}"
            )
        self._saturation_zone = val

    @property
    def ztops(self):
        """Return a list of depth to the top of the layers"""
        return self._ztops

    @ztops.setter
    def ztops(self, ztops):
        self._ztops = ztops

    @property
    def zbots(self):
        """Return a list of depth to bottom of the layers"""
        return self._zbots

    @zbots.setter
    def zbots(self, zbots):
        self._zbots = zbots

    @property
    def surcharge(self):
        """Return the surface surchage value
        :returns: external surcharge on the top of the soil profile
        :rtype: float
        """
        return self._surcharge

    @property
    def gammaw(self):
        """Return the unit weight of water
        :returns: unit weight of water
        :rtype: float
        """
        return self._gammaw

    def split_layer(self, z):
        """Split the layer into two layers if the depth z is not a layer boundary.
        i.e. ztop < z < zbot
        """

        for idx, layer in enumerate(self.layers):
            if self.ztops[idx] < z < self.zbots[idx]:
                dh = z - self.ztops[idx]
                if dh > layer.thickness:
                    raise ValueError(
                        f"Depth {dh} within a layer cannot be greater than the layer thickness {self._layer_thickness}."
                    )
                ilayer = copy.deepcopy(layer)
                layer_thickness = layer.thickness
                layer.thickness = dh
                ilayer.thickness = layer_thickness - dh
                self.insert(idx + 1, ilayer)
                break

    def set_saturation_flag(self):
        """Set a Boolean Flag, True if the layer is beneath the water table"""
        if abs(self.saturation_zone - self.zw) > 0.01:
            zw = self.saturation_zone
        else:
            zw = self.zw
        for ztop, layer in zip(self.ztops, self.layers):
            if abs(ztop - zw) < 0.01 or (ztop > zw):
                layer.sat = True
            else:
                layer.sat = False

    def update_profile(self):
        """Split the profile at the groundwater level and compute overburden stress at the top of each layer."""
        if (
            not any([abs(z - self.zw) < 0.01 for z in (self.ztops + [self.zbots[-1]])])
            and self.zw < self.zbots[-1]
        ):
            self.split_layer(self.zw)

        # update depths to the top and bottom of the layers after layer insertion
        self.update_layer_depths()

        # set saturation flag for layers
        self.set_saturation_flag()

        # compute overburden for each layer
        self.layers[0].overburden = self.surcharge
        for tlayer, blayer in zip(self.layers[0:-1], self.layers[1:]):
            blayer.overburden = tlayer.calc_inlayer_vertical_stress(tlayer.thickness)

    def water_stress(self):
        """If there is standing water then compute the total stress from the water on the soil profile."""
        if self.zw < 0:
            return -self.zw * self.gammaw
        else:
            return 0

    def update_layer_depths(self):
        """Update the depths to top of the layers"""

        self.ztops = [0]
        ztop = 0
        # update top of layers, ztops, for the profile
        for layer in self.layers[0:-1]:
            ztop += layer.thickness
            self.ztops.append(ztop)
        # update bottom of layers, zbots, for the profile
        self.zbots = [
            ztop + layer.thickness for ztop, layer in zip(self.ztops, self.layers)
        ]

        # update ztop and zbot for the layer as well
        for layer, ztop, zbot in zip(self.layers, self.ztops, self.zbots):
            layer.ztop = ztop
            layer.zbot = zbot

    def vertical_stresses(self, pts):
        """Compute total vertical stress, pore pressure, and effective stress at the specified points, depth below the ground surface

        :param pts: list of Point instances, depth below the surface at which stress is computed"""

        if isinstance(pts, list):
            pass
        else:
            pts = [pts]

        for pt in pts:
            pt.total_stress = self.calc_total_stress(pt)
            pt.pore_pressure = self.calc_pore_pressure(pt)
            pt.effective_stress = pt.total_stress - pt.pore_pressure

    def calc_total_stress(self, pt):
        """Compute total stress at the specified point, depth below the ground surface

        :param Point pt: Point instance"""

        for layer in self.layers:
            if pt.is_in(layer):
                depth = pt.z - layer.ztop
                return layer.calc_inlayer_vertical_stress(depth)

        # if there is a point at the bottom of the soil profile
        if abs(pt.z - self.layers[-1].zbot) < 0.01:
            depth = self.layers[-1].thickness
            return layer.calc_inlayer_vertical_stress(depth)

    def calc_pore_pressure(self, pt):
        """Compute pore pressure at the specified point, the water pressure with respect to the groundwater table
        :param pt: Point instance"""

        if pt.z > self.zw:
            return (pt.z - self.zw) * self._gammaw
        else:
            return 0.0

    def assign_layer_index(self, pt):
        """Assign layer index to the point
        :param pt: Point object"""
        for layer in self.layers:
            if pt.is_in(layer):
                pt.layer_index = self.index(layer)
            elif abs(pt.z - self.layers[-1].zbot) < 0.01:
                pt.layer_index = self.index(layer)

    # def soil_profile_points(self, analysis_type="vertical"):
    #     """Returns points for computing lateral earth pressures for the soil profile.
    #     Generate two points at all interior layer boundaries, one point at the top of the soil profile,
    #     and one point at the bottom of the soil profile. If the groundwater table is at the layer boundary
    #     then no additional points are required, but if the groundwater table is within a layer then add an
    #     additional point at the depth of the groundwater table.

    #     Two point at interior layer boundaries are required because the top layer and the bottom layer will
    #     have different values of phi  and c resulting in different lateral streses

    #     :param analysis_type: str,
    #         vertical: assigns a point at the soil profile top, one point each at the layer boundaries, and at
    #         groundwater table if it is not the same as the layer boundaries
    #         lateral: assigns a pont at the soil profile top, two points at each of the layer boundaries, and a
    #         point at the groundwater table if it is not the same as the layer boundaries
    #     """

    #     # abs to prevent -0.000 after subtracting delta_z and rounding
    #     ptts = [Point(z) for z in self._ztops_0]
    #     ptbs = [Point(z) for z in self._zbots_0]

    #     # these are points that fall on the top layer of the layer boundary
    #     for pt in ptts:
    #         self.assign_layer_index(pt)

    #     # these are points that fall on the bottom layer of the layer boundary
    #     for pt in ptbs:
    #         self.assign_layer_index(pt)

    #     if analysis_type == "vertical":
    #         # one point at the top of the profile, layer boundaries, bottom of the profile
    #         pts = ptts + [ptbs[-1]]
    #     elif analysis_type == "lateral":
    #         # reduce the index for all the points excepth the surface point
    #         for pt in ptts[1:]:
    #             pt.layer_index -= 1
    #         # combine the points on either side of the layer boundary
    #         pts = ptts + ptbs
    #     else:
    #         raise ValueError(
    #             f"{analysis_type} is not one of the acceptable arguments: 'vertical' or 'lateral' "
    #         )

    #     # add a point for the watertable if it is not one of the layer boundaries
    #     if not any([abs(pt.z - self.zw) < 0.01 for pt in pts]):
    #         ptz = Point(self.zw)
    #         self.assign_layer_index(ptz)
    #         pts.append(ptz)

    #     # sort the points per depth and then layer_index
    #     pts.sort(key=lambda pt: (pt.z, pt.layer_index))

    #     return pts

    # def generate_regular_points(self, analysis_type="vertical", dz=0.5):
    #     """Generate a list of points within the soil profile layer.

    #     Generate points, when possible, at equal intervals of dz.
    #     Points may not be dz apart near layer boundaries. Either one or two points
    #     are generated at internal layer boundaries based on whether the type of
    #     analysis involves vertical stresses, 1 point per boundary, or lateral stresses
    #     2 points per boundary.

    #     :param SoilProfile soilprofile: SoilProfile object
    #     :param float dz: maximum separation distance between points
    #     :param str analysis_type: type of analysis either 'vertical' or 'lateral'
    #     :returns: a list of Point objects, almost equally spaced over the soil profile
    #     :rtype: [Point]
    #     """

    #     # generate boundary points
    #     ptb = self.soil_profile_points(analysis_type)
    #     # depths and indices for interboundary points
    #     zs = []
    #     idxs = []
    #     for layer_idx, layer in enumerate(self):
    #         npts = int(math.floor(layer.thickness / dz) - 1)
    #         zs += [(layer.ztop + (idx + 1) * dz) for idx in range(npts)]
    #         idxs += [layer_idx] * npts

    #     # inter boundary points
    #     pti = [Point(z=z, layer_index=idx) for z, idx in zip(zs, idxs)]
    #     # all the pionts
    #     pts = ptb + pti
    #     pts.sort(key=lambda pt: (pt.z, pt.layer_index))
    #     return pts

    def get_params(self, pts, keylist):
        """Collect and return attribute values of layer object corresponding to point layer indices

        :param pts: [] of Point objects
        :param keylist: [] of class attributes as string
            class attributes for which the values are required"""
        params = []
        # first check all the layers have all the required keyword arguments, material parameters
        for layer in self:
            if not all(k in layer.__dict__.keys() for k in keylist):
                raise ParamError(
                    f"One or more keyword arguments, material parameters, missing in {layer}"
                )

        for pt in pts:
            params.append(
                [self.layers[pt.layer_index].__dict__[key] for key in keylist]
            )

        return params
