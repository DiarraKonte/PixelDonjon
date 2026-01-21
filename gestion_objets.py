import pygame
import random

class Balle_rouge:
    """objet Boule Rouge simple qui rinitialise la degradation"""
    
    def __init__(self, x, y, scale=2):
        self.x = x
        self.y = y
        self.type = "red_ball"
        self.visible = True
        self.collected = False
        self.scale = scale
        self.room = None
        
        # Chargement de l'image
        try:
            self.image = pygame.image.load("assets/red_ball.png")
            new_size = (self.image.get_width() * scale, self.image.get_height() * scale)
            self.image = pygame.transform.scale(self.image, new_size)
        except:
            self.image = pygame.Surface((16*scale, 16*scale), pygame.SRCALPHA)
            pygame.draw.circle(self.image, (255, 0, 0), (8*scale, 8*scale), 8*scale)
            
        self.rect = self.image.get_rect(center=(x, y))
        
    def draw(self, surface):
        if self.visible:
            surface.blit(self.image, self.rect)
            
    def get_rect(self):
        return self.rect
        
    def collecter(self):
        self.visible = False
        self.collected = True


class Etoile:
    """l'objet etoile qui donne du score"""
    
    def __init__(self, x, y, scale=2):
        self.x = x
        self.y = y
        self.type = "star"
        self.visible = True
        self.collected = False
        self.scale = scale
        self.room = None
        
        try:
            self.image = pygame.image.load("assets/etoile.png")
            new_size = (self.image.get_width() * scale, self.image.get_height() * scale)
            self.image = pygame.transform.scale(self.image, new_size)
        except:
            self.image = pygame.Surface((16*scale, 16*scale), pygame.SRCALPHA)
            pygame.draw.polygon(self.image, (255, 215, 0), [(8*scale, 0), (10*scale, 6*scale), (16*scale, 6*scale), (11*scale, 10*scale), (13*scale, 16*scale), (8*scale, 12*scale), (3*scale, 16*scale), (5*scale, 10*scale), (0, 6*scale), (6*scale, 6*scale)])
            
        self.rect = self.image.get_rect(center=(x, y))
        
    def draw(self, surface):
        if self.visible:
            surface.blit(self.image, self.rect)
            
    def get_rect(self):
        return self.rect
        
    def collecter(self):
        self.visible = False
        self.collected = True


class Gestion_objets:
    """Gère les objets du jeu"""
    def __init__(self, scale):
        self.items = []
        self.scale = scale
        self.spawn_positions = {
            "room2": [(150, 200), (600, 500), (400, 350), (200, 400)],
            "room3": [(300, 300), (450, 200), (250, 450), (500, 300)],
            "room4": [(400, 400), (300, 300), (500, 300), (200, 200)]
        }
        
    def spawn_balle_rouge(self, room):
        """Fait apparaître une boule rouge"""
        pos = random.choice(self.spawn_positions.get(room, [(400, 400)]))
        ball = Balle_rouge(pos[0], pos[1], self.scale)
        ball.room = room
        self.items.append(ball)
        return ball

    def spawn_etoile(self, room):
        """Fait apparaître une étoile"""
        pos = random.choice(self.spawn_positions.get(room, [(400, 400)]))
        star = Etoile(pos[0], pos[1], self.scale)
        star.room = room
        self.items.append(star)
        return star
        
    def spawn_aleatoire(self, room):
        """Spawn soit une boule soit une étoile"""
        # Vérifier combien de boules rouges sont actives
        red_balls_count = sum(1 for item in self.items if item.type == "red_ball" and item.visible)
        
        # S'il n'y a pas de boule rouge, on en force une pour la survie !
        if red_balls_count == 0:
            return self.spawn_balle_rouge(room)
            
        # Sinon aléatoire classique
        if random.random() < 0.4: # 40% chance boule rouge
            return self.spawn_balle_rouge(room)
        else:
            return self.spawn_etoile(room)
        
    def update(self):
        pass
            
    def draw(self, surface, current_room):
        for item in self.items:
            if item.room == current_room:
                item.draw(surface)
                
    def verifier_collision(self, player_rect, current_room, game_state):
        for item in self.items:
            if item.room == current_room and item.visible:
                if player_rect.colliderect(item.rect):
                    item.collecter()
                    # Effet specifique selon le type
                    if item.type == "red_ball":
                        game_state['degradation'] = max(0, game_state['degradation'] - 0.2)  # reduit de 20% la dégradation
                    elif item.type == "star":
                        game_state['score'] += 100
                        game_state['stars_collected'] = game_state.get('stars_collected', 0) + 1
                        # Augmenter la vitesse de dégradation tous les 3 étoiles
                        if game_state['stars_collected'] % 2 == 0:
                            game_state['degradation_speed'] = game_state.get('degradation_speed', 0.0008) * 1.3
                    return item
        return None
        
    def supprimer_collectes(self):
        self.items = [i for i in self.items if not i.collected]
