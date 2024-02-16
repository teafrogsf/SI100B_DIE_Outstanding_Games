from Settings import *
import pygame
import sys


class Brush:
    def __init__(self, texture, key):
        self.texture = textures[texture]
        self.key = key


def in_map(x1, y1, x2, y2):
    screen_rect = [camera_left, camera_top, camera_left +
                   SCREEN_WIDTH, camera_top+SCREEN_HEIGHT]
    grid_rect = [x1*GRID_SIZE, y1*GRID_SIZE,
                 (x2+1)*GRID_SIZE, (y2+1)*GRID_SIZE]
    if screen_rect[2] < grid_rect[0] or grid_rect[2] < screen_rect[0]:
        return False
    if screen_rect[3] < grid_rect[1] or grid_rect[3] < screen_rect[1]:
        return False
    return True


pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Map Editor')
clock = pygame.time.Clock()

selected_cell = [0, 0]  # 初始选中的单元格，先行后列
camera_left = 0
camera_top = 0

brushs = {}
caches = {}

brushs["grass_ground"] = Brush("grass_ground", pygame.K_1)
brushs["sand_ground"] = Brush("sand_ground", pygame.K_2)
brushs["bush"] = Brush("bush", pygame.K_3)
brushs["grass"] = Brush("grass", pygame.K_4)
brushs["flower"] = Brush("flower", pygame.K_5)
brushs["tree"] = Brush("tree", pygame.K_6)

for i in range(1, len(layers)+1):
    layer = layers[i]
    for row in range(layer.rows):
        for col in range(layer.cols):
            for cur in textures:
                texture = textures[cur]
                if texture.idx == layer.map_data[row][col] and texture.layer == i:
                    caches[(texture.idx, texture.layer)] = texture
                    break

for cur in brushs:
    brush = brushs[cur]
    caches[(brush.texture.idx, brush.texture.layer)] = brush.texture

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            for i in layers:
                layer = layers[i]
                layer.save()
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONUP:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            selected_cell = [(mouse_y+camera_top) // GRID_SIZE,
                             (mouse_x+camera_left) // GRID_SIZE]
            print("选中了：", selected_cell)
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                selected_cell[1] -= 1
            elif event.key == pygame.K_RIGHT:
                selected_cell[1] += 1
            elif event.key == pygame.K_UP:
                selected_cell[0] -= 1
            elif event.key == pygame.K_DOWN:
                selected_cell[0] += 1

            for cur in brushs:
                brush = brushs[cur]
                if brush.key == event.key:
                    layers[brush.texture.layer].map_data[selected_cell[0]
                                                         ][selected_cell[1]] = brush.texture.idx
                    break

            if event.key == pygame.K_BACKSPACE:
                for i in range(len(layers), 0, -1):
                    if layers[i].map_data[selected_cell[0]][selected_cell[1]] != 0:
                        layers[i].map_data[selected_cell[0]
                                           ][selected_cell[1]] = 0
                        break

    keys = pygame.key.get_pressed()
    if keys[pygame.K_a]:
        camera_left -= GRID_SIZE
    if keys[pygame.K_d]:
        camera_left += GRID_SIZE
    if keys[pygame.K_w]:
        camera_top -= GRID_SIZE
    if keys[pygame.K_s]:
        camera_top += GRID_SIZE

    screen.fill((49, 131, 214))
    for i in range(1, len(layers)+1):
        layer = layers[i]
        for row in range(layer.rows):
            for col in range(layer.cols):
                if layer.map_data[row][col] == 0:
                    continue
                texture = caches[(layer.map_data[row][col], i)]
                if in_map(col, row, col+texture.col-1, row+texture.row-1):
                    screen.blit(
                        texture.image, (col*GRID_SIZE-camera_left, row*GRID_SIZE-camera_top))

    # 绘制选中框
    pygame.draw.rect(
        screen, BLACK, (selected_cell[1] * GRID_SIZE-camera_left, selected_cell[0] * GRID_SIZE-camera_top, GRID_SIZE, GRID_SIZE), 3)

    # 显示具体坐标
    font = pygame.font.Font(None, 36)
    text_content = "current grid:( "+str(selected_cell[0]) + \
        " , "+str(selected_cell[1])+" )[row,column]"
    text_surface = font.render(text_content, True, (0, 0, 0))
    text_rect = text_surface.get_rect()
    text_rect.center = (SCREEN_WIDTH // 2, 20)
    screen.blit(text_surface, text_rect.topleft)

    pygame.display.flip()
    clock.tick(FPS)
