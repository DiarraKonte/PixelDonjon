from PIL import Image
import random

width = 384
height = 384

TAILLE_BLOCS_X = 10
TAILLE_BLOCS_Y = 10
JOINT_SIZE = 2
GRIS_BASE = 70

img = Image.new('RGB', (width, height), (0, 0, 0))
pixels = img.load()

Couleurs_Bloques = {}

for y in range(height):
    for x in range(width):

        row = y // TAILLE_BLOCS_Y
        offset = (TAILLE_BLOCS_X // 2) if (row % 2 == 1) else 0

        tile_x = (x + offset) // TAILLE_BLOCS_X
        tile_y = y // TAILLE_BLOCS_Y
        tile_id = (tile_x, tile_y)

        if tile_id not in Couleurs_Bloques:
            variation = random.randint(-10, 10)
            gris = GRIS_BASE + variation
            gris = max(0, min(255, gris))
            Couleurs_Bloques[tile_id] = gris

        gris = Couleurs_Bloques[tile_id]

        lx = (x + offset) % TAILLE_BLOCS_X
        ly = y % TAILLE_BLOCS_Y

        if lx < JOINT_SIZE or ly < JOINT_SIZE:
            pixels[x, y] = (40, 40, 40)
        else:
            pixels[x, y] = (gris, gris, gris)


def draw_rect(pixels, x1, y1, x2, y2, color):
    for y in range(y1, y2):
        for x in range(x1, x2):
            if 0 <= x < width and 0 <= y < height:
                pixels[x, y] = color

def draw_door(pixels, start_x, start_y, w, h):
    NOIR = (0, 0, 0)
    for py in range(start_y, start_y + h):
        for px in range(start_x, start_x + w):
            if 0 <= px < width and 0 <= py < height:
                pixels[px, py] = NOIR


# Porte en bas (centrée)
DOOR_W_V = 20
DOOR_H_V = 60
DOOR_W_H = 60
DOOR_H_H = 20
draw_door(pixels, (width - DOOR_W_H)//2, 0, DOOR_W_H, DOOR_H_H)
draw_door(pixels, 0, (height - DOOR_H_V)//2, DOOR_W_V, DOOR_H_V)


# deco trees simple

def draw_outline_rect(pixels, x1, y1, w, h, color):
    for x in range(x1, x1 + w):
        if 0 <= x < width:
            if 0 <= y1 < height: pixels[x, y1] = color
            if 0 <= y1 + h - 1 < height: pixels[x, y1 + h - 1] = color
    for y in range(y1, y1 + h):
        if 0 <= y < height:
            if 0 <= x1 < width: pixels[x1, y] = color
            if 0 <= x1 + w - 1 < width: pixels[x1 + w - 1, y] = color

STONE_DARK = (35, 35, 35)
STONE_MID  = (90, 90, 90)
STONE_LIGHT = (115, 115, 115)
RED_DARK = (110, 20, 20)
RED_MID  = (140, 30, 30)
ORANGE   = (220, 140, 40)

# piliers 
pillar_w, pillar_h = 18, 70
pillar_y = 60

draw_rect(pixels, 60, pillar_y, 60 + pillar_w, pillar_y + pillar_h, STONE_MID)
draw_outline_rect(pixels, 60, pillar_y, pillar_w, pillar_h, STONE_DARK)
draw_rect(pixels, 62, pillar_y + 4, 64, pillar_y + pillar_h - 4, STONE_LIGHT)

draw_rect(pixels, 280, pillar_y, 280 + pillar_w, pillar_y + pillar_h, STONE_MID)
draw_outline_rect(pixels, 280, pillar_y, pillar_w, pillar_h, STONE_DARK)
draw_rect(pixels, 282, pillar_y + 4, 284, pillar_y + pillar_h - 4, STONE_LIGHT)

# tapis 
carpet_w, carpet_h = 120, 50
carpet_x = width // 2 - carpet_w // 2
carpet_y = height // 2 + 20
draw_rect(pixels, carpet_x, carpet_y, carpet_x + carpet_w, carpet_y + carpet_h, RED_MID)
draw_outline_rect(pixels, carpet_x, carpet_y, carpet_w, carpet_h, RED_DARK)

# caillou
rock_x, rock_y = 90, 290
draw_rect(pixels, rock_x, rock_y, rock_x + 14, rock_y + 10, STONE_MID)
draw_outline_rect(pixels, rock_x, rock_y, 14, 10, STONE_DARK)
draw_rect(pixels, rock_x + 2, rock_y + 2, rock_x + 5, rock_y + 4, STONE_LIGHT)

# torches
tx, ty = 40, 60
draw_rect(pixels, tx, ty, tx + 6, ty + 14, STONE_DARK)
draw_rect(pixels, tx + 1, ty - 6, tx + 5, ty, ORANGE)
draw_outline_rect(pixels, tx + 1, ty - 6, 4, 6, (180, 100, 30))

tx2, ty2 = 330, 220
draw_rect(pixels, tx2, ty2, tx2 + 6, ty2 + 14, STONE_DARK)
draw_rect(pixels, tx2 + 1, ty2 - 6, tx2 + 5, ty2, ORANGE)
draw_outline_rect(pixels, tx2 + 1, ty2 - 6, 4, 6, (180, 100, 30))

img.save("assets/room4.png")
print("Image créée !")
