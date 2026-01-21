import pygame

def render_menu(screen, width, height, mouse_pos):
    """
    Rend le menu principal.
    
    Args:
        screen: Surface pygame pour le rendu
        width: Largeur de l'écran
        height: Hauteur de l'écran
        mouse_pos: Position de la souris (x, y)
    
    Returns:
        dict: Zones cliquables {'jouer': Rect, 'aide': Rect}
    """
    # Fond uni sombre
    screen.fill((25, 25, 35))
    
    # Polices
    font_title = pygame.font.Font(None, 90)
    font_option = pygame.font.Font(None, 50)
    font_small = pygame.font.Font(None, 28)
    
    mouse_x, mouse_y = mouse_pos
    
    # === OPTIONS À GAUCHE ===
    # JOUER
    jouer_rect = pygame.Rect(80, height // 2 - 60, 200, 50)
    jouer_hover = jouer_rect.collidepoint(mouse_x, mouse_y)
    jouer_color = (220, 220, 220) if jouer_hover else (150, 150, 150)
    jouer_text = font_option.render("JOUER", True, jouer_color)
    screen.blit(jouer_text, (80, height // 2 - 60))
    
    # AIDE
    aide_rect = pygame.Rect(80, height // 2 + 20, 200, 50)
    aide_hover = aide_rect.collidepoint(mouse_x, mouse_y)
    aide_color = (220, 220, 220) if aide_hover else (150, 150, 150)
    aide_text = font_option.render("AIDE", True, aide_color)
    screen.blit(aide_text, (80, height // 2 + 20))
    
    # === TITRE AU CENTRE-DROIT ===
    title = font_title.render("PIXEL SURVIVOR", True, (200, 200, 200))
    title_rect = title.get_rect(center=(width - 280, height // 2))
    screen.blit(title, title_rect)
    
    # Petite ligne de séparation verticale
    pygame.draw.line(screen, (60, 60, 70), (width // 2 - 50, height // 2 - 100), (width // 2 - 50, height // 2 + 100), 2)
    
    # Instructions en bas
    info_text = font_small.render("Entrée: Jouer | Échap: Quitter", True, (80, 80, 90))
    info_rect = info_text.get_rect(center=(width // 2, height - 40))
    screen.blit(info_text, info_rect)
    
    return {'jouer': jouer_rect, 'aide': aide_rect}
