import pygame
import math

def render_aide(screen, width, height, mouse_pos):
    """
    Rend l'écran d'aide.
    
    Args:
        screen: Surface pygame pour le rendu
        width: Largeur de l'écran
        height: Hauteur de l'écran
        mouse_pos: Position de la souris (x, y)
    
    Returns:
        pygame.Rect: Zone cliquable du bouton retour
    """
    # Fond uni sombre (même que le menu)
    screen.fill((25, 25, 35))
    
    font_title = pygame.font.Font(None, 70)
    font_section = pygame.font.Font(None, 45)
    font_text = pygame.font.Font(None, 32)
    font_small = pygame.font.Font(None, 28)
    
    # Titre
    title = font_title.render("AIDE", True, (200, 200, 200))
    screen.blit(title, (60, 50))
    
    # === SECTION OBJECTIF ===
    y_pos = 140
    objectif_title = font_section.render("OBJECTIF", True, (180, 180, 180))
    screen.blit(objectif_title, (60, y_pos))
    
    objectif_text = font_text.render("Survivez le plus longtemps possible a la degradation", True, (150, 150, 150))
    screen.blit(objectif_text, (60, y_pos + 50))
    
    # === SECTION OBJETS ===
    y_pos = 260
    objets_title = font_section.render("OBJETS", True, (180, 180, 180))
    screen.blit(objets_title, (60, y_pos))
    
    # Boule rouge - icône simple
    pygame.draw.circle(screen, (255, 80, 80), (90, y_pos + 65), 16)
    boule_text = font_text.render("Les Boule Rouge on pour role de reduire la degradation", True, (150, 150, 150))
    screen.blit(boule_text, (130, y_pos + 50))
    
    # Étoile - icône simple
    cx, cy = 90, y_pos + 125
    points = []
    for i in range(10):
        angle = (i * 36 - 90) * math.pi / 180
        r = 16 if i % 2 == 0 else 7
        points.append((cx + r * math.cos(angle), cy + r * math.sin(angle)))
    pygame.draw.polygon(screen, (255, 215, 100), points)
    
    etoile_text = font_text.render("Les etoiles donnent des points : +100 par etoile", True, (150, 150, 150))
    screen.blit(etoile_text, (130, y_pos + 110))
    
    # === SECTION CONTRÔLES ===
    y_pos = 450
    controles_title = font_section.render("CONTRÔLES", True, (180, 180, 180))
    screen.blit(controles_title, (60, y_pos))
    
    controles = [
        "Flèches - Pour se deplacer",
        "Entrée - Pour commencer",
        "Échap - Pour quitter"
    ]
    
    for i, ctrl in enumerate(controles):
        ctrl_text = font_text.render(ctrl, True, (150, 150, 150))
        screen.blit(ctrl_text, (60, y_pos + 50 + i * 35))
    
    # Bouton retour en bas à droite
    retour_text = font_small.render("< RETOUR", True, (150, 150, 150))
    retour_rect = retour_text.get_rect(bottomright=(width - 40, height - 40))
    
    # Effet hover
    if retour_rect.collidepoint(mouse_pos):
        retour_text = font_small.render("< RETOUR", True, (220, 220, 220))
    
    screen.blit(retour_text, retour_rect)
    
    return retour_rect
