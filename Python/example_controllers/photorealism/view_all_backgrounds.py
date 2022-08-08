from tdw.add_ons.image_capture import ImageCapture
from tdw.add_ons.third_person_camera import ThirdPersonCamera
from tdw.backend.paths import EXAMPLE_CONTROLLER_OUTPUT_PATH
from tdw.controller import Controller
from tdw.librarian import HDRISkyboxLibrarian
from pathlib import Path
import imageio
import os

"""
Add an HDRI skybox to the scene and rotate it.
"""

if __name__ == '__main__':
    c = Controller(launch_build=False, port=1071)
    hdri_skybox_librarian = HDRISkyboxLibrarian()
    skyboxes = [
        record for record in hdri_skybox_librarian.records
        if record.location != 'interior' and record.sun_elevation >= 120
    ]
    camera = ThirdPersonCamera(avatar_id="a",
                            position={"x": -4.28, "y": 0.85, "z": 4.27},
                            look_at={"x": 0, "y": 0, "z": 0})
    object_id = c.get_unique_id()
    c.communicate([{'$type':'load_scene', 'scene_name':'ProcGenScene'},
                    c.get_add_object(model_name="alma_floor_lamp",
                                            object_id=object_id,
                                            rotation={"x": 0, "y": 90, "z": 0}),
                    {"$type": "set_post_exposure",
                        "post_exposure": 0.6},
                    {"$type": "set_contrast",
                        "contrast": -20},
                    {"$type": "set_saturation",
                        "saturation": 10},
                    {"$type": "set_screen_space_reflections",
                        "enabled": False},
                    {"$type": "set_shadow_strength",
                        "strength": 1.0}
                   ])

    for skybox in skyboxes:
        path = Path(f'~/tmp/tdw_backgrounds/{skybox.name}').expanduser()
        os.makedirs(path, exist_ok=True)
        capture = ImageCapture(avatar_ids=["a"], path=path)
        c.add_ons.extend([camera, capture])
        c.communicate([c.get_add_hdri_skybox(skybox.name),])
        # Rotate the skybox.
        for i in range(24):
            c.communicate([{"$type": "look_at",
                            "object_id": object_id,
                            "use_centroid": True},
                        {"$type": "rotate_hdri_skybox_by",
                            "angle": 15}])
        images = []
        for i in range(24):
            images.append(imageio.imread(path/f'img_{i}.jpg'))
        imageio.mimsave(path/'background.gif', images, duration=0.1)
            
    c.communicate({"$type": "terminate"})
