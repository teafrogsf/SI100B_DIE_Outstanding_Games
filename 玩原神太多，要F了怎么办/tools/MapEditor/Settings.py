import pygame

# 定义常量
SCREEN_WIDTH, SCREEN_HEIGHT = 1280, 720
GRID_SIZE = 30
ROWS, COLS = SCREEN_HEIGHT // GRID_SIZE, SCREEN_WIDTH // GRID_SIZE
FPS = 60

# 定义颜色
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)


class FileCommand:
    def load_map(self, filepath):
        map_data = []
        with open(filepath, 'r') as file:
            for line in file:
                row = list(map(int, line.strip().split()))
                if row == []:
                    continue
                map_data.append(row)
        return map_data

    def save_map(self, filepath, map_data):
        with open(filepath, 'w') as file:
            for row in map_data:
                file.write(' '.join(map(str, row)) + '\n')


class Layer(FileCommand):
    def __init__(self, name, filepath):
        self.name = name
        self.filepath = filepath
        self.file_command = FileCommand()
        self.map_data = self.file_command.load_map(filepath)
        self.rows = len(self.map_data)
        self.cols = len(self.map_data[0])

    def save(self):
        self.file_command.save_map(self.filepath, self.map_data)


class Texture:
    '''
    idx表示的是在地图中的标识
    size表示的是实际像素大小(先水平后垂直)
    col、row表示的是横竖占用几格
    layer越大越后渲染
    '''

    def __init__(self, idx, path, size=(30, 30), col=1, row=1, layer=1):
        self.idx = idx
        self.path = path
        self.size = size
        self.col = col
        self.row = row
        self.layer = layer
        self.image = pygame.image.load(path)
        self.image = pygame.transform.scale(self.image, size)
        self.rect = self.image.get_rect()


layers = {}

layers[1] = Layer("ground", "ground_map.txt")
layers[2] = Layer("item", "item_map.txt")

textures = {}

textures["grass_ground"] = Texture(
    1, "./source/grass_ground.png", (30, 30), 1, 1, 1)
textures["sand_ground"] = Texture(
    2, "./source/sand_ground.png", (30, 30), 1, 1, 1)

textures["bush"] = Texture(1, "./source/bush.png", (30, 30), 1, 1, 2)
textures["grass"] = Texture(2, "./source/grass.png", (30, 30), 1, 1, 2)
textures["flower"] = Texture(3, "./source/flower.png", (30, 30), 1, 1, 2)
textures["tree"] = Texture(4, "./source/tree.png", (60, 60), 2, 2, 2)
