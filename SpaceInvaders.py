####################
#Emerson Blanco
#Nicolas Fonseca
#Luis Miguel Correa
###################
import pygame

VENTANA_HORI = 800  # Ancho de la ventana
VENTANA_VERT = 600  # Alto de la ventana
FPS = 60 # Fotogramas por segundo
NEGRO = (0,0,0)

class Juego:
    pantalla = None
    aliens = []
    balas = []
    barrera=[]
    
    lost = False

    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        self.pantalla = pygame.display.set_mode((VENTANA_HORI, VENTANA_VERT))
        self.clock = pygame.time.Clock()

    def comenzar(self):    
        
        background = pygame.image.load("background.jpg").convert()
        nave = pygame.image.load("nave.png").convert()
        mario = pygame.mixer.Sound("mario.wav")
        mario.set_volume(0.5)
        pygame.mixer.Sound.play(mario)
        
        #genAliens = Generador(self)
        genAliens = Seleccion.seleccionar(self,VENTANA_HORI / 2, VENTANA_VERT - 20,'GenAliens')
        #genBarrera = Generadorbarr(self)
        genBarrera = Seleccion.seleccionar(self,VENTANA_HORI / 2, VENTANA_VERT - 20,'GenBarrera')
        #player = Jugador(self, VENTANA_HORI / 2, VENTANA_VERT - 20)
        player = Seleccion.seleccionar(self,VENTANA_HORI / 2, VENTANA_VERT - 20,'Jugador')
        bala = None
        ACTIVO = True

        while ACTIVO:
            if len(self.aliens) == 0:
                self.mensaje("HAS GANADO")
                mario = pygame.mixer.Sound("final.wav")
                mario.set_volume(0.5)
                pygame.mixer.Sound.play(mario)
               

            tecla = pygame.key.get_pressed()
            if tecla[pygame.K_LEFT]:  # flecha izquierda
                player.x -= 3 if player.x > 20 else 0  # borde del área izquierda
            elif tecla[pygame.K_RIGHT]:  # flecha derecha
                player.x += 3 if player.x < VENTANA_HORI - 20 else 0  # borde del área derecha
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    ACTIVO = False

                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and not self.lost:
                    #self.balas.append(Bala(self, player.x, player.y))
                    bala = Seleccion.seleccionar(self,player.x, player.y,'Bala')
                    self.balas.append(bala)

            pygame.display.flip()
            self.clock.tick(FPS)
            self.pantalla.blit(background, [0, 0])

            self.pantalla.blit(nave, [player.x-15, 600-50])
            for alien in self.aliens:
                alien.dibujar()
                alien.Colision(self)
                if (alien.y > VENTANA_VERT):
                    self.lost = True
                    sonido_fondo = pygame.mixer.Sound("GameOver.wav")
                    sonido_fondo.set_volume(0.05)
                    self.mensaje("GAME OVER")
                    pygame.mixer.Sound.play(sonido_fondo)
            for barrera in self.barrera:
                barrera.dibujar()
                barrera.Colision(self)
            for bala in self.balas:
                bala.dibujar()

            if not self.lost: 
                player.dibujar()
    
    def mensaje(self, texto):
        pygame.font.init()
        font = pygame.font.SysFont('Times New Roman', 60)
        textsurface = font.render(texto, False, (230, 235, 235))
        self.pantalla.blit(textsurface, ((VENTANA_HORI/2) - 150, 200))

class Generador:
    def __init__(self, juego : Juego):
        margen = 45  # espacio desde el borde de la pantalla
        ancho = 45  # brecha entre extraterrestres
        for x in range(margen, VENTANA_HORI - margen, ancho):
            for y in range(-margen*4, int(VENTANA_VERT/ancho), ancho):
                #juego.aliens.append(Alien(juego, x, y))
                juego.aliens.append(Seleccion.seleccionar(juego, x, y, 'Alien'))

class Generadorbarr:
    def __init__(self, juego : Juego):
        margen = 30  
        ancho = 45  
        for x in range(margen, VENTANA_HORI - margen, ancho):
            for y in range(-margen*4, int(4), ancho):
                #juego.barrera.append(Barrera(juego, x, y))
                juego.barrera.append(Seleccion.seleccionar(juego,x,y,'Barrera'))

class Barrera:
    def __init__(self, juego : Juego, x, y):
        self.x = x
        self.juego = juego
        self.y = y
        self.size = 35

    def dibujar(self):
        pygame.draw.rect(self.juego.pantalla,(255,255,255), pygame.Rect(self.x, self.y, self.size, self.size))
        self.y = 400
        
    def Colision(self, juego : Juego):
        for bala in juego.balas:
            if (bala.x < self.x + self.size and
                    bala.x > self.x - self.size and
                    bala.y < self.y + self.size and
                    bala.y > self.y - self.size):
                juego.balas.remove(bala)
                juego.barrera.remove(self)
                sonido_fondo = pygame.mixer.Sound("explosion.wav")
                sonido_fondo.set_volume(0.05)
                pygame.mixer.Sound.play(sonido_fondo)

class Jugador:
    def __init__(self, juego : Juego, x, y):
        self.x = x
        self.juego = juego
        self.y = y
        
    def dibujar(self):
        pygame.draw.rect(self.juego.pantalla,(0,0,0,0.1),pygame.Rect(self.x, self.y, 30, 1))
        
class Bala:
    def __init__(self, juego : Juego, x, y):
        self.x = x
        self.y = y
        self.juego = juego
       
    def dibujar(self):
        pygame.draw.rect(self.juego.pantalla,(0, 0, 0),pygame.Rect(self.x, self.y, 6, 12))
        self.y -= 6
        bala = pygame.image.load("bullet.png").convert()
        self.juego.pantalla.blit(bala, [ self.x, self.y])
        # sonido_fondo = pygame.mixer.Sound("bulletShoot.wav")
        # sonido_fondo.set_volume(0.05)
        # pygame.mixer.Sound.play(sonido_fondo,0)
        
class Alien:
    def __init__(self, juego, x, y):
        self.x = x
        self.juego = juego
        self.y = y
        self.size = 20

    def dibujar(self):
        pygame.draw.rect(self.juego.pantalla,(0,0,0,0.0), pygame.Rect(self.x, self.y, self.size, self.size))
        self.y += 0.4
        alien = pygame.image.load("bot.png").convert()
        self.juego.pantalla.blit(alien, [ self.x, self.y])

    def Colision(self, juego):
        for bala in juego.balas:
            if (bala.x < self.x + self.size and
                    bala.x > self.x - self.size and
                    bala.y < self.y + self.size and
                    bala.y > self.y - self.size):
                juego.balas.remove(bala)
               
                sonido_fondo = pygame.mixer.Sound("Alienkilled.wav")
                sonido_fondo.set_volume(1)
                pygame.mixer.Sound.play(sonido_fondo)
                juego.aliens.remove(self)

##-----------------------------------------------------------------------------------------
class Seleccion:
    def seleccionar(juego:Juego, x, y,objeto):
        if objeto != 'GenBarrera' and objeto != 'GenAliens':
            componente = JuegoFactory.get_componente(objeto)(juego,x,y)
        else:
            componente = JuegoFactory.get_componente(objeto)(juego)
        return componente


class JuegoFactory:
    def get_componente(objeto):
        if objeto == 'Alien':
            return Alien
        elif objeto == 'Bala':
            return Bala
        elif objeto == 'Jugador':
            return Jugador
        elif objeto == 'Barrera':
            return Barrera
        elif objeto == 'GenBarrera':
            return Generadorbarr
        elif objeto == 'GenAliens':
            return Generador
        else:
            raise ValueError(objeto) 


if __name__ == "__main__":
    juego = Juego()
    juego.comenzar()
    
