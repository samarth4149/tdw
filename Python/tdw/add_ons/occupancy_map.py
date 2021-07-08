from typing import List, Dict, Optional, Tuple
import numpy as np
from tdw.output_data import OutputData, Raycast, Overlap
from tdw.add_ons.add_on import AddOn
from tdw.scene.scene_bounds import SceneBounds


class OccupancyMap(AddOn):
    _RAYCAST_Y: float = 100

    def __init__(self):
        super().__init__()
        self.occupancy_map: Optional[np.array] = None
        self.scene_bounds: Optional[SceneBounds] = None
        self._cell_size: float = -1
        self._occupancy_map_size: Tuple[int, int] = (0, 0)

    def get_initialization_commands(self) -> List[dict]:
        return [{"$type": "send_environments"}]

    def on_send(self, resp: List[bytes]) -> None:
        def __get_islands() -> List[List[Tuple[int, int]]]:
            """
            :return: A list of all islands, i.e. continuous zones of traversability on the occupancy map.
            """

            # Positions that have been reviewed so far.
            traversed: List[Tuple[int, int]] = []
            islands: List[List[Tuple[int, int]]] = list()

            for ox, oy in np.ndindex(self.occupancy_map.shape):
                op = (ox, oy)
                if op in traversed:
                    continue
                # Fill the island (a continuous zone) that position `p` belongs to.
                to_check: List[tuple] = [op]
                island: List[Tuple[int, int]] = list()
                while len(to_check) > 0:
                    # Check the next position.
                    op = to_check.pop(0)
                    if op[0] < 0 or op[0] >= self.occupancy_map.shape[0] or op[1] < 0 or \
                            op[1] >= self.occupancy_map.shape[1] or \
                            self.occupancy_map[op[0]][op[1]] != 0 or op in island:
                        continue
                    # Mark the position as traversed.
                    island.append(op)
                    # Check these neighbors.
                    px, py = op
                    to_check.extend([(px, py + 1),
                                     (px + 1, py + 1),
                                     (px + 1, py),
                                     (px + 1, py - 1),
                                     (px, py - 1),
                                     (px - 1, py - 1),
                                     (px - 1, py),
                                     (px - 1, py + 1)])
                if len(island) > 0:
                    for island_position in island:
                        traversed.append(island_position)
                    islands.append(island)
            return islands

        # Set the scene bounds.
        if self.scene_bounds is None:
            self.scene_bounds = SceneBounds(resp=resp)
        if self.occupancy_map is None:
            # Generate the occupancy map.
            self.occupancy_map = np.zeros(shape=(self._occupancy_map_size[0] + 1, self._occupancy_map_size[1] + 1),
                                          dtype=int)
            # Get all of the positions that are actually in the environment.
            hit_env: Dict[int, bool] = dict()
            # Get all of the overlaps to determine if there was an object.
            hit_obj: Dict[int, bool] = dict()
            for i in range(len(resp) - 1):
                r_id = OutputData.get_data_type_id(resp[i])
                if r_id == "rayc":
                    raycast = Raycast(resp[i])
                    hit_env[raycast.get_raycast_id()] = raycast.get_hit()
                elif r_id == "over":
                    overlap = Overlap(resp[i])
                    hit_obj[overlap.get_id()] = len(overlap.get_object_ids()) > 0

            for cast_id in hit_env:
                idx = cast_id % 10000
                idz = int((cast_id - (cast_id % 10000)) / 10000)
                # The position is outside of the environment.
                if not hit_env[cast_id]:
                    self.occupancy_map[idx][idz] = -1
                # The position is occupied by at least one object.
                elif hit_obj[cast_id]:
                    self.occupancy_map[idx][idz] = 1
                # The position is free.
                else:
                    self.occupancy_map[idx][idz] = 0
            # Assume that the edges of the occupancy map are out of bounds.
            for ix, iy in np.ndindex(self.occupancy_map.shape):
                if ix == 0 or ix == self.occupancy_map.shape[0] - 1 or iy == 0 or \
                        iy == self.occupancy_map.shape[1] - 1:
                    self.occupancy_map[ix][iy] = -1
            # Sort the free positions of the occupancy map into continuous "islands".
            # Then, sort that list of lists by length.
            # The longest list is the biggest "island" i.e. the navigable area.
            non_navigable = list(sorted(__get_islands(), key=len))[:-1]
            # Record non-navigable positions.
            for n in non_navigable:
                for p in n:
                    self.occupancy_map[p[0]][p[1]] = -1

    def generate(self, cell_size: float = 0.5) -> None:
        """
        Generate an occupancy map.
        This function should only be called at least one controller.communicate() call after adding this add-on.
        The OccupancyMap then requires one more controller.communicate() call to create the occupancy map:

        ```python
        from tdw.controller import Controller
        from tdw.add_ons.occupancy_map import OccupancyMap

        c = Controller(launch_build=False)
        o = OccupancyMap()
        c.add_ons.append(o)
        c.communicate([])

        o.generate(cell_size=0.49, y=10)
        c.communicate([])
        print(o.occupancy_map)
        ```

        :param cell_size: The diameter of each cell of the occupancy map in meters.
        """

        if not self.initialized:
            print("Can't generate an occupancy map because this add-on hasn't initialized.\n"
                  "Wait at least one controller.communicate() call before calling occupancy_map.generate()")
            return
        self.occupancy_map = None
        self._cell_size = cell_size
        # Spherecast to each point.
        x = self.scene_bounds.x_min
        idx = 0
        idz = 0
        while x < self.scene_bounds.x_max:
            z = self.scene_bounds.z_min
            idz = 0
            while z < self.scene_bounds.z_max:
                # Create an overlap sphere to determine if the cell is occupied.
                # Cast a ray to determine if the cell has a floor.
                cast_id = idx + (idz * 10000)
                self.commands.extend([{"$type": "send_overlap_sphere",
                                       "radius": self._cell_size / 2,
                                       "position": {"x": x, "y": 0, "z": z},
                                       "id": cast_id},
                                      {"$type": "send_raycast",
                                       "origin": {"x": x, "y": OccupancyMap._RAYCAST_Y, "z": z},
                                       "destination": {"x": x, "y": -1, "z": z},
                                       "id": cast_id}])
                z += self._cell_size
                idz += 1
            x += self._cell_size
            idx += 1
        self._occupancy_map_size = (idx, idz)

    def get_occupancy_position(self, i: int, j: int) -> Tuple[float, float]:
        """
        Convert occupancy map indices to worldspace coordinates.
        This function can only be sent after first calling `self.generate()` and waiting at least one `controller.communicate()` call.:

        ```python
        from tdw.controller import Controller
        from tdw.add_ons.occupancy_map import OccupancyMap

        c = Controller(launch_build=False)
        o = OccupancyMap()
        c.add_ons.append(o)
        c.communicate([])

        o.generate(cell_size=0.49, y=10)
        c.communicate([])
        print(o.occupancy_map)
        ```

        :param i: The column index of self.occupancy_map
        :param j: The row index of self.occupancy_map.

        :return: `self.occupancy_map[i][j]` converted into x, z worldspace coordinates.
        """

        return self.scene_bounds.x_min + (i * self._cell_size), self.scene_bounds.z_min + (j * self._cell_size)

    def show(self) -> None:
        if self.occupancy_map is None:
            raise Exception("The occupancy map hasn't been generated and initialized (see documentation).")
        for idx, idy in np.ndindex(self.occupancy_map.shape):
            if self.occupancy_map[idx][idy] != 0:
                continue
            x, z = self.get_occupancy_position(idx, idy)
            self.commands.append({"$type": "add_position_marker",
                                  "position": {"x": x, "y": 0.05, "z": z},
                                  "scale": self._cell_size * 0.9,
                                  "color": {"r": 0, "g": 0, "b": 1, "a": 1},
                                  "shape": "square"})

    def hide(self) -> None:
        self.commands.append({"$type": "remove_position_markers"})
