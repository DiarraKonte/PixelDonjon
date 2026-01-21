import pygame
import os

def create_simple_red_ball():
    pygame.init()
    
    # Taille de l'image (plus petite - 24px)
    size = 24
    center = size // 2
    surface = pygame.Surface((size, size), pygame.SRCALPHA)
    
    # Couleurs
    RED = (255, 0, 0)
    DARK_RED = (200, 0, 0)
    WHITE = (255, 255, 255)
    
    # Dessiner la boule rouge simple (plus petite)
    pygame.draw.circle(surface, RED, (center, center), 8)
    
    # Un petit contour pour la définition
    pygame.draw.circle(surface, DARK_RED, (center, center), 8, 2)
    
    # Un petit reflet simple
    pygame.draw.circle(surface, WHITE, (center - 3, center - 3), 2)

    # Sauvegarder l'image
    if not os.path.exists("assets"):
        os.makedirs("assets")
        
    try:
        pygame.image.save(surface, "assets/red_ball.png")
        print("Image 'assets/red_ball.png' créée avec succès !")
    except Exception as e:
        print(f"Erreur lors de la sauvegarde : {e}")

if __name__ == "__main__":
    create_simple_red_ball()
