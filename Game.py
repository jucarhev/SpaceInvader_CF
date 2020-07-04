import pygame
import random, sys

# varianbles globales
ancho = 900
alto = 480
listaEnemigos = []

class Proyectil(pygame.sprite.Sprite):
    def __init__(self, posX, posY, ruta, personaje):
        pygame.sprite.Sprite.__init__(self)

        self.imagenProyectil = pygame.image.load(ruta)

        self.rect = self.imagenProyectil.get_rect()

        self.velocidadDisparo = 5

        self.rect.top = posY
        self.rect.left = posX

        self.disparoPersonaje = personaje
    
    def trayectoria(self):
        if self.disparoPersonaje == True:
            self.rect.top = self.rect.top - self.velocidadDisparo
        else:
            self.rect.top = self.rect.top + self.velocidadDisparo
    
    def dibujar(self, screen):
        screen.blit(self.imagenProyectil, self.rect)

class naveEspacial(pygame.sprite.Sprite):
    """ Clase para naves """
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.ImagenNave = pygame.image.load("img/nave.jpg")
        self.ImagenExplosion = pygame.image.load("img/explosion.jpg")

        # Obtenesmos los artibutos del objeto
        self.rect = self.ImagenNave.get_rect()
        self.rect.centerx = ancho / 2
        self.rect.centery = alto - 30

        self.listaDisparo = []
        self.Vida = True

        self.velocidad = 40
    
    def destruccion(self):
        self.Vida = False
        self.velocidad = 0
        self.ImagenNave = self.ImagenExplosion

    def movimientoDerecha(self):
        self.rect.right += self.velocidad
        self.movimiento()
    
    def movimientoIzquierda(self):
        self.rect.left -= self.velocidad
        self.movimiento()
    
    def movimiento(self):
        if self.Vida == True:
            if self.rect.left <= 0:
                self.rect.left = 0
            elif self.rect.right >= 840:
                self.rect.right = 860

    def disparar(self, x, y):
        miProyectil = Proyectil(x, y, "img/disparoa.jpg", True )
        self.listaDisparo.append(miProyectil)

    def dibujar(self, superficie):
        superficie.blit(self.ImagenNave, self.rect)

class Enemigo(pygame.sprite.Sprite):
    def __init__(self, posX, posY, distancia, imagenUno, imagenDos):
        pygame.sprite.Sprite.__init__(self)

        self.imagenA = pygame.image.load("img/MarcianoA.jpg")
        self.imagenB = pygame.image.load("img/MarcianoB.jpg")

        self.listaImagenes = [self.imagenA, self.imagenB]
        self.posImagen = 0
        
        self.imagenInvasor = self.listaImagenes[self.posImagen]
        self.rect = self.imagenInvasor.get_rect()

        self.velocidad = 1
        self.listaDisparo = []
        self.rect.top = posY
        self.rect.left = posX

        self.tiempoCambio = 1
        self.rangoDisparo = 3

        self.conquista = False

        self.derecha = True
        self.contador = 0
        self.maximoDescenso = self.rect.top + 40

        self.limiteDerecha = posX + distancia
        self.limiteIzquierda = posX - distancia
    
    def dibujar(self, screen):
        self.imagenInvasor = self.listaImagenes[self.posImagen]
        screen.blit(self.imagenInvasor, self.rect)
    
    def comportamient(self, tiempo):
        if self.conquista == False:
            self.movimientos()
            self.ataque()
            if self.tiempoCambio == tiempo:
                self.posImagen += 1
                self.tiempoCambio += 1

                if self.posImagen > len(self.listaImagenes) -1:
                    self.posImagen = 0
        
    def ataque(self):
        if random.randint(0,1000) < self.rangoDisparo:
            self.disparo()

    def disparo(self):
        x, y = self.rect.center
        miProyectil = Proyectil(x, y, "img/disparob.jpg", False)
        self.listaDisparo.append(miProyectil)
    
    def movimientos(self):
        if self.contador < 3:
            self.movimiento_lateral()
        else:
            self.descenso()
    
    def descenso(self):
        if self.maximoDescenso == self.rect.top:
            self.contador = 0
            self.maximoDescenso = self.rect.top + 40
        else:
            self.rect.top += 1
    
    def movimiento_lateral(self):
        if self.derecha == True:
            self.rect.left = self.rect.left + self.velocidad
            if self.rect.left > self.limiteDerecha:
                self.derecha = False

                self.contador += 1
        else:
            self.rect.left = self.rect.left - self.velocidad
            if self.rect.left < self.limiteIzquierda:
                self.derecha = True

def cargarEnemigos():
    posx = 100
    for x in range(1,5):
        enemigo = Enemigo(posx,100, 40, "img/MarcianoA.jpg", "img/MarcianoB.jpg")
        listaEnemigos.append(enemigo)
        posx = posx + 200
    
    posx = 100
    for x in range(1,5):
        enemigo = Enemigo(posx,0, 40, "img/Marciano2A.jpg", "img/Marciano3B.jpg")
        listaEnemigos.append(enemigo)
        posx = posx + 200
    
    posx = 100
    for x in range(1,5):
        enemigo = Enemigo(posx,-100, 40, "img/Marciano3A.jpg", "img/Marciano3B.jpg")
        listaEnemigos.append(enemigo)
        posx = posx + 200

def detenerTodo():
    for enemigo in listaEnemigos:
        for disparo in enemigo.listaDisparo:
            enemigo.listaDisparo.remove(disparo)
        
        enemigo.conquista = True

def SpaceInvader():
    pygame.init()
    screen = pygame.display.set_mode( (ancho, alto) )
    pygame.display.set_caption("SpaceInvader")

    MiFuenteSistema = pygame.font.SysFont('Arial', 30)
    Texto = MiFuenteSistema.render("Fin del juego", 0, (120,100,40))

    pygame.mixer.music.load("sounds/SpaceInvaders.mp3")
    pygame.mixer.music.play(3)

    ImagenFondo = pygame.image.load("img/Fondo.jpg")

    jugador = naveEspacial()

    enJuego = True

    #DemoProyectil = Proyectil(ancho/2, alto-30)
    cargarEnemigos()

    reloj = pygame.time.Clock()

    while True:
        # verificar donde esta la nave
        #jugador.movimiento()

        reloj.tick(60)
        #tiempo = pygame.time.get_ticks() / 1000
        #tiempo = round(pygame.time.get_ticks()/1000,0)
        tiempo = int(pygame.time.get_ticks()/1000.0)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            if enJuego == True:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        jugador.movimientoIzquierda()
                    elif event.key == pygame.K_RIGHT:
                        jugador.movimientoDerecha()
                    elif event.key == pygame.K_s:
                        x, y = jugador.rect.center
                        jugador.disparar(x, y)
        
        screen.blit(ImagenFondo, (0,0))

        if len(jugador.listaDisparo) > 0:
            for x in jugador.listaDisparo:
                x.dibujar(screen)
                x.trayectoria()
                
                if x.rect.top < 50:
                    jugador.listaDisparo.remove(x)
                else:
                    for enemigo in listaEnemigos:
                        if x.rect.colliderect(enemigo):
                            listaEnemigos.remove(enemigo)
                            jugador.listaDisparo.remove(x)
        
        if len(listaEnemigos) > 0:
            for enemigo in listaEnemigos:
                enemigo.comportamient(tiempo)
                enemigo.dibujar(screen)

                if enemigo.rect.colliderect(jugador.rect):
                    enJuego = False
                    detenerTodo()
                    jugador.destruccion()

               
                if len(enemigo.listaDisparo) > 0:
                    for x in enemigo.listaDisparo:
                        x.dibujar(screen)
                        x.trayectoria()

                        if x.rect.colliderect(jugador.rect):
                            enJuego = False
                            detenerTodo()
                            jugador.destruccion()
                        
                        if x.rect.top > 900:
                            enemigo.listaDisparo.remove(x)
                        else: 
                            for disparo in jugador.listaDisparo:
                                if x.rect.colliderect(disparo.rect):
                                    jugador.listaDisparo.remove(disparo)
                                    enemigo.listaDisparo.remove(x)

        jugador.dibujar(screen)

        if enJuego == False:
            pygame.mixer.music.fadeout(3000)
            screen.blit(Texto, (300,300))
        pygame.display.update()

SpaceInvader()