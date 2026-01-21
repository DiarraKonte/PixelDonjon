import pygame
import os
import math

def create_star_image():
    pygame.init()
    
    # Taille de l'image
    size = 24
    surface = pygame.Surface((size, size), pygame.SRCALPHA)
    
    # Couleurs
    YELLOW = (255, 215, 0)
    ORANGE = (255, 140, 0)
    WHITE = (255, 255, 255)
    
    # Dessiner une étoile à 5 branches
    center = size // 2
    outer_radius = 10
    inner_radius = 4
    points = []
    
    for i in range(10):
        angle = (i * 36 - 90) * math.pi / 180
        curr_radius = outer_radius if i % 2 == 0 else inner_radius
        x = center + curr_radius * math.cos(angle)
        y = center + curr_radius * math.sin(angle)
        points.append((x, y))
        
    # Dessiner l'étoile
    pygame.draw.polygon(surface, YELLOW, points)
    pygame.draw.polygon(surface, ORANGE, points, 2)
    
    # Sauvegarder l'image
    if not os.path.exists("assets"):
        os.makedirs("assets")
        
    try:
        pygame.image.save(surface, "assets/etoile.png")
        print("Étoile créée")


if __name__ == "__main__":
    create_star_image()
