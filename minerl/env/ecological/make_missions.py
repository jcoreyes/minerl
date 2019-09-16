
import xml.etree.ElementTree as ET
import numpy as np


class MissionGen:

    type_to_idx = {
        'wool': 1,
        'bedrock':2,
    }

    idx_to_type = {v:k for k,v in type_to_idx.items()}

    def __init__(self, base_xml, size):
        self.base_xml = base_xml
        self.size = size
        self.ground_y = 227


    def print_grid(self, grid):
        for row in grid:
            print(' '.join('%d' % x for x in row ))


    def addBlock(self, drawing_d, type, x, y, z):
        text = 'DrawBlock type="%s" x="%d" y="%d" z="%d"' % (type, x, y, z)
        elem = ET.SubElement(drawing_d, text)

    def populate_grid_random_resource(self, grid, type, prob):
        # Populate grid randomly with resources
        idx = np.random.random(size=grid.shape) < prob
        grid[idx] = self.type_to_idx[type]

    def populate_grid_random_resource_radius(self, grid, type, prob, radius):
        # Populate grid with random resources within some radius of center
        center = self.size // 2

        # Construct grid with 1s where inside radius of center
        radius_grid = np.zeros(grid.shape)
        for i in range(radius):
            radius_grid[center-radius + i, center-radius:center+radius] = 1

        # Idxs where resource gen and inside radius
        idx = np.logical_and(np.random.random(size=grid.shape) < prob, radius_grid)

        # Set grid to resource type
        grid[idx] = self.type_to_idx[type]

    def gen_mission(self, training=True):
        ns = "{http://ProjectMalmo.microsoft.com}"
        ET.register_namespace("", 'http://ProjectMalmo.microsoft.com')
        tree = ET.parse(self.base_xml)
        root = tree.getroot()
        server_section = root.find(ns + 'ServerSection')
        server_handler = server_section.find(ns + 'ServerHandlers')
        drawing_d  = server_handler.find(ns + 'DrawingDecorator')

        grid = np.zeros((self.size, self.size))

        self.populate_grid_random_resource(grid, 'wool', 0.03)

        if training:
            self.populate_grid_random_resource_radius(grid, 'wool', 0.2, 5)

        # Add walls
        grid[0, :] = 2
        grid[-1, :] = 2
        grid[:, 0] = 2
        grid[:, -1] = 2

        # Clear center
        grid[self.size//2, self.size//2] = 0

        self.print_grid(grid)

        min_xz = - self.size // 2
        for i in range(self.size):
            for j in range(self.size):
                type_idx = grid[i, j]
                x = min_xz + i
                z = min_xz + j
                if type_idx in self.idx_to_type:
                    self.addBlock(drawing_d, self.idx_to_type[type_idx], x, self.ground_y, z)

        return tree


if __name__ == '__main__':
    base_xml = '/home/jcoreyes/continual/minerl/minerl/env/ecological/missions/wool_gather_base.xml'
    missiongen = MissionGen(base_xml, 40)


    mission = missiongen.gen_mission(training=True)
    mission.write('/home/jcoreyes/continual/minerl/minerl/env/ecological/missions/wool_gather_train.xml',
                  encoding="UTF-8", xml_declaration=True, default_namespace='')

    mission = missiongen.gen_mission(training=False)
    mission.write('/home/jcoreyes/continual/minerl/minerl/env/ecological/missions/wool_gather_test.xml',
                  encoding="UTF-8", xml_declaration=True, default_namespace='')