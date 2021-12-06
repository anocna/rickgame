from os import kill
import pygame
import random
import time

from pygame import sprite
from pygame import draw
from pygame.constants import K_a

#Tamaño de pantalla
ANCHO = 800
ALTO = 400

#FPS
FPS = 40

# Paleta de colores
NEGRO = (0,0,0)
BLANCO = (255,255,255)
ROJO = (255,0,0)
NARANJA = (255,128,0)
VERDE= (0,255,0)
AZUL = (0,0,255)
CELESTE = (94,210,254)

# Fuente
consolas = pygame.font.match_font('consolas')

class Jugador(pygame.sprite.Sprite):
    # Sprite del jugador
    def __init__(self):
        # Heredamos el init de la clase Sprite de Pygame
        super().__init__()
        # Personaje
        self.image = pygame.image.load("imagenes/rick.png").convert()
        # Obtiene el jugador (sprite)
        self.rect = self.image.get_rect()
        # Generamos un circulo para evitar choques falsos
        self.radius = 25
        # Quitamos el fondo borde negro
        self.image.set_colorkey(NEGRO)
        # Centra el jugador (sprite)
        self.rect.center = (0, ALTO // 2)
        # Movimiento del jugador
        self.px = 0
        self.py = 0
        # Campo protector
        self.campo = False
        # Vidas
        self.vidas = 3
        # Condicionamos el tiempo de inmunidad
        self.cadencia = 1010
        self.ultima_inmunidad = pygame.time.get_ticks()



    def update(self):
                
        # Velocidad 0 a cada actualizacion para frenar el personaje
        self.px = 0
        self.py = 0

        # Opcion de tecla pulsada
        keys = pygame.key.get_pressed()
        # Tecla arriba
        if keys[pygame.K_UP]:
            self.py -= 4
        # Tecla abajo
        if keys[pygame.K_DOWN]:
            self.py += 5
        # Tecla derecha
        if keys[pygame.K_RIGHT]:
            self.px += 4
        # Tecla izquierda
        if keys[pygame.K_LEFT]:
            self.px -= 5
        # Tecla espacio
        if keys[pygame.K_SPACE]:
            self.campo = True
            self.image = pygame.image.load("imagenes/campo.png").convert()
            self.image.set_colorkey(BLANCO)
        else:
            self.campo = False
            self.image = pygame.image.load("imagenes/rick.png").convert()
            self.image.set_colorkey(NEGRO)

        #Actualizamos la posicion del personaje
        self.rect.x += self.px
        self.rect.y += self.py

        # Limitamos los margenes para el personaje
        if self.rect.right > ANCHO:
            self.rect.right = ANCHO
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.bottom > ALTO:
            self.rect.bottom = ALTO
        if self.rect.top < 0:
            self.rect.top = 0

class Roca(pygame.sprite.Sprite):
    # Sprite de la roca
    def __init__(self):
        # Heredamos el init de la clase Sprite de Pygame
        super().__init__()
        # Roca
        self.image = pygame.image.load("imagenes/roca.png").convert()
        # Obtiene el rectángulo (sprite)
        self.rect = self.image.get_rect()
        self.image.set_colorkey(NEGRO)
        # Generamos un circulo para evitar choques falsos
        self.radius = 20
        # posiciones aleatorias 
        self.rect.y = random.randrange(ALTO - self.rect.height)
        self.rect.x = - self.rect.width
        # Movimiento de la roca
        self.px = random.randrange(1,6)

    def update(self):
        #Actualizamos la posicion del personaje
        self.rect.x -= self.px
        # Limitamos los margenes para el personaje
        if self.rect.left < 0:
            self.rect.x = ANCHO
            # Que tome una velocidad diferente
            self.px = random.randrange(1,6)
            # y posicion diferente
            self.rect.y = random.randrange(ALTO - self.rect.height)

class Diamante(pygame.sprite.Sprite):
    # Sprite del diamante
    def __init__(self):
        # Heredamos el init de la clase Sprite de Pygame
        super().__init__()
        # diamante
        self.image = pygame.image.load("imagenes/diamante.png").convert()
        # Obtiene el rectángulo (sprite)
        self.rect = self.image.get_rect()
        self.image.set_colorkey(NEGRO)
        # Generamos un circulo para evitar choques falsos
        self.radius = 20
        # posiciones aleatorias 
        self.rect.y = random.randrange(ALTO - self.rect.height)
        self.rect.x = random.randrange(ANCHO - self.rect.width)
        self.contador = pygame.time.get_ticks()
        self.numero = 300
        self.puntos = 0



# Inicialización de Pygame, creación de la ventana, título y control de reloj.
pygame.init()
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Seminario de Lenguajes")
clock = pygame.time.Clock()

# Puntuaciones
puntuacion = 0

def muestra_texto(pantalla,fuente,texto,color, dimensiones, x, y):
    tipo_letra = pygame.font.Font(fuente,dimensiones)
    superficie = tipo_letra.render(texto,True, color)
    rectangulo = superficie.get_rect()
    rectangulo.center = (x, y)
    pantalla.blit(superficie,rectangulo)
        
        

# Cargo el fondo
fondo = pygame.transform.scale(pygame.image.load("imagenes/universo.jpg").convert(),(800,400))
#el convert es para que ajuste la imajen y corra mejor el juego
x=0 #fondo1 para q el fondo se mueva cambiamos la x por una variable la cual iremos alterando


# Agregamos icono a la ventana
icono = pygame.image.load("imagenes/unla_logo.png")
pygame.display.set_icon(icono)


# Música de fondo
pygame.mixer.music.load('sonidos/car-drive-561.mp3')
pygame.mixer.music.play(-1)


#Grupo de sprites, instanciación de objetos.
sprites = pygame.sprite.Group()
rocas = pygame.sprite.Group()
diamantes = pygame.sprite.Group()
dificultad = 6 # variante a la cual iremos incrementando
niveles = 1


# Ingresamos diamantes aleatorios
def generar_diamantes():
    puntuacion = 0
    for x in range (0,dificultad): #(random.randrange(dificultad)+2): # el mas dos es para que minimo aparezcan dos diamantes
        diamante = Diamante()
        diamantes.add(diamante)
        #diamante.puntos += 10

generar_diamantes()

# Ingresamos las rocas con una cantidad aleatoria y nos aseguramos que nunca quede en cero con el +4
def generar_rocas():
    for x in range (random.randrange(dificultad)+4):
        roca = Roca()
        rocas.add(roca)
        

generar_rocas()

# Ingresamos al jugador
jugador = Jugador()
sprites.add(jugador)


def nivel():
    pantalla.fill(CELESTE)
    muestra_texto(pantalla, consolas, "Siguiente Nivel...", BLANCO, 50, ANCHO // 2, ALTO // 2)
    

        
        
def pausa():
    time.sleep(4)


# Bucle de juego
ejecutando = True
while ejecutando:
    # Es lo que especifica la velocidad del bucle de juego
    clock.tick(FPS)

    x_relativa = x % fondo.get_rect().width     
    # fondo2 para que el fondo se mueva pero no solo distorsione los pixeles, creamos una x relativa en la que 
    # iremos guardando el resto de pixeles para q el movimieto entre en un bucle '''
    pantalla.blit(fondo,(x_relativa - fondo.get_rect().width,0))
    if x_relativa < ANCHO:
        pantalla.blit(fondo,(x_relativa,0)) 
    #fondo3 para perfeccionar el bucle de movimiento y q no se note q sea un bucle hacemos lo siguiente
    x -= 1 #si esto fuera positivo nos movemos para el otro lado fondo4 para controlar la velocidad del fondo especificamos los FPS maximos en la primer parte del codigo
    
    # Eventos
    for event in pygame.event.get():
        # Se cierra y termina el bucle
        if event.type == pygame.QUIT:
            ejecutando = False

    # Actualización de sprites
    sprites.update()
    rocas.update()
    diamantes.update()


    # Vidas 
    if jugador.vidas == 3:
        vida_1 = pantalla.blit(pygame.transform.scale(jugador.image, (25,25)),(760,25))
        vida_2 = pantalla.blit(pygame.transform.scale(jugador.image, (25,25)),(730,25))
        vida_3 = pantalla.blit(pygame.transform.scale(jugador.image, (25,25)),(700,25))                     
    if jugador.vidas == 2:
        vida_2 = pantalla.blit(pygame.transform.scale(jugador.image, (25,25)),(730,25))
        vida_3 = pantalla.blit(pygame.transform.scale(jugador.image, (25,25)),(700,25))
    if jugador.vidas == 1:
        vida_3 = pantalla.blit(pygame.transform.scale(jugador.image, (25,25)),(700,25))
    if jugador.vidas == 0:
        jugador.kill()
        muestra_texto(pantalla, consolas, "GAME OVER", BLANCO, 50, ANCHO // 2, ALTO // 2)
        
    
    
    # Choque
    choque = pygame.sprite.spritecollide(jugador, rocas, True, pygame.sprite.collide_circle,)
    if jugador.campo == False:
        if choque:
            jugador.vidas -= 1
            

   
    # Captura de diamante
    captura = pygame.sprite.spritecollide(jugador, diamantes, True, pygame.sprite.collide_circle)
    if captura:
        puntuacion += 10
        if puntuacion >= 60:
            nivel()
            generar_diamantes()
            puntuacion = 0
            generar_rocas()
            niveles +=1
            


    # Mostrar texto
    muestra_texto(pantalla, consolas, "Puntuacion: "+str(puntuacion), BLANCO, 15, 700, 15)
    muestra_texto(pantalla, consolas, "Vidas: ", BLANCO, 15, 680, 35)
    muestra_texto(pantalla, consolas, "Nivel: "+ str(niveles), BLANCO, 15, 35, 15)

    # Fondo de pantalla, dibujo de sprites y formas geométricas.
    sprites.draw(pantalla)
    rocas.draw(pantalla)
    diamantes.draw(pantalla)
    # Actualiza el contenido de la pantalla.
    pygame.display.flip()    

pygame.quit()