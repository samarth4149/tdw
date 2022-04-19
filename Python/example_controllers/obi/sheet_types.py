from tdw.controller import Controller
from tdw.tdw_utils import TDWUtils
from tdw.add_ons.obi import Obi
from tdw.add_ons.third_person_camera import ThirdPersonCamera
from tdw.obi_data.cloth.sheet_type import SheetType

"""
Example of different sheet types.
"""

c = Controller()
camera = ThirdPersonCamera(position={"x": 0, "y": 8, "z": 5},
                           look_at={"x": 0, "y": 1.25, "z": 0})
obi = Obi()
c.add_ons.extend([camera, obi])
# Create cloth sheets, each with a different type.
obi.create_cloth_sheet(cloth_material="cotton",
                       object_id=Controller.get_unique_id(),
                       position={"x": -4, "y": 2, "z": 0},
                       rotation={"x": 30, "y": 0, "z": 0},
                       sheet_type=SheetType.cloth)
obi.create_cloth_sheet(cloth_material="cotton",
                       object_id=Controller.get_unique_id(),
                       position={"x": -2, "y": 2, "z": 0},
                       rotation={"x": 30, "y": 0, "z": 0},
                       sheet_type=SheetType.cloth_hd)
obi.create_cloth_sheet(cloth_material="cotton",
                       object_id=Controller.get_unique_id(),
                       position={"x": 2, "y": 2, "z": 0},
                       rotation={"x": 30, "y": 0, "z": 0},
                       sheet_type=SheetType.cloth_vhd)
c.communicate(TDWUtils.create_empty_room(12, 12))
for i in range(150):
    c.communicate([])
c.communicate({"$type": "terminate"})
