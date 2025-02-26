from qplib.suspended.devices import E_PC_Waveguide
import samplemaker.layout as smlay  # used for layout
from samplemaker.viewers import DeviceInspect
from qplib.suspended.waveguides import SuspendedWaveguideSequencer
import samplemaker.layout as smlay
from samplemaker.viewers import GeomView
from samplemaker.viewers import DeviceInspect, GeomView
from samplemaker.devices import CreateDeviceLibrary, Device
import samplemaker.devices as smdev
from samplemaker.layout import GeomGroup


themask = smlay.Mask("QPLIB_ELE_PCWG_test")

class FranzKeldyshDevice(Device):
    def initialize(self):
        self.set_name("CUSTOM_FK")
        self.set_description("Device for on-chip photodetection")
    
    def parameters(self):
        self.addparameter("length_slow", 10, "Length of the slow section of the waveguide", float)
        # self.addparameter("length_fast", 10, "Length of the slow section of the waveguide", float)
        self.addparameter("dev_height", 17.04, "Height of the waveguide + trench", float)

    
    def geom(self):
        offset = 3
        p = self.get_params()
        lslow = p["length_slow"]
        total_height = p["dev_height"]
        fgca_xcenter = lslow/2 + 12 #15
        fgca_ycenter =  total_height / 2 + 5
        entry_list = [
        smdev.NetListEntry("QPLIB_ELE_PCWG", 0, 0, "E", {"p1": "inA", "p2": "inB", "emesa": "inC"}, {"length_slow": lslow}),
        smdev.NetListEntry("QPLIB_FGCA", -fgca_xcenter, fgca_ycenter, "N", {"in": "inA"}, {}),
        smdev.NetListEntry("QPLIB_FGCA", fgca_xcenter, fgca_ycenter-offset, "W", {"in": "inB"}, {}),
        smdev.NetListEntry("QPLIB_ELE_BP", 0, -200, "E", {"bp": "inC"}, {}),
        smdev.NetListEntry("QPLIB_ELE_BP", -230, -200, "E", {}, {"NType": True})
        ]

        netlist = smdev.NetList(f"my_circuit", entry_list)
        # netlist.set_aligned_ports(["inA", "inB"])
        cir = smdev.Circuit.build()
        cir.set_param("NETLIST",netlist)
        g = cir.run()
        return g

dev = FranzKeldyshDevice.build()

dev.set_param("length_slow", 15)
g = dev.geom()

themask.addToMainCell(g)

themask.exportGDS()
