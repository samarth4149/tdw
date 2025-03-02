from pkg_resources import resource_filename
from pathlib import Path
from json import loads
from typing import Dict
from tdw.obi_data.fluids.fluid_base import FluidBase


class Fluid(FluidBase):
    """
    Data for an Obi fluid. For more information, [read this](http://obi.virtualmethodstudio.com/tutorials/emittermaterials.html).
    """

    def __init__(self, smoothing: float, surface_tension: float, viscosity: float, vorticity: float,
                 reflection: float, transparency: float, refraction: float, capacity: int, resolution: float,
                 color: Dict[str, float], rest_density: float, buoyancy: float = -1, diffusion: float = 0,
                 diffusion_data: Dict[str, float] = None, atmospheric_drag: float = 0, atmospheric_pressure: float = 0,
                 particle_z_write: bool = False, thickness_cutoff: float = 1.2, thickness_downsample: int = 2,
                 blur_radius: float = 0.02, surface_downsample: int = 1, render_smoothness: float = 0.8,
                 metalness: float = 0, ambient_multiplier: float = 1, absorption: float = 5,
                 refraction_downsample: int = 1, foam_downsample: int = 1, radius_scale: float = 1.7,
                 random_velocity: float = 0):
        """
        :param smoothing: A rendering parameter that controls the radius of the particle.
        :param surface_tension: Increasing this value will make the fluid try to minimize its surface area, causing spherical drops to form.
        :param viscosity: Viscosity smooths out the velocity field generated by fluid particles when moving.
        :param vorticity: Amount of vorticity confinement, it will contribute to maintain vortical details in the fluid.
        :param reflection: Amount of reflection.
        :param transparency: Amount of fluid transparency.
        :param refraction: Amount of light refraction. This effect is more noticeable in thicker regions of the fluid.
        :param capacity: The maximum amount of emitted particles.
        :param resolution: The size and amount of particles in 1 cubic meter.
        :param color: The visual color of the fluid.
        :param rest_density: The fluid density in kg/m3.
        :param buoyancy: Controls the relative density between the fluid and the surrounding air.
        :param diffusion: A diffusion value that will modify `diffusion_data`. [Read this for more information.](http://obi.virtualmethodstudio.com/tutorials/particlediffusion.html)
        :param diffusion_data: A dictionary of four floats that can be used arbitrarily, for example to colorize a fluid based on its physical state. [Read this for more information.](http://obi.virtualmethodstudio.com/tutorials/particlediffusion.html)
        :param atmospheric_drag: The amount of air resistance.
        :param atmospheric_pressure: The amount of inward pressure applied by air on the surface of the fluid.
        :param particle_z_write: A shader rendering flag. This should be false for semi-transparent objects and true for opaque objects.
        :param thickness_cutoff: A threshold for rendering fluid thickness. Regions that are less thick than this are discarded.
        :param thickness_downsample: Increase this value to use a lower-resolution rendering buffer.
        :param blur_radius: Amount of depth blurring applied before generating normals. Higher values will result in a smoother surface.
        :param surface_downsample: Downsampling of the depth/normals buffers. Increase it to use lower-resolution buffers.
        :param render_smoothness: Surface smoothness of the fluid. High values will result in small specular glints, lower values will result in a rougher-looking surface.
        :param metalness: Controls reflection metalness: high values will cause reflection/specular to be tinted with the fluid's surface color.
        :param ambient_multiplier: A parameter that affects the fluid vis a vis the ambient lighting.
        :param absorption: How much light is absorbed by the fluid, as light travels trough it: higher values will tint the background with the fluid color.
        :param refraction_downsample: Downsampling of the refraction buffers. Increase it to use a lower-resolution buffer.
        :param foam_downsample: Downsampling of the foam buffer. Increase it to use a lower-resolution buffer.
        :param radius_scale: This scales the size at which particles are drawn.
        :param random_velocity: Random velocity of emitted particles.
        """

        super().__init__(capacity=capacity, resolution=resolution, color=color, rest_density=rest_density,
                         radius_scale=radius_scale, random_velocity=random_velocity)

        """:field
        A rendering parameter that controls the radius of the particle.
        """
        self.smoothing: float = smoothing
        """:field
        Increasing this value will make the fluid try to minimize its surface area, causing spherical drops to form.
        """
        self.surface_tension: float = surface_tension
        """:field
        Viscosity smooths out the velocity field generated by fluid particles when moving.
        """
        self.viscosity: float = viscosity
        """:field
        Amount of vorticity confinement, it will contribute to maintain vortical details in the fluid.
        """
        self.vorticity: float = vorticity
        """:field
        Amount of reflection.
        """
        self.reflection: float = reflection
        """:field
        Amount of fluid transparency.
        """
        self.transparency: float = transparency
        """:field
        Amount of light refraction. This effect is more noticeable in thicker regions of the fluid.
        """
        self.refraction: float = refraction
        """:field
        Controls the relative density between the fluid and the surrounding air.
        """
        self.buoyancy: float = buoyancy
        """:field
        A diffusion value that will modify `diffusion_data`. [Read this for more information.](http://obi.virtualmethodstudio.com/tutorials/particlediffusion.html)
        """
        self.diffusion: float = diffusion
        if diffusion_data is None:
            """:field
            A dictionary of four floats that can be used arbitrarily, for example to colorize a fluid based on its physical state. [Read this for more information.](http://obi.virtualmethodstudio.com/tutorials/particlediffusion.html)
            """
            self.diffusion_data: Dict[str, float] = {"x": 0, "y": 0, "z": 0, "w": 0}
        else:
            self.diffusion_data = diffusion_data
        """:field
        The amount of air resistance.
        """
        self.atmospheric_drag: float = atmospheric_drag
        """:field
        The amount of inward pressure applied by air on the surface of the fluid.
        """
        self.atmospheric_pressure: float = atmospheric_pressure
        """:field
        A shader rendering flag. This should be false for semi-transparent objects and true for opaque objects.
        """
        self.particle_z_write: bool = particle_z_write
        """:field
        A threshold for rendering fluid thickness. Regions that are less thick than this are discarded.
        """
        self.thickness_cutoff: float = thickness_cutoff
        """:field
        Increase this value to use a lower-resolution rendering buffer.
        """
        self.thickness_downsample: int = thickness_downsample
        """:field
        Amount of depth blurring applied before generating normals. Higher values will result in a smoother surface.
        """
        self.blur_radius: float = blur_radius
        """:field
        Downsampling of the depth/normals buffers. Increase it to use lower-resolution buffers.
        """
        self.surface_downsample: int = surface_downsample
        """:field
        Surface smoothness of the fluid. High values will result in small specular glints, lower values will result in a rougher-looking surface.
        """
        self.render_smoothness: float = render_smoothness
        """:field
        Controls reflection metalness: high values will cause reflection/specular to be tinted with the fluid's surface color.
        """
        self.metalness: float = metalness
        """:field
        A parameter that affects the fluid vis a vis the ambient lighting.
        """
        self.ambient_multiplier: float = ambient_multiplier
        """:field
        How much light is absorbed by the fluid, as light travels trough it: higher values will tint the background with the fluid color.
        """
        self.absorption: float = absorption
        """:field
        Downsampling of the refraction buffers. Increase it to use a lower-resolution buffer.
        """
        self.refraction_downsample: int = refraction_downsample
        """:field
        Downsampling of the foam buffer. Increase it to use a lower-resolution buffer.
        """
        self.foam_downsample: int = foam_downsample

    def _get_type(self) -> str:
        return "fluid"


def __get() -> Dict[str, Fluid]:
    data = loads(Path(resource_filename(__name__, "data/fluids.json")).read_text())
    materials = dict()
    for k in data:
        materials[k] = Fluid(**data[k])
    return materials


FLUIDS: Dict[str, Fluid] = __get()
