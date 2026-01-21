from PIL import Image

# dimensions du sprite du joueur (16x16 pixels)
WIDTH = 32
HEIGHT = 32

# creation de l'image avec transparence (RGBA)
img = Image.new('RGBA', (WIDTH, HEIGHT), (0, 0, 0, 0))
pixels = img.load()

# === PALETTE DE COULEURS ===
TRANSPARENT = (0, 0, 0, 0)

# couleurs de la peau
SKIN = (255, 206, 180, 255)
SKIN_DARK = (220, 170, 140, 255)

# couleurs des cheveux
HAIR = (60, 40, 30, 255)
HAIR_DARK = (40, 25, 15, 255)

# couleurs des yeux
EYE = (40, 40, 40, 255)
EYE_WHITE = (255, 255, 255, 255)

# couleurs du t-shirt (bleu)
SHIRT = (70, 100, 170, 255)
SHIRT_DARK = (50, 70, 130, 255)
SHIRT_LIGHT = (100, 130, 200, 255)

# couleurs du pantalon
PANTS = (50, 50, 60, 255)
PANTS_DARK = (30, 30, 40, 255)

# couleurs des chaussures
SHOES = (80, 50, 30, 255)
SHOES_DARK = (50, 30, 15, 255)


# === FONCTIONS UTILITAIRES ===
def draw_pixel(x, y, color):
    """Dessine un pixel avec vérification des limites."""
    if 0 <= x < WIDTH and 0 <= y < HEIGHT:
        pixels[x, y] = color


def draw_rect(x1, y1, x2, y2, color):
    """Dessine un rectangle rempli (x2, y2 exclus)."""
    for y in range(y1, y2):
        for x in range(x1, x2):
            draw_pixel(x, y, color)


def draw_line_h(x1, x2, y, color):
    """Dessine une ligne horizontale."""
    for x in range(x1, x2):
        draw_pixel(x, y, color)


def draw_line_v(x, y1, y2, color):
    """Dessine une ligne verticale."""
    for y in range(y1, y2):
        draw_pixel(x, y, color)


# === DESSIN DU PERSONNAGE ===

# --- CHEVEUX (haut de la tête) ---
# ligne du haut des cheveux
draw_line_h(6, 11, 1, HAIR_DARK)
# corps des cheveux
draw_rect(5, 2, 12, 4, HAIR)
draw_pixel(5, 2, HAIR_DARK)
draw_pixel(11, 2, HAIR_DARK)
# meche sur les côtés
draw_pixel(4, 3, HAIR)
draw_pixel(12, 3, HAIR)

# forme du visage
draw_rect(5, 4, 12, 8, SKIN)
# opmbre du visage
draw_line_v(5, 4, 8, SKIN_DARK)
draw_line_v(11, 4, 8, SKIN_DARK)
draw_line_h(5, 12, 7, SKIN_DARK)

# yeux
draw_pixel(6, 5, EYE_WHITE)
draw_pixel(7, 5, EYE)
draw_pixel(9, 5, EYE)
draw_pixel(10, 5, EYE_WHITE)

# cou
draw_rect(7, 8, 10, 9, SKIN)

# corps du t-shirt
draw_rect(5, 9, 12, 13, SHIRT)
#ombre du t-shirt
draw_line_v(5, 9, 13, SHIRT_DARK)
draw_line_v(11, 9, 13, SHIRT_DARK)
draw_line_h(5, 12, 12, SHIRT_DARK)
# Highlight
draw_pixel(7, 10, SHIRT_LIGHT)
draw_pixel(8, 10, SHIRT_LIGHT)

# mache et bras
draw_rect(3, 9, 5, 12, SHIRT)
draw_rect(12, 9, 14, 12, SHIRT)
draw_pixel(3, 9, SHIRT_DARK)
draw_pixel(13, 9, SHIRT_DARK)

# Mains
draw_pixel(3, 12, SKIN)
draw_pixel(4, 12, SKIN)
draw_pixel(12, 12, SKIN)
draw_pixel(13, 12, SKIN)

# --- PANTALON ---
draw_rect(5, 13, 12, 15, PANTS)
# ombre pantalon
draw_line_v(5, 13, 15, PANTS_DARK)
draw_line_v(11, 13, 15, PANTS_DARK)
# Separer les jambes
draw_line_v(8, 14, 15, PANTS_DARK)

# chaussure 
draw_rect(5, 15, 8, 16, SHOES)
draw_rect(9, 15, 12, 16, SHOES)
# ombre chaussure
draw_pixel(5, 15, SHOES_DARK)
draw_pixel(11, 15, SHOES_DARK)


img.save("assets/player.png")
print("✓ Sprite du joueur créé : assets/player.png")
print(f"  Dimensions : {WIDTH}x{HEIGHT} pixels")
