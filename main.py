import pygame
import math
import random
from gestion_objets import Gestion_objets
from constantes import *
from UI.ui_menu import render_menu
from UI.ui_aide import render_aide
from UI.ui_gameover import render_gameover

pygame.init()
width = WIDTH
height = HEIGHT
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()

player_img = pygame.image.load("assets/player.png")
player_img = pygame.transform.scale(player_img, (player_img.get_width() * SCALE, player_img.get_height() * SCALE))
# chargement des images room 1 et room 2
# on voit si bonne taille de l'écran (width, height)
room1_img = pygame.image.load("assets/room1.png")
room1_img = pygame.transform.scale(room1_img, (width, height))

room2_img = pygame.image.load("assets/room2.png")
room2_img = pygame.transform.scale(room2_img, (width, height))

room3_img = pygame.image.load("assets/room3.png")
room3_img = pygame.transform.scale(room3_img, (width, height))

room4_img = pygame.image.load("assets/room4.png")
room4_img = pygame.transform.scale(room4_img, (width, height))

player_x = 100
player_y = 100
player_width = player_img.get_width()
player_height = player_img.get_height()

#Dico pour gerer les maps et portes
# chaque room : son image, et une liste de portes
# chaque porte : rectangle de collision (rect), nom de la prochaine room (next), point d apparition (spawn)
rooms = {
    "room1": {
        "image": room1_img,
        "doors": [
            # Porte Est -> vers Room 2
            {"rect": pygame.Rect(width - 20 * SCALE, (height - 60 * SCALE) // 2, 20 * SCALE, 60 * SCALE), 
             "next": "room2", 
             "spawn": (50, height // 2 - player_height // 2)},
            
            # Porte Sud -> vers Room 3
            {"rect": pygame.Rect((width - 60 * SCALE) // 2, height - 20 * SCALE, 60 * SCALE, 20 * SCALE), 
             "next": "room3", 
             "spawn": (width // 2 - player_width // 2, 50)}
        ]
    },
 
    "room2": {
        "image": room2_img,
        "doors": [
            # Porte Ouest -> vers Room 1
            {"rect": pygame.Rect(0, (height - 60 * SCALE) // 2, 20 * SCALE, 60 * SCALE), 
             "next": "room1", 
             "spawn": (width - 100, height // 2 - player_height // 2)},
            
            # Porte Sud -> vers Room 4
            {"rect": pygame.Rect((width - 60 * SCALE) // 2, height - 20 * SCALE, 60 * SCALE, 20 * SCALE), 
             "next": "room4", 
             "spawn": (width // 2 - player_width // 2, 50)}
        ]
    },

    "room3": {
        "image": room3_img,
        "doors": [
            # Porte Nord -> vers Room 1
            {"rect": pygame.Rect((width - 60 * SCALE) // 2, 0, 60 * SCALE, 20 * SCALE), 
             "next": "room1", 
             "spawn": (width // 2 - player_width // 2, height - 100)},
            
            # Porte Est -> vers Room 4
            {"rect": pygame.Rect(width - 20 * SCALE, (height - 60 * SCALE) // 2, 20 * SCALE, 60 * SCALE), 
             "next": "room4", 
             "spawn": (50, height // 2 - player_height // 2)}
        ]
    },

    "room4": {
        "image": room4_img,
        "doors": [
            # Porte Nord -> vers Room 2
            {"rect": pygame.Rect((width - 60 * SCALE) // 2, 0, 60 * SCALE, 20 * SCALE), 
             "next": "room2", 
             "spawn": (width // 2 - player_width // 2, height - 100)},
            
            # Porte Ouest -> vers Room 3
            {"rect": pygame.Rect(0, (height - 60 * SCALE) // 2, 20 * SCALE, 60 * SCALE), 
             "next": "room3", 
             "spawn": (width - 100, height // 2 - player_height // 2)}
        ]
    },
}

salle_actuellle = "room1"


vitesse = 4

def limite(v, minimum, maximum):
    return max(minimum, min(v, maximum))

# ========== SYSTEME DE DEGRADATION ==========
degradation = 0  # 0 = pas de degradation, 1 t'es mort
degradation_speed = 0.0008  # Vitesse d'augmentation par frame 
max_radius = 500  # rayon max de la zone visible (en pixels)

# ========== SYSTEME D'OBJETS ==========
gestionnaire_objets = Gestion_objets(SCALE)
gestionnaire_objets.spawn_aleatoire("room1")
gestionnaire_objets.spawn_aleatoire("room2")
gestionnaire_objets.spawn_aleatoire("room3")
gestionnaire_objets.spawn_aleatoire("room4")

# ========== SYSTEME DE SCORE ==========
score = 0
items_collected = 0

# ========== ETAT DU JEU ==========
game_state = {
    'degradation': 0,
    'vitesse': 4,
    'score': 0,
    'stars_collected': 0,
    'degradation_speed': 0.0008
}

def surface_degradation(center_x, center_y, radius, screen_w, screen_h, block_size=32):
    """
    Cree une surface avec un effet de vignette PIXELISE.
    Les pixels sont assombris par blocs en fonction de la distance au centre.
    """
    # surface noire avec alpha
    vignette = pygame.Surface((screen_w, screen_h), pygame.SRCALPHA)
    
    # parcourir par blocs pour effet pixel
    for by in range(0, screen_h, block_size):
        for bx in range(0, screen_w, block_size):
            # Centre du bloc
            block_center_x = bx + block_size // 2
            block_center_y = by + block_size // 2
            
            # Distance du bloc au centre de la vignette
            distance = math.sqrt((block_center_x - center_x)**2 + (block_center_y - center_y)**2)
            
            # Calculer l'alpha (opacite) en fonction de la distance
            if radius <= 0:
                alpha = 255  # tout noir si radius = 0
            elif distance < radius * 0.5:
                alpha = 0  # zone centrale transparente
            elif distance < radius:
                # zone de transition (fondu)
                factor = (distance - radius * 0.5) / (radius * 0.5)
                alpha = int(255 * factor)
            else:
                alpha = 255  # zone extene noire
            
            # dessiner le bloc avec l'alpha calcule
            pygame.draw.rect(vignette, (0, 0, 0, alpha), (bx, by, block_size, block_size))
    
    return vignette

# ========== ETATS DU JEU ==========
# Importés depuis constantes.py

game_state_mode = MENU  # Commence au menu
game_over = False

def reset_game():
    """Réinitialise toutes les variables du jeu pour recommencer"""
    global player_x, player_y, salle_actuellle, game_over, items_collected, gestionnaire_objets, game_state
    
    # Position du joueur
    player_x = 100
    player_y = 100
    salle_actuellle = "room1"
    
    # État du jeu
    game_over = False
    items_collected = 0
    
    # Réinitialiser le game_state
    game_state = {
        'degradation': 0,
        'vitesse': 4,
        'score': 0,
        'stars_collected': 0,
        'degradation_speed': 0.0008
    }
    
    # Réinitialiser les objets
    gestionnaire_objets = Gestion_objets(SCALE)
    gestionnaire_objets.spawn_aleatoire("room1")
    gestionnaire_objets.spawn_aleatoire("room2")
    gestionnaire_objets.spawn_aleatoire("room3")
    gestionnaire_objets.spawn_aleatoire("room4")


while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        
        # Gestion des clics de souris
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            
            # Dans le menu - Gestion des clics sur les options
            if game_state_mode == MENU:
                # Zone cliquable pour JOUER
                jouer_rect = pygame.Rect(80, height // 2 - 60, 200, 50)
                if jouer_rect.collidepoint(mouse_x, mouse_y):
                    game_state_mode = PLAYING
                    reset_game()
                
                # Zone cliquable pour AIDE
                aide_rect = pygame.Rect(80, height // 2 + 20, 200, 50)
                if aide_rect.collidepoint(mouse_x, mouse_y):
                    game_state_mode = HELP
            
            # Dans l'aide
            elif game_state_mode == HELP:
                # Zone cliquable pour retour (en bas à droite)
                retour_rect = pygame.Rect(width - 150, height - 60, 110, 40)
                if retour_rect.collidepoint(mouse_x, mouse_y):
                    game_state_mode = MENU
            
            # Dans le game over
            elif game_state_mode == GAME_OVER:
                # Zone cliquable REJOUER
                rejouer_rect = pygame.Rect(60, 480, 250, 50)
                if rejouer_rect.collidepoint(mouse_x, mouse_y):
                    game_state_mode = PLAYING
                    reset_game()
                
                # Zone cliquable MENU
                menu_rect = pygame.Rect(400, 480, 150, 50)
                if menu_rect.collidepoint(mouse_x, mouse_y):
                    game_state_mode = MENU
                    reset_game()
        
        # Touche R pour restart rapide, ENTREE pour jouer
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN and game_state_mode == MENU:
                game_state_mode = PLAYING
                reset_game()
            if event.key == pygame.K_r and game_state_mode == GAME_OVER:
                game_state_mode = PLAYING
                reset_game()
            elif event.key == pygame.K_ESCAPE:
                if game_state_mode == PLAYING:
                    game_state_mode = MENU
                    reset_game()

    # ========== AFFICHAGE DU MENU ==========
    if game_state_mode == MENU:
        render_menu(screen, width, height, pygame.mouse.get_pos())
        pygame.display.update()
        clock.tick(60)
        continue

    # ========== AFFICHAGE AIDE ==========
    if game_state_mode == HELP:
        render_aide(screen, width, height, pygame.mouse.get_pos())
        pygame.display.update()
        clock.tick(60)
        continue
    if game_state_mode == PLAYING:

        keys = pygame.key.get_pressed()
        
        current_speed = game_state['vitesse']

        if keys[pygame.K_LEFT]:
            player_x -= current_speed
        if keys[pygame.K_RIGHT]:
            player_x += current_speed
        if keys[pygame.K_UP]:
            player_y -= current_speed
        if keys[pygame.K_DOWN]:
            player_y += current_speed

        player_rect = pygame.Rect(player_x, player_y, player_width, player_height)
        
        # Récupérer les données de la room actuelle
        current_room_data = rooms[salle_actuellle]
        
        # vérifier les collisions avec les portes
        for door in current_room_data["doors"]:
            if player_rect.colliderect(door["rect"]):
                salle_actuellle = door["next"]  # changer de nom de room
                player_x, player_y = door["spawn"] #  y envoyer le joueur
        
        # ========== COLLISION AVEC LES OBJETS ==========
        collected_item = gestionnaire_objets.verifier_collision(player_rect, salle_actuellle, game_state)
        if collected_item:
            
            # Nettoyer les objets collectés
            gestionnaire_objets.supprimer_collectes()
            
            # Faire apparaître un nouvel objet aléatoire
            spawn_room = random.choice(["room2", "room3", "room4"])
            gestionnaire_objets.spawn_aleatoire(spawn_room)
            
            # S'assurer qu'il y a toujours au moins 3 objets visibles
            visible_items = len([item for item in gestionnaire_objets.items if item.visible])
            if visible_items < 3:
                for _ in range(3 - visible_items):
                    spawn_room = random.choice(["room2", "room3", "room4"])
                    gestionnaire_objets.spawn_aleatoire(spawn_room)
        
        # limiter le joueur a l'ecran
        player_x = limite(player_x, 0, width - player_width)
        player_y = limite(player_y, 0, height - player_height) 
        
        # mise a jour de la degradation
        if not game_over:
            current_degradation_speed = game_state.get('degradation_speed', 0.0008)
            game_state['degradation'] += current_degradation_speed
            if game_state['degradation'] >= 1.0:
                game_state['degradation'] = 1.0
                game_over = True
                game_state_mode = GAME_OVER  # Passer en mode game over
        
        # Calculer le rayon de vision (diminue avec la degradation)
        current_radius = max_radius * (1 - game_state['degradation'])
        
        # Mettre à jour les animations des objets
        gestionnaire_objets.update()
        
        clock.tick(60)

        # afficher l'image de la room actuelle
        screen.blit(current_room_data["image"], (0, 0))
        
        # ========== DESSINER LES OBJETS ==========
        gestionnaire_objets.draw(screen, salle_actuellle)
        
        screen.blit(player_img, (player_x, player_y)) # dessine le joueur


        
        # dessiner la vignette de degradation 
        # centre de la vignette = centre du joueur
        player_center_x = player_x + player_width // 2
        player_center_y = player_y + player_height // 2
        
        vignette_surface = surface_degradation(player_center_x, player_center_y, current_radius, width, height)
        screen.blit(vignette_surface, (0, 0))
        
        # ========== AFFICHER LE HUD (SCORE, STATS) ==========
        font_large = pygame.font.Font(None, 48)
        font_small = pygame.font.Font(None, 32)
        
        # Score principal
        score_text = font_large.render(f"Score: {game_state['score']}", True, (255, 255, 255))
        score_shadow = font_large.render(f"Score: {game_state['score']}", True, (0, 0, 0))
        screen.blit(score_shadow, (22, 22))
        screen.blit(score_text, (20, 20))
        

        
        # Salle courante (Haut Droite)
        room_text = font_small.render(f"Salle: {salle_actuellle.upper()}", True, (200, 255, 200)) # Vert clair
        room_rect = room_text.get_rect(topright=(width - 20, 20))
        screen.blit(room_text, room_rect)
        
        # Barre de dégradation
        bar_width = 200
        bar_height = 20
        bar_x = width - bar_width - 20
        bar_y = height - 40
        
        # Fond de la barre
        pygame.draw.rect(screen, (50, 50, 50), (bar_x, bar_y, bar_width, bar_height))
        # Barre de progression
        degradation_width = int(bar_width * game_state['degradation'])
        color_r = int(255 * game_state['degradation'])
        color_g = int(255 * (1 - game_state['degradation']))
        pygame.draw.rect(screen, (color_r, color_g, 0), (bar_x, bar_y, degradation_width, bar_height))
        # Contour
        pygame.draw.rect(screen, (255, 255, 255), (bar_x, bar_y, bar_width, bar_height), 2)
        
        pygame.display.update()

    # ========== ÉCRAN GAME OVER ==========
    if game_state_mode == GAME_OVER:
        render_gameover(screen, width, height, game_state, pygame.mouse.get_pos())
        pygame.display.update()
        clock.tick(60)
        continue
    
    pygame.display.update()
