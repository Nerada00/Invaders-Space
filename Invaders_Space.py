import pygame
import random
import time
import math
from pygame import mixer
import collisions

pygame.init()

class Orbe(pygame.sprite.Sprite):

    def __init__ (self,joueur):
        super().__init__()
        self.vitesse = 7
        self.joueur = joueur
        self.image = pygame.image.load ('Sprites/feu.png')
        self.image = pygame.transform.scale(self.image,(10,10)) #modifier la taille de l'image
        self.rect = self.image.get_rect()
        self.rect.x = joueur.rect.x +20
        self.rect.y = joueur.rect.y +10
        self.origin_image = self.image
        self.angle = 0

    def rotation (self):
        #tourner l'orbe
        self.angle += 12
        self.image = pygame.transform.rotozoom(self.origin_image,self.angle,1)
        self.rect = self.image.get_rect(center=self.rect.center) #effet de rotation fluide

    def remove(self):
        #supprimer l'orbe
        self.joueur.plusieur_orbes.remove(self)


    def mouvement (self):
        self.rect.y -= self.vitesse
        self.rotation()
        #verifier l'orbe sur la collision du bot
        for bot in self.joueur.jeu.check_collision(self,self.joueur.jeu.all_bot):
            self.remove()
            #degat
            bot.degat(self.joueur.atk)

        for bot2 in self.joueur.jeu.check_collision(self,self.joueur.jeu.all_bot2):
            self.remove()
            #degat
            bot2.degat(self.joueur.atk)

        for bot3 in self.joueur.jeu.check_collision(self,self.joueur.jeu.all_bot3):
            self.remove()
            #degat
            bot3.degat(self.joueur.atk)

        for powerup in self.joueur.jeu.check_collision(self,self.joueur.jeu.all_powerups1):
            self.remove()
            powerup.degat(self.joueur.atk)
            powerup.bonus()

        for powerup in self.joueur.jeu.check_collision(self,self.joueur.jeu.all_powerups2):
            self.remove()
            powerup.degat(self.joueur.atk)
            powerup.bonus()

        for powerup in self.joueur.jeu.check_collision(self,self.joueur.jeu.all_powerups3):
            self.remove()
            powerup.degat(self.joueur.atk)
            powerup.bonus()

        for bonus in self.joueur.jeu.check_collision(self,self.joueur.jeu.all_bonusexp):
            self.remove()
            bonus.degat(self.joueur.atk)
            bonus.bonification()

        for killall in self.joueur.jeu.check_collision(self,self.joueur.jeu.all_killall):
            self.remove()
            killall.degat(self.joueur.atk)
            killall.overkill()

        #verifier si l'orbe est supprimé de l'ecran
        if self.rect.y < 0:
            self.remove()

class Orbe2(pygame.sprite.Sprite):

    def __init__ (self,joueur):
        super().__init__()
        self.vitesse = 10
        self.joueur = joueur
        self.image = pygame.image.load ('Sprites/eclair.png')
        self.image = pygame.transform.scale(self.image,(50,150))
        self.rect = self.image.get_rect()
        self.rect.x = joueur.rect.x
        self.rect.y = joueur.rect.y -115
        self.angle = 0

    def remove(self):
    #supprimer l'orbe
        self.joueur.plusieur_tonerre.remove(self)

    def mouvement (self):
        self.rect.y -= self.vitesse
        #verifier l'orbe sur la collision du bot
        for bot in self.joueur.jeu.check_collision(self,self.joueur.jeu.all_bot):
            #degat
            bot.degat(self.joueur.atk2)

        for bot2 in self.joueur.jeu.check_collision(self,self.joueur.jeu.all_bot2):
            #degat
            bot2.degat(self.joueur.atk2)

        for bot3 in self.joueur.jeu.check_collision(self,self.joueur.jeu.all_bot3):
            #degat
            bot3.degat(self.joueur.atk2)

        for bonus in self.joueur.jeu.check_collision(self,self.joueur.jeu.all_bonusexp):
            self.remove()
            bonus.degat(self.joueur.atk2)
            bonus.bonification()

        for killall in self.joueur.jeu.check_collision(self,self.joueur.jeu.all_killall):
            self.remove()
            killall.degat(self.joueur.atk2)
            killall.overkill()



        #verifier si l'orbe est supprimé de l'ecran
        if self.rect.y < -20:
            self.remove()


class Bot(pygame.sprite.Sprite):

    def __init__(self,jeu):
        super().__init__()
        self.jeu = jeu
        self.vie = 50
        self.max_vie = 50
        self.atk = 1
        self.atkc = 30
        self.image = pygame.image.load('Sprites/minirobot.png')
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0,300)
        self.rect.y = -20
        self.vitesse = random.randint(1,3)


    def degat(self, montant):
        #infliger les degats
        self.vie -= montant

        #verifier les points de vie si <= 0
        if self.vie <= 0:
            #reaparaitre comme nvx bot
            self.respawn()

    def respawn(self):
        self.rect.x =  random.randint(0,400)
        self.rect.y =  -20
        self.vitesse = random.randint(1,3)
        self.vie = self.max_vie
        self.jeu.score+=20

    def update_vie(self,surface):

        #dessiner la barre de vie (background)
        pygame.draw.rect(surface, (60,63,60), [self.rect.x -10 , self.rect.y  ,self.max_vie, 4 ])
        #dessiner la barre de vie
        pygame.draw.rect(surface, (111,210,46), [self.rect.x -10 , self.rect.y  ,self.vie, 4 ])


    def avancer(self):
        if self.rect.y >700:
            self.degat(100)
            self.jeu.joueur.damage(self.atkc)
        #deplacer que si il n'y a pas de collision
        if not self.jeu.check_collision(self,self.jeu.all_joueur):
            if self.jeu.powerup2_actif == "oui" and self.rect.y>=0:
                self.vitesse = self.vitesse//2
                self.rect.y += self.vitesse
            self.rect.y += self.vitesse
        else:
            self.jeu.joueur.damage(self.atk)


class Bot2(pygame.sprite.Sprite):

    def __init__(self,jeu):
        super().__init__()
        self.jeu = jeu
        self.vie = 20
        self.max_vie = 20
        self.atk = 0.5
        self.atkc = 10
        self.image = pygame.image.load('Sprites/Robot4.png')
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0,400)
        self.rect.y = -400
        self.vitesse = random.randint(3,4)


    def degat(self, montant):
        #infliger les degats
        self.vie -= montant

        #verifier les points de vie si <= 0
        if self.vie <= 0:
            #reaparaitre comme nvx bot
            self.respawn()


    def respawn(self):
        self.rect.x =  random.randint(0,400)
        self.rect.y =  -400
        self.vitesse = random.randint(3,4)
        self.vie = self.max_vie
        self.jeu.score+=30

    def update_vie(self,surface):

        #dessiner la barre de vie (background)
        pygame.draw.rect(surface, (60,63,60), [self.rect.x + 15, self.rect.y  ,self.max_vie, 4 ])
        #dessiner la barre de vie
        pygame.draw.rect(surface, (111,210,46), [self.rect.x +15, self.rect.y  ,self.vie, 4 ])


    def avancer2(self):
        if self.rect.y >700:
            self.degat(100)
            self.jeu.joueur.damage(self.atkc)
        #deplacer que si il n'y a pas de collision
        if not self.jeu.check_collision(self,self.jeu.all_joueur):
            if self.jeu.powerup2_actif == "oui" and self.rect.y>=0:
                self.vitesse = self.vitesse//2
                self.rect.y += self.vitesse
            self.rect.y += self.vitesse
        else:
            self.jeu.joueur.damage(self.atk)



class Bot3(pygame.sprite.Sprite):

    def __init__(self,jeu):
        super().__init__()
        self.jeu = jeu
        self.vie = 150
        self.max_vie = 150
        self.atk = 2
        self.atkc = 50   #degat bas de la fenetre
        self.image = pygame.image.load('Sprites/Robot3.png')
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0,300)
        self.rect.y = -350
        self.vitesse = 1


    def degat(self, montant):
        #infliger les degats
        self.vie -= montant

        #verifier les points de vie si <= 0
        if self.vie <= 0:
            #reaparaitre comme nvx bot
            self.respawn()

    def respawn(self):
        self.rect.x =  random.randint(0,400)
        self.rect.y =  -350
        self.vitesse = 1
        self.vie = self.max_vie
        self.jeu.score+=40

    def update_vie(self,surface):

        #dessiner la barre de vie (background)
        pygame.draw.rect(surface, (60,63,60), [self.rect.x -30 , self.rect.y  ,self.max_vie, 4 ])
        #dessiner la barre de vie
        pygame.draw.rect(surface, (111,210,46), [self.rect.x -30 , self.rect.y  ,self.vie, 4 ])


    def avancer3(self):
        if self.rect.y >700:
            self.degat(100)
            self.jeu.joueur.damage(self.atkc)
        #deplacer que si il n'y a pas de collision
        if not self.jeu.check_collision(self,self.jeu.all_joueur):
            if self.jeu.powerup2_actif == "oui" and self.rect.y>=0:
                self.vitesse = self.vitesse//2
                self.rect.y += self.vitesse
            self.rect.y += self.vitesse
        else:
            self.jeu.joueur.damage(self.atk)

#########################################################################################################

class Powerup1(pygame.sprite.Sprite):

    def __init__(self,jeu,joueur):
        super().__init__()
        self.jeu = jeu
        self.joueur = joueur
        self.vie = 1
        self.image = pygame.image.load('Sprites/bullerouge.png')
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0,400)
        self.rect.y = -20
        self.vitesse = 2


    def degat(self, montant):
        #infliger les degats
        self.vie -= montant

        #verifier les points de vie si <= 0
        if self.vie <= 0:
            self.rect.x = random.randint(0,400)
            self.rect.y = -530

    def avancer(self):
        if not self.jeu.check_collision(self,self.joueur.plusieur_orbes):
            self.rect.y += self.vitesse
            if self.rect.y>=-30 and self.jeu.powerup1_actif == "oui":
                self.jeu.powerup1_actif = "non"
                self.rect.y = -2000
            if self.rect.y>800:
                self.rect.x = random.randint(0,400)
                self.rect.y = -2000

    def bonus(self):
        self.jeu.powerup1_actif = "oui"

########################################################################################################

class Powerup2(pygame.sprite.Sprite):

    def __init__(self,jeu,joueur):
        super().__init__()
        self.jeu = jeu
        self.joueur = joueur
        self.vie = 1
        self.image = pygame.image.load('Sprites/bullebleue.png')
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0,400)
        self.rect.y = -1300
        self.vitesse = 3


    def degat(self, montant):
        #infliger les degats
        self.vie -= montant

        #verifier les points de vie si <= 0
        if self.vie <= 0:
            self.rect.x = random.randint(0,400)
            self.rect.y = -510

    def avancer(self):
        if not self.jeu.check_collision(self,self.joueur.plusieur_orbes):
            self.rect.y += self.vitesse
            if self.rect.y>=-30 and self.jeu.powerup2_actif == "oui":
                self.jeu.powerup2_actif = "non"
                self.rect.y = -3000
            if self.rect.y>800:
                self.rect.x = random.randint(0,400)
                self.rect.y = -3000

    def bonus(self):
        self.jeu.powerup2_actif = "oui"

#########################################################################################################

class Powerup3(pygame.sprite.Sprite):

    def __init__(self,jeu,joueur):
        super().__init__()
        self.jeu = jeu
        self.joueur = joueur
        self.vie = 1
        self.image = pygame.image.load('Sprites/bullejaune.png')
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0,400)
        self.rect.y = -2000
        self.vitesse = 4


    def degat(self, montant):
        #infliger les degats
        self.vie -= montant

        #verifier les points de vie si <= 0
        if self.vie <= 0:
            self.rect.x = random.randint(0,400)
            self.rect.y = -500

    def avancer(self):
        if not self.jeu.check_collision(self,self.joueur.plusieur_orbes):
            self.rect.y += self.vitesse
            if self.rect.y>=-30 and self.jeu.powerup3_actif == "oui":
                self.jeu.powerup3_actif = "non"
                self.rect.y = -4000
            if self.rect.y>800:
                self.rect.x = random.randint(0,400)
                self.rect.y = -4000

    def bonus(self):
        self.jeu.powerup3_actif = "oui"

#########################################################################################################

class BonusExp(pygame.sprite.Sprite):

    def __init__(self,jeu,joueur):
        super().__init__()
        self.jeu = jeu
        self.joueur = joueur
        self.vie = 1
        self.image = pygame.image.load('Sprites/bulleblanche.png')
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0,400)
        self.rect.y = -500
        self.vitesse = 1.5


    def degat(self, montant):
        #infliger les degats
        self.vie -= montant

        #verifier les points de vie si <= 0
        if self.vie <= 0:
            self.rect.x = random.randint(0,400)
            self.rect.y = -800

    def avancer(self):
        if not self.jeu.check_collision(self,self.joueur.plusieur_orbes):
            self.rect.y += self.vitesse
        if self.rect.y>800:
                self.rect.x = random.randint(0,400)
                self.rect.y = -800

    def bonification(self):
        self.jeu.score += 100

#########################################################################################################

class KillAll(pygame.sprite.Sprite):

    def __init__(self,jeu,joueur):
        super().__init__()
        self.jeu = jeu
        self.joueur = joueur
        self.vie = 1
        self.image = pygame.image.load('Sprites/bulleviolette.png')
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0,400)
        self.rect.y = -3500
        self.vitesse = 5


    def degat(self, montant):
        #infliger les degats
        self.vie -= montant

        #verifier les points de vie si <= 0
        if self.vie <= 0:
            self.rect.x = random.randint(0,400)
            self.rect.y = -2500

    def avancer(self):
        if not self.jeu.check_collision(self,self.joueur.plusieur_orbes):
            self.rect.y += self.vitesse
        if self.rect.y>800:
                self.rect.x = random.randint(0,400)
                self.rect.y = -2500

    def overkill(self):
        for bot in self.jeu.all_bot:
            bot.respawn()
        for bot in self.jeu.all_bot2:
            bot.respawn()
        for bot in self.jeu.all_bot3:
            bot.respawn()

#########################################################################################################

class Jeu():

    def __init__(self):
        self.is_playing = False
        self.all_joueur = pygame.sprite.Group()
        self.joueur = Joueur(self)
        self.all_joueur.add(self.joueur)
        self.pressed = {}
        self.all_bot = pygame.sprite.Group()
        self.all_bot2 = pygame.sprite.Group()
        self.all_bot3 = pygame.sprite.Group()
        self.all_powerups1 = pygame.sprite.Group()
        self.all_powerups2 = pygame.sprite.Group()
        self.all_powerups3 = pygame.sprite.Group()
        self.all_bonusexp = pygame.sprite.Group()
        self.all_killall = pygame.sprite.Group()
        self.powerup1_actif = "non"
        self.powerup2_actif = "non"
        self.powerup3_actif = "non"
        self.score = 0
        self.fin_de_partie = "non"


    def start(self):
        self.is_playing = True
        self.spawn_bot()
        self.spawn_bot()
        self.spawn_bot()
        self.spawn_bot2()
        self.spawn_bot2()
        self.spawn_bot3()
        self.spawn_powerup1()
        self.spawn_powerup2()
        self.spawn_powerup3()
        self.spawn_bonusexp()
        self.spawn_killall()



    def game_over(self):
        self.all_bot = pygame.sprite.Group()
        self.all_bot2 = pygame.sprite.Group()
        self.all_bot3 = pygame.sprite.Group()
        self.all_powerups1 = pygame.sprite.Group()
        self.all_powerups2 = pygame.sprite.Group()
        self.all_powerups3 = pygame.sprite.Group()
        self.all_bonusexp = pygame.sprite.Group()
        self.all_killall = pygame.sprite.Group()
        self.joueur.plusieur_orbes = pygame.sprite.Group()
        self.plusieur_tonerre = pygame.sprite.Group()
        self.score = 0
        self.joueur.vie = self.joueur.max_vie
        self.ecran_game_over()
        self.is_playing = False


    def update(self, fond):
            #appliquer le joueur image
        if self.powerup1_actif == "oui":
            fond.blit(self.joueur.image_p1, self.joueur.rect)
        elif self.powerup2_actif == "oui":
            fond.blit(self.joueur.image_p2, self.joueur.rect)
        elif self.powerup3_actif == "oui":
            fond.blit(self.joueur.image_p3, self.joueur.rect)
        else:
            fond.blit(self.joueur.image, self.joueur.rect)

        #AACTUALISER LA BARRE
        self.joueur.update_vie(fond)

        #recuperer les orbes
        for orbe in self.joueur.plusieur_orbes:
            orbe.mouvement()

        #applique l'orbe
        self.joueur.plusieur_orbes.draw(fond)

        for orbe2 in self.joueur.plusieur_tonerre:
            orbe2.mouvement()

        #afficher le groupe tonerre (laser)
        self.joueur.plusieur_tonerre.draw(fond)

        #recuperer les bots
        for bot in self.all_bot:
            bot.avancer()
            bot.update_vie(fond)

        for bot2 in self.all_bot2:
            bot2.avancer2()
            bot2.update_vie(fond)

        for bot3 in self.all_bot3:
            bot3.avancer3()
            bot3.update_vie(fond)

        #recuperer les powerups
        for powerup in self.all_powerups1:
            powerup.avancer()

        for powerup in self.all_powerups2:
            powerup.avancer()

        for powerup in self.all_powerups3:
            powerup.avancer()

        for bonus in self.all_bonusexp:
            bonus.avancer()

        for killall in self.all_killall:
            killall.avancer()

        #afficher le groupe bot
        self.all_bot.draw(fond)
        self.all_bot2.draw(fond)
        self.all_bot3.draw(fond)

        self.all_powerups1.draw(fond)

        self.all_powerups2.draw(fond)

        self.all_powerups3.draw(fond)

        self.all_bonusexp.draw(fond)

        self.all_killall.draw(fond)

        self.affichage_score()


        #verifier si le joueur veut aller à gauche ou a droite tout en verifiant les coordonnées
        if self.pressed.get(pygame.K_RIGHT) and self.joueur.rect.x < 463:
            self.joueur.deplacement_droite()
        elif self.pressed.get(pygame.K_LEFT) and self.joueur.rect.x >-5:
            self.joueur.deplacement_gauche()



    #fonctions pour faire spawn les bots
    def spawn_bot(self):
        bot = Bot(self)
        self.all_bot.add(bot)

    def spawn_bot2(self):
        bot2 = Bot2(self)
        self.all_bot2.add(bot2)

    def spawn_bot3(self):
        bot3 = Bot3(self)
        self.all_bot3.add(bot3)

    #fonctions pour faire spawn les powerups
    def spawn_powerup1(self):
        powerup1 = Powerup1(self,Joueur(self))
        self.all_powerups1.add(powerup1)

    def spawn_powerup2(self):
        powerup2 = Powerup2(self,Joueur(self))
        self.all_powerups2.add(powerup2)

    def spawn_powerup3(self):
        powerup3 = Powerup3(self,Joueur(self))
        self.all_powerups3.add(powerup3)

    def spawn_bonusexp(self):
        bonusexp = BonusExp(self,Joueur(self))
        self.all_bonusexp.add(bonusexp)

    def spawn_killall(self):
        killall = KillAll(self,Joueur(self))
        self.all_killall.add(killall)


    def affichage_score(self):
        texte = font_score.render("Score : "+str(self.score),1,(255,255,255))
        fond.blit(texte, (0,0))

    def ecran_game_over(self):
        self.fin_de_partie = "oui"


    #fonction de collision des differents Sprites
    def check_collision(self,sprite,group):
        return pygame.sprite.spritecollide(sprite,group, False,pygame.sprite.collide_mask)





class Joueur(pygame.sprite.Sprite):

    def __init__(self,jeu):
        self.jeu = jeu
        super().__init__()
        self.vie = 100
        self.max_vie = 100
        self.atk = 10
        self.atk2 = 2
        self.vitesse = 6
        self.plusieur_orbes = pygame.sprite.Group()
        self.plusieur_tonerre = pygame.sprite.Group()
        self.image = pygame.image.load('Sprites/canon.png')
        self.image_p1 = pygame.image.load('Sprites/CanonRouge.png')
        self.image_p2 = pygame.image.load('Sprites/CanonBleu.png')
        self.image_p3 = pygame.image.load('Sprites/CanonJaune.png')
        self.rect = self.image.get_rect()
        self.rect.x = 100
        self.rect.y = 640

    def damage(self,amount):
        if self.jeu.powerup3_actif == "non":
            if self.vie - amount > amount:
                self.vie -= amount
            else:
                self.jeu.game_over()


        #position_finale,vitesse_finale = collisions.deplacement_contraint((self.rect.x,self.rect.y),(40,80),(0,- (10*(self.saut /2))),jeu.positions_obstacles,jeu.dimensions_obstacles)

        #self.rect.y =position_finale[1]
        #self.rect.x =position_finale[0]


    def update_vie(self,surface):
        #dessiner la barre de vie
        pygame.draw.rect(surface, (60,63,60), [375, 50 ,self.max_vie, 15 ])

        pygame.draw.rect(surface, (111,210,46), [375,  50 ,self.vie, 15 ])



    #lancer l'orbe
    def lanceur(self):
        if self.jeu.powerup1_actif == "oui":
            eclair = Orbe2(self)
            self.plusieur_tonerre.add(Orbe2(self))
        else:
            orbe = Orbe(self)
            self.plusieur_orbes.add(Orbe(self))

    def deplacement_droite(self):
        #collision bot
        if not self.jeu.check_collision(self,self.jeu.all_bot):
            self.rect.x += self.vitesse

    def  deplacement_gauche(self):
        self.rect.x -= self.vitesse


################################################################################
################################################################################

#                              Clock/Info/images                               #

################################################################################
################################################################################


#faire appraître la fenêtre
clock = pygame.time.Clock()

fond = pygame.display.set_mode ((500,700))

LOGO = pygame.image.load ('Sprites/logo.png')
pygame.display.set_caption("Invaders Space premium deluxe edition & Knuckles")
pygame.display.set_icon(LOGO)

font_score = pygame.font.Font("Font/Fresh Lychee.ttf", 30)
font_credits = pygame.font.Font("Font/Fresh Lychee.ttf", 40)
font_game_over = pygame.font.Font("Font/Fresh Lychee.ttf", 120)

#fond du jeu import
background = pygame.image.load ('Sprites/fond.png').convert_alpha()
#musique de background
mixer.music.load('Music/Musique fond.mp3')
mixer.music.play(-1)

#banniere
banner = pygame.image.load ('Sprites/final.png').convert_alpha()
banner_rect = banner.get_rect()
banner = pygame.transform.scale(banner,(400,400))
banner_rect.x = math.ceil( fond.get_width() / 10)
banner_rect.y = math.ceil( fond.get_width() / 8 )

#bouton de lancer
play_button = pygame.image.load ('Sprites/start.png').convert_alpha()
play_button = pygame.transform.scale(play_button,(120,100))
play_button_rect = play_button.get_rect()
play_button_rect.x = math.ceil( fond.get_width() / 2.7 )
play_button_rect.y = math.ceil( fond.get_width() / 1.25 )

#bouton de retry
retry_button = pygame.image.load ('Sprites/retry.png').convert_alpha()
retry_button = pygame.transform.scale(retry_button,(120,100))
retry_button_rect = retry_button.get_rect()
retry_button_rect.x = math.ceil( fond.get_width() / 2.7 )
retry_button_rect.y = math.ceil( fond.get_width() / 1.18 )

#bouton de exit
exit_button = pygame.image.load ('Sprites/exit.png').convert_alpha()
exit_button = pygame.transform.scale(exit_button,(120,100))
exit_button_rect = exit_button.get_rect()
exit_button_rect.x = math.ceil( fond.get_width() / 2.7 )
exit_button_rect.y = math.ceil( fond.get_width() / 0.93 )

#bouton de quit
quit_button = pygame.image.load ('Sprites/exit.png').convert_alpha()
quit_button = pygame.transform.scale(quit_button,(120,100))
quit_button_rect = quit_button.get_rect()
quit_button_rect.x = math.ceil( fond.get_width() / 2.7 )
quit_button_rect.y = math.ceil( fond.get_width() / 1.07 )

#ecran de game over
texte_game_over = font_game_over.render("Game Over",1,(255,0,0))

#chargement du jeu
jeu = Jeu()


#chargement du joueur
joueur = Joueur(jeu)

################################################################################
################################################################################

#                              BOUCLE DU JEU                                   #

################################################################################
################################################################################

running = True
while running:


    #appliquer le background
    fond.blit(background,(0,0))


    #verifer si is_playing debute
    if jeu.is_playing:
        jeu.update(fond)
    #verifier si le jeu na pas commencé
    elif jeu.fin_de_partie == "oui":
        fond.blit(background,(0,0))
        fond.blit(texte_game_over, (37,250))
        fond.blit(retry_button,retry_button_rect)
        fond.blit(exit_button,exit_button_rect)
    else:
        fond.blit(play_button,play_button_rect)
        fond.blit(quit_button,quit_button_rect)
        fond.blit(banner,banner_rect)
        texte = font_credits.render("      By Nerada",1,(156,0,0))
        fond.blit(texte, (95,600))

    #mettre a jour la fenetre
    pygame.display.flip()

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
            print ("fermeture du jeu")

        #detecter les touches
        elif event.type == pygame.KEYDOWN:
            jeu.pressed[event.key] = True

            if event.key == pygame.K_SPACE:
                jeu.joueur.lanceur()

        elif event.type == pygame.KEYUP:
            jeu.pressed [event.key] = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if play_button_rect.collidepoint(event.pos) or retry_button_rect.collidepoint(event.pos):
                jeu.start()

            if exit_button_rect.collidepoint(event.pos):
                jeu.fin_de_partie = "non"

            if quit_button_rect.collidepoint(event.pos):
                running = False
                pygame.quit()
                print ("fermeture du jeu")



    clock.tick(30)
pygame.quit()