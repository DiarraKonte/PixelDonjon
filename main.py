import pygame

pygame.init()
screen = pygame.display.set_mode((384, 384))
SCALE = 2
width = 384 * SCALE
height = 384 * SCALE
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()

player_img = pygame.image.load("assets/player.png")
player_img = pygame.transform.scale(player_img, (player_img.get_width() * SCALE, player_img.get_height() * SCALE))
# Chargement des images de scènes (Room 1 et Room 2)
# On s'assure qu'elles sont à la bonne taille de l'écran (width, height)
room1_img = pygame.image.load("assets/room1.png")
room1_img = pygame.transform.scale(room1_img, (width, height))

room2_img = pygame.image.load("assets/room2.png")
room2_img = pygame.transform.scale(room2_img, (width, height))

room3_img = pygame.image.load("assets/room3.png")
room3_img = pygame.transform.scale(room3_img, (width, height))

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
            # porte droite -> va a room2, spawn a gauche
            {"rect": pygame.Rect(width - 20 * SCALE, (height - 60 * SCALE) // 2, 20 * SCALE, 60 * SCALE), 
             "next": "room2", 
             "spawn": (50, height // 2 - player_height // 2)},
            
            # porte bas -> va a room3, spawn en haut
            {"rect": pygame.Rect((width - 60 * SCALE) // 2, height - 20 * SCALE, 60 * SCALE, 20 * SCALE), 
             "next": "room3", 
             "spawn": (width // 2 - player_width // 2, 50)}
        ]
    },
 
    "room2": {
        "image": room2_img,
        "doors": [
            # porte gauche -> va a room1, spawn a droite
            {"rect": pygame.Rect(0, (height - 60 * SCALE) // 2, 20 * SCALE, 60 * SCALE), 
             "next": "room1", 
             "spawn": (width - 100, height // 2 - player_height // 2)},
            #porte bas -> va a room3, spawn a droite
            {"rect": pygame.Rect((width - 60 * SCALE) // 2, height - 20 * SCALE, 60 * SCALE, 20 * SCALE), 
             "next": "room3", 
             "spawn": (width - 100, height // 2 - player_height // 20)}
        ]
    },
       "room3": {
        "image": room3_img,
        "doors": [
            #porte haut -> va a room1, spawn en bas
            {"rect": pygame.Rect((width - 60 * SCALE) // 2, 0, 60 * SCALE, 20 * SCALE), 
             "next": "room1", 
             "spawn": (width // 2 - player_width // 2, height - 100)},
            #porte droite -> va a room2, spawn en bas
            {"rect": pygame.Rect(width - 20 * SCALE, (height - 60 * SCALE) // 2, 20 * SCALE, 60 * SCALE), 
             "next": "room2", 
             "spawn": (width // 2 - player_width // 2, height - 100)}
        ]
    },
    "room4": {
        "image": room4_img,
        "doors": [
            
        ]
    },
}

current_room_name = "room1"


vitesse = 4

def limite(v, minimum, maximum):
    return max(minimum, min(v, maximum))



while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT]:
        player_x -= vitesse
    if keys[pygame.K_RIGHT]:
        player_x += vitesse
    if keys[pygame.K_UP]:
        player_y -= vitesse
    if keys[pygame.K_DOWN]:
        player_y += vitesse

    player_rect = pygame.Rect(player_x, player_y, player_width, player_height)
    
    # Récupérer les données de la room actuelle
    current_room_data = rooms[current_room_name]
    
    # Vérifier les collisions avec les portes
    for door in current_room_data["doors"]:
        if player_rect.colliderect(door["rect"]):
            current_room_name = door["next"]  # Changer de nom de room
            player_x, player_y = door["spawn"] # Téléporter le joueur
    
    # Limiter le joueur à l'écran
    player_x = limite(player_x, 0, width - player_width)
    player_y = limite(player_y, 0, height - player_height) 
    
    clock.tick(60)

    # Afficher l'image de la room actuelle
    screen.blit(current_room_data["image"], (0, 0))
    screen.blit(player_img, (player_x, player_y)) # Dessine le joueur
    pygame.display.update()   
