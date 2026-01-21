from PIL import Image
import random

width = 384
height = 384

TAILLE_BLOCS_X = 10
TAILLE_BLOCS_Y = 10
JOINT_SIZE = 2
# Theme Nature/Foret - Vert mousse
VERT_BASE = 45  # Vert fonce pour le sol

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
            vert = VERT_BASE + variation
            vert = max(0, min(255, vert))
            Couleurs_Bloques[tile_id] = vert

        vert = Couleurs_Bloques[tile_id]

        lx = (x + offset) % TAILLE_BLOCS_X
        ly = y % TAILLE_BLOCS_Y

        if lx < JOINT_SIZE or ly < JOINT_SIZE:
            pixels[x, y] = (25, 35, 20)  # Joints vert fonce
        else:
            pixels[x, y] = (30, vert + 20, 25)  # Sol vert mousse


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


# Porte en haut (centrée)
DOOR_W_V = 20
DOOR_H_V = 60
DOOR_W_H = 60
DOOR_H_H = 20

draw_door(pixels, 0, (height - DOOR_H_V)//2, DOOR_W_V, DOOR_H_V)
draw_door(pixels, (width - DOOR_W_H)//2, height - DOOR_H_H, DOOR_W_H, DOOR_H_H)

# ---------------------------
# DECOS SIMPLES
# ---------------------------

def draw_outline_rect(pixels, x1, y1, w, h, color):
    for x in range(x1, x1 + w):
        if 0 <= x < width:
            if 0 <= y1 < height: pixels[x, y1] = color
            if 0 <= y1 + h - 1 < height: pixels[x, y1 + h - 1] = color
    for y in range(y1, y1 + h):
        if 0 <= y < height:
            if 0 <= x1 < width: pixels[x1, y] = color
            if 0 <= x1 + w - 1 < width: pixels[x1 + w - 1, y] = color

# Couleurs theme Nature
WOOD_DARK = (45, 30, 15)      # Bois fonce
WOOD_MID  = (85, 55, 25)      # Bois moyen
WOOD_LIGHT = (120, 80, 40)    # Bois clair
LEAF_DARK = (20, 60, 20)      # Feuille fonce
LEAF_MID  = (40, 100, 40)     # Feuille moyenne
YELLOW_GLOW = (180, 200, 80)  # Luciole/Champignon

# Arbres/Troncs (remplacent les piliers)
pillar_w, pillar_h = 18, 70
pillar_y = 110
draw_rect(pixels, 60, pillar_y, 60 + pillar_w, pillar_y + pillar_h, WOOD_MID)
draw_outline_rect(pixels, 60, pillar_y, pillar_w, pillar_h, WOOD_DARK)
draw_rect(pixels, 62, pillar_y + 4, 64, pillar_y + pillar_h - 4, WOOD_LIGHT)

draw_rect(pixels, 280, pillar_y, 280 + pillar_w, pillar_y + pillar_h, WOOD_MID)
draw_outline_rect(pixels, 280, pillar_y, pillar_w, pillar_h, WOOD_DARK)
draw_rect(pixels, 282, pillar_y + 4, 284, pillar_y + pillar_h - 4, WOOD_LIGHT)

# Zone d'herbe/mousse (remplace le tapis)
carpet_w, carpet_h = 120, 50
carpet_x = width // 2 - carpet_w // 2
carpet_y = height // 2 + 60
draw_rect(pixels, carpet_x, carpet_y, carpet_x + carpet_w, carpet_y + carpet_h, LEAF_MID)
draw_outline_rect(pixels, carpet_x, carpet_y, carpet_w, carpet_h, LEAF_DARK)

# Caillou (pierre grise pour contraste)
STONE_DARK = (35, 35, 35)
STONE_MID  = (90, 90, 90)
STONE_LIGHT = (115, 115, 115)
rock_x, rock_y = 90, 300
draw_rect(pixels, rock_x, rock_y, rock_x + 14, rock_y + 10, STONE_MID)
draw_outline_rect(pixels, rock_x, rock_y, 14, 10, STONE_DARK)
draw_rect(pixels, rock_x + 2, rock_y + 2, rock_x + 5, rock_y + 4, STONE_LIGHT)

# Champignons lumineux (remplacent les torches)
tx, ty = 40, 90
draw_rect(pixels, tx, ty, tx + 6, ty + 14, WOOD_DARK)
draw_rect(pixels, tx + 1, ty - 6, tx + 5, ty, YELLOW_GLOW)
draw_outline_rect(pixels, tx + 1, ty - 6, 4, 6, (140, 160, 60))

tx2, ty2 = 330, 120
draw_rect(pixels, tx2, ty2, tx2 + 6, ty2 + 14, WOOD_DARK)
draw_rect(pixels, tx2 + 1, ty2 - 6, tx2 + 5, ty2, YELLOW_GLOW)
draw_outline_rect(pixels, tx2 + 1, ty2 - 6, 4, 6, (140, 160, 60))

img.save("assets/room2.png")
print("Image créée !")
