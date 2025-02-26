import qplib.suspended.devices
from qplib.suspended.electrical import ElectricalConnectorOptions
import samplemaker.layout as smlay  # used for layout
from samplemaker.viewers import DeviceInspect
from qplib.suspended.waveguides import SuspendedWaveguideSequencer, SuspendedWaveguideAdapter
import samplemaker.layout as smlay
from samplemaker.viewers import GeomView
from samplemaker.viewers import DeviceInspect, GeomView
from samplemaker.devices import CreateDeviceLibrary, Device
import samplemaker.devices as smdev
from samplemaker.layout import GeomGroup
import numpy as np

# themask = smlay.Mask("QPLIB_ELE_PCWG_single")
themask = smlay.Mask("QPLIB_ELE_PCWG_table")
# themask = smlay.Mask("Bonding_pad_updated")

lslow_vals = [15, 40, 60, 100, 140, 40]
block_vals = [False, False, False, False, False, True]

class FranzKeldyshDevice(Device):
    def initialize(self):
        self.set_name("CUSTOM_FK")
        self.set_description("Device for on-chip photodetection")
    
    def parameters(self):
        self.addparameter("length_slow", 15, "Length of the slow section of the waveguide", float)
        self.addparameter("length_fast", 5, "Length of the fast section of the waveguide", float)
        self.addparameter("dev_height", 17.04, "Height of the waveguide + trench", float)
        self.addparameter("block_wg", False, "Whether the waveguide is a QPLIB_PC_BSF", bool)
        self.addparameter("mmi", False, "Whether we add MMI instead of grating couplers", bool)
        # The below values are different from the normal default, turns out these are the ideal ones
        self.addparameter("r", 0.07, "Hole radius", float)
        self.addparameter("a", 0.250, "Lattice constant", float)

    def geom(self):
        p = self.get_params()
        lslow = p["length_slow"]
        lfast = p["length_fast"]
        block_wg = p["block_wg"]
        mmi = p["mmi"]
        total_height = p["dev_height"]
        r = p["r"]
        a = p["a"]
        pw = 3
        fgca_xcenter = lslow/2 + 12
        fgca_ycenter =  total_height / 2 + 15#5
        offset = np.sqrt(30**2 - fgca_ycenter**2)
        if not block_wg:
            entry_list = [
                smdev.NetListEntry("QPLIB_ELE_PCWG_FK", 0, 0, "E", {"p1": "inA", "p2": "inB", "emesa": "inC"}, {"length_slow": lslow, "a": a, "r": r, "port_width": pw}),
                smdev.NetListEntry("QPLIB_FGCA", -fgca_xcenter, 0, "W", {"in": "inA"}, {}),
                smdev.NetListEntry("QPLIB_FGCA", -fgca_xcenter+offset, fgca_ycenter, "W", {"in": "inB"}, {}),                   
                # smdev.NetListEntry("QPLIB_ELE_BP", 0, -200, "E", {"bp": "inC"}, {}),
                smdev.NetListEntry("QPLIB_ELE_BP_EPO", 0, -200, "E", {"bp": "inC"}, {}),
                smdev.NetListEntry("QPLIB_ELE_BP", -240, -200, "E", {}, {"NType": True})
            ]
        else:
            entry_list = [
                smdev.NetListEntry("QPLIB_ELE_PCWG_BLOCK_FK", 0, 0, "E", {"p1": "inA", "p2": "inB", "emesa": "inC"}, {"length_slow": lslow, "a": a, "r": r, "port_width": pw}),
                smdev.NetListEntry("QPLIB_FGCA", fgca_xcenter-offset, fgca_ycenter, "E", {"in": "inA"}, {}),
                smdev.NetListEntry("QPLIB_FGCA", fgca_xcenter, 0, "E", {"in": "inB"}, {}),
                            
                #smdev.NetListEntry("QPLIB_ELE_BP", -0.5, -200, "E", {"bp": "inC"}, {}),
                smdev.NetListEntry("QPLIB_ELE_BP_EPO", 0, -200, "E", {"bp": "inC"}, {}),
                smdev.NetListEntry("QPLIB_ELE_BP", -240, -200, "E", {}, {"NType": True})
            ]        
        if mmi and not block_wg:
            wg_length_offset = 0.432500001
            nanobeam_length = lslow + 2 * lfast + wg_length_offset
            # entry_list[0] = smdev.NetListEntry("QPLIB_ELE_PCWG_FK", 0, 0, "E", {"p1": "inA", "p2": "inB", "emesa": "inC"}, {"length_slow": lslow, "a": a, "r": r, "nanobeam": True})
            # entry_list[1] = smdev.NetListEntry("QPLIB_MMI2x2", -fgca_xcenter - 25, total_height/3 + 1.75, "E", {"p2": "inD", "p4": "inA"}, {"offset": total_height/2, "width": 15})
            entry_list[0] = smdev.NetListEntry("QPLIB_ELE_WG_FK", 0, 0, "E", {"p1": "inA", "p2": "inB", "emesa": "inC"}, {"wg_length": nanobeam_length, "port_width": pw})
            entry_list[1] = smdev.NetListEntry("QPLIB_DCPL", -fgca_xcenter - 30, 15, "E", {"p1": "inE", "p2": "inD", "p3": "inF", "p4": "inA"}, {"input_dist": 30-1.5})
            entry_list[2] = smdev.NetListEntry("QPLIB_DCPL", fgca_xcenter + 30, 15, "E", {"p1": "inD", "p2": "inG", "p3": "inB", "p4": "inH"}, {"input_dist": 30-1.5})
            entry_list.append(smdev.NetListEntry("QPLIB_FGCA", -fgca_xcenter - 60, 30, "W", {"in": "inE"}, {})) 
            entry_list.append(smdev.NetListEntry("QPLIB_FGCA", -fgca_xcenter - 60, 0, "W", {"in": "inF"}, {}))                                 
            entry_list.append(smdev.NetListEntry("QPLIB_FGCA", fgca_xcenter + 60, 30, "E", {"in": "inG"}, {}))
            entry_list.append(smdev.NetListEntry("QPLIB_FGCA", fgca_xcenter + 60, 0, "E", {"in": "inH"}, {}))                                  
            # entry_list[2] = smdev.NetListEntry("QPLIB_DCPL", fgca_xcenter + 25, total_height/2 + 0.75 - 2, "E", {"p1": "inD", "p3": "inB"}, {"input_dist": total_height-4})
        
        netlist = smdev.NetList(f"my_circuit", entry_list)
        cir = smdev.Circuit.build()
        cir.set_param("NETLIST",netlist)
        g = cir.run()
        g = g.flatten()
        g.boolean_union(11)

        trenchW = ElectricalConnectorOptions["PType_trench_width"]
        epo_offset = 4.5#1.5
        epo_width = trenchW + 2 * epo_offset
        shell_offset = trenchW
        n_shell = 4


        epolay = g.copy().select_layer(11).poly_resize(epo_offset, 11)
        epolay.set_layer(8)
        g+=epolay
        for i in range(n_shell):
            shell = epolay.copy()
            shell.poly_outlining(shell_offset, 8, distance=i*shell_offset)
            shell.set_layer(18 + i)
            g += shell
        layer11 = g.select_layer(11)
        layer11.set_layer(7)
        g = g.deselect_layers([11]) + layer11
        return g


class AlignmentWaveguideDevice(Device):
    def initialize(self):
        self.set_name("ALIGNMENT_WAVEGUIDE_DEVICE")
        self.set_description("Photonic crystal waveguide or nanobeam waveguide for alignment.")
        self._seq = SuspendedWaveguideSequencer([])
    
    def parameters(self):
        self.addparameter("length_slow", 15, "Length of the slow section of the waveguide", float)
        self.addparameter("length_fast", 5, "Length of the fast section of the waveguide", float)
        self.addparameter("nanobeam", False, "Whether the waveguide is a nanobeam waveguide.", bool)
        # The below values are different from the normal default, turns out these are the ideal ones
        self.addparameter("r", 0.07, "Hole radius", float)
        self.addparameter("a", 0.250, "Lattice constant", float)
    
    def geom(self):
        p = self.get_params()
        lslow = p["length_slow"]
        lfast = p["length_fast"]        
        r = p["r"]
        a = p["a"]
        nanobeam = p["nanobeam"]
        wg_length_offset = 0.432500001
        nanobeam_length = lslow + 2 * lfast + wg_length_offset
        pcw_centers = [12.582500000500001, 25.082500000499998, 35.082500000500005, 55.08250000050001, 75.0825000005]
        pcw_center_dict = dict(zip(lslow_vals[:-1], pcw_centers))
        pcw_center = pcw_center_dict[lslow]
        fgca_xcenter = lslow/2 + 12
        fgca_ycenter =  21#13
        offset = np.sqrt(30**2 - fgca_ycenter**2)

        if not nanobeam:
            entry_list = [
            smdev.NetListEntry("QPLIB_PC_FSF", 0, 0, "E", {"p1": "inA", "p2": "inB"}, {"length_slow": lslow, "a": a, "r": r}),
            smdev.NetListEntry("QPLIB_FGCA", -fgca_xcenter+pcw_center, 0, "W", {"in": "inA"}, {}),
            smdev.NetListEntry("QPLIB_FGCA", -fgca_xcenter+offset+pcw_center, fgca_ycenter, "W", {"in": "inB"}, {}),                   
            ]
            # entry_list = [
            # smdev.NetListEntry("QPLIB_PC_FSF", 0, 0, "E", {"p1": "inA", "p2": "inB"}, {"length_slow": lslow, "a": a, "r": r}),
            # smdev.NetListEntry("QPLIB_FGCA", -fgca_xcenter+pcw_center, 0, "W", {"in": "inA"}, {}),
            # smdev.NetListEntry("QPLIB_FGCA", fgca_xcenter+pcw_center, 0, "E", {"in": "inB"}, {}),                   
            # ]
            netlist = smdev.NetList(f"my_circuit", entry_list)
            cir = smdev.Circuit.build()
            cir.set_param("NETLIST",netlist)
            g = cir.run()
        else:
            self._seq.options["tetherAuto"] = True
            if lslow <= 30:
                seq = [["DEV", "QPLIB_FGCA", "in", "in"], ["S", nanobeam_length], ["DEV", "QPLIB_FGCA", "in", "in"]]
            else:
                up = 13#5
                second_coupler_right = np.sqrt(30**2 - up**2)
                long_straight = (nanobeam_length + second_coupler_right - up) / 2
                short_straight = long_straight - second_coupler_right
                bend_radius = 3
                seq = [["DEV", "QPLIB_FGCA", "in", "in"], ["S", long_straight - bend_radius], ["B",90,bend_radius], ["S", up - bend_radius], ["B",90,bend_radius], ["S", short_straight - bend_radius], ["DEV", "QPLIB_FGCA", "in", "in"]]

                # straight = 30
                # down = (nanobeam_length - straight) / 2
                # seq = [["DEV", "QPLIB_FGCA", "in", "in"], ["S", down], ["B",90,3], ["S", straight], ["B",90,3], ["S", down], ["DEV", "QPLIB_FGCA", "in", "in"]]
            self._seq.reset()
            self._seq.seq = seq
            g = self._seq.run()
            # if lslow > 30:     
            #     g.rotate(g.bounding_box().cx(), g.bounding_box().cy(), -90)       
        return g

class GratingCouplerLossDevice(Device):
    def initialize(self):
        self.set_name("GS_LOSS")
        self.set_description("Device for testing the loss of grating coupler.")
        self._seq = SuspendedWaveguideSequencer([])
    
    def parameters(self):
        self.addparameter("length", 15, "Length of the waveguide", float)
    
    def geom(self):
        p = self.get_params()
        l = p["length"]
        seq = [["DEV", "QPLIB_FGCA", "in", "in"], ["S", l], ["DEV", "QPLIB_FGCA", "in", "in"]]
        self._seq.reset()
        self._seq.seq = seq
        g = self._seq.run()
        return g

## bbs 12.582500000500001, 25.082500000499998, 35.082500000500005, 55.08250000050001, 75.0825000005
dev = FranzKeldyshDevice.build()
dev1 = AlignmentWaveguideDevice.build()
dev2 = GratingCouplerLossDevice.build()

# g = dev.geom()


tab = smlay.DeviceTable(dev, 1, 6, {}, {"length_slow": lslow_vals, "block_wg": block_vals})
tab.set_device_rotation(180)
tab.auto_align(100, 100)

tab2 = smlay.DeviceTable(dev, 3, 1, {"length_slow": lslow_vals[0:3], "block_wg": block_vals[0:3]}, {})
tab2.set_device_rotation(-90)
tab2.auto_align(100, 100)

tab3 = smlay.DeviceTable(dev, 3, 1, {"length_slow": lslow_vals[3:], "block_wg": block_vals[3:]}, {})
tab3.set_device_rotation(90)
tab3.auto_align(100, 100)

tab4 = smlay.DeviceTable(dev, 1, 6, {"mmi": [True]}, {"length_slow": lslow_vals, "block_wg": block_vals})
tab4.auto_align(100, 100)

tab5 = smlay.DeviceTable(dev1, 4, 5, {"nanobeam": [False, False, True, True]}, {"length_slow": lslow_vals[:-1]})
tab5.auto_align(100, 100)

tab6 = smlay.DeviceTable(dev2, 4, 1, {}, {})
tab6.auto_align(100, 100)

themask.addDeviceTable(tab, 0, 50)
themask.addDeviceTable(tab2, -1600, -1000)
themask.addDeviceTable(tab3, 1600, -1000)
themask.addDeviceTable(tab4, 0, -2050)
themask.addDeviceTable(tab5, 0, -800)
themask.addDeviceTable(tab6, 600, -800)

# themask.addToMainCell(g)

themask.exportGDS()

"""
Trench around bp should be on layer 7?.
Maybe remove bridge on layer 8?
Do weird "stairs" thing around bonding pad,
make a line in the bonding bad going up to the
circuit which also has the "stairs" around it

Three QDs:

We have the four "shell" layers, 18, 19, 20, 21.

Inside the bonding pad (not just around), there is another trench
(the thin red one). This is the one just called "trench" and it is
on layer 1.
The way that trench is initialized is the following. First, they just
select layer 5 of the bonding pad. This is basically just what they
later call base_metal (indeed, base_metal is just a copy of this and
resized to -1, which I'm not sure what that is, I guess flipping it?)
Then, trench is assigned to the shrinked outlining of its original,
making it go from something that covers the entire bonding pad to a thin
trench.


All around "trench", there is another copy of it that is resized to be thicker.
This is on layer 8 and is referred to as "epolay" in the code, presumably
"epoxy layer.

top_metal is just as it sounds, the whole metal of the bonding pad.

base_metal (layer 5) is a weird thing that we don't need anyway.

Curve the waveguides so that they are roughly 30 microns away from each other

Change the layout so that the bonding pad is on the outside.

In the connection between the electrical contact and the bonding pad,
we should not remove the layer below the metal.

Add a nanobeam waveguide above the top row of each column for alignment.

Add one QPLIB_PC_BSF

"""
