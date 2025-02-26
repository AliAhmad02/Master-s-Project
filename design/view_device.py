from qplib.suspended.devices import E_PC_Waveguide_FK
from qplib.suspended.devices import E_PC_Waveguide
import samplemaker.layout as smlay # used for layout 
from samplemaker.viewers import DeviceInspect
from qplib.suspended.waveguides import SuspendedWaveguideSequencer
import samplemaker.layout as smlay
from samplemaker.viewers import GeomView
from samplemaker.viewers import DeviceInspect
from samplemaker.devices import CreateDeviceLibrary, Device

dev_name = "QPLIB_ELE_BP_EPO"
# dev_name = "QPLIB_ELE_BP"
themask = smlay.Mask(f'check {dev_name}')

# seq = [["S", 10], ["DEV","QPLIB_ELE_PCWG_FK","p1","p2"], ["S", 10]]
# seq = [["S", 10], ["DEV",f"{dev_name}","p1","p2"], ["S", 10]]
# Step 2 pass the sequence to the sequencer initializer
# sequencer = SuspendedWaveguideSequencer(seq)
# geomE = sequencer.run()

# geomE=geomE.flatten()
# GeomView(geomE)
dev = Device.build_registered(f"{dev_name}")
tab = smlay.DeviceTable(dev, 1, 1, {}, {})
themask.addDeviceTable(tab, 0, 0)


# DeviceInspect(Device.build_registered(f"{dev_name}"))
# Let's add all to main cell
# themask.addToMainCell(geomE)    

# Export to GDS
themask.exportGDS()


""""
layers:
1: orange
2: Green (newly added isolation layer)
3: Red
4: Some sort of purple-ish color (unused)
5: Brown (contact-color)
6: Pink (unused)
7: Grey (unused)


Questions:

1) The waveguide is not symmetrical. Is that an issue?

2) What layers should the different things be on? It's random now.

3) The isolation I've added now is just a polygon? Does it need
to be turned into a trench or something?

4) What about sizes? Basically everything is the default size.
Does this need to be adjustable? Some things are hard-coded now.

5) Is it realistic to simulate this in COMSOL?

6) I'm assuming I need to shield around the bonding pad. How can
I do this, if the geometry of the bonding pad is not accessible?

7) What exactly was the bridge that I needed to add, again?

8) Does the current design seem well-isolated? Gaps too big?

Put the green mask at layer 7 (DONE).

Change trench width so the two parts meet, bonding pad (DONE)

Change thickness of metal (Easy to do, need to ask what thickness we need)

Add one more slightly wider thing on the metal, on a different layer (DONE)

Just add an n-contact next to the p-contact (DONE)

Each structure should have a pair of bonding pads (DONE)

slow light area, sweep 40um-140um in steps of 20 (5 columns) and 3 rows.
"""