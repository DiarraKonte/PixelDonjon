import pygame

def render_gameover(screen, width, height, game_state, mouse_pos):
    """
    Rend l'écran game over.
    
    Args:
        screen: Surface pygame pour le rendu
        width: Largeur de l'écran
        height: Hauteur de l'écran
        game_state: Dictionnaire contenant l'état du jeu (score, stars_collected, etc.)
        mouse_pos: Position de la souris (x, y)
    
    Returns:
        dict: Zones cliquables {'rejouer': Rect, 'menu': Rect}
    """
    # Fond uni sombre (même que le menu)
    screen.fill((25, 25, 35))
    
    font_title = pygame.font.Font(None, 80)
    font_stats = pygame.font.Font(None, 45)
    font_option = pygame.font.Font(None, 40)
    
    # Titre GAME OVER
    title = font_title.render("GAME OVER", True, (200, 80, 80))
    screen.blit(title, (60, 80))
    
    # === STATISTIQUES ===
    y_pos = 200
    stats_title = font_stats.render("STATISTIQUES", True, (180, 180, 180))
    screen.blit(stats_title, (60, y_pos))
    
    # Score
    score_text = font_option.render(f"Score: {game_state['score']}", True, (150, 150, 150))
    screen.blit(score_text, (60, y_pos + 60))
    
    # Étoiles collectées
    stars_text = font_option.render(f"Étoiles: {game_state.get('stars_collected', 0)}", True, (150, 150, 150))
    screen.blit(stars_text, (60, y_pos + 110))
    
    # === OPTIONS ===
    mouse_x, mouse_y = mouse_pos
    y_pos = 480
    
    # REJOUER
    rejouer_rect = pygame.Rect(60, y_pos, 250, 50)
    rejouer_hover = rejouer_rect.collidepoint(mouse_x, mouse_y)
    rejouer_color = (220, 220, 220) if rejouer_hover else (150, 150, 150)
    rejouer_text = font_option.render("REJOUER (R)", True, rejouer_color)
    screen.blit(rejouer_text, (60, y_pos))
    
    # MENU
    menu_rect = pygame.Rect(400, y_pos, 150, 50)
    menu_hover = menu_rect.collidepoint(mouse_x, mouse_y)
    menu_color = (220, 220, 220) if menu_hover else (150, 150, 150)
    menu_text = font_option.render("MENU", True, menu_color)
    screen.blit(menu_text, (400, y_pos))
    
    return {'rejouer': rejouer_rect, 'menu': menu_rect}
