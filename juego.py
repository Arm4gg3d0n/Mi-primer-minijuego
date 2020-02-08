#Empezamos importando el módulo de pygame
import pygame
#Importamos módulos adicionales de nivel superior
from pygame.locals import *
#Módulo que permite generar números aleatorios entre otras funciones
import random

#Inicializa todos lo módulos de pygame,devueve excepciones si algún módulo falla
pygame.init()
#Determinamos dimensiones y título de la pantalla, con el módulo display, al igual que la cantidad de pelotas
ancho,alto=800,600
cantidadPelotas=3 
pantalla=pygame.display.set_mode((ancho,alto))
pygame.display.set_caption("Pelota Rebota")
#Carga imagen con el módulo image
icono=pygame.image.load("Imagenes/pelota_1.jpg")
#Determinamos ícono de la pantalla con el módulo display
pygame.display.set_icon(icono)

#Función que permite la pulsación sostenida de una tecla
#al principio da un tiempo de espera de un mseg y después cada 25 mseg se repetirá el evento de teclado correspondiente
pygame.key.set_repeat(1,25)
#Se crea un objeto que permite medir y gestionar el tiempo
reloj=pygame.time.Clock()
imagenRaqueta=pygame.image.load("Imagenes/raqueta.png")
#Se crea un rectángulo que conserva altura y anchura(por defecto en (0,0))que la contiene
#Puede tener parámetros: imagen.get_rect(center=(a,b))
rectanguloRaqueta=imagenRaqueta.get_rect()

#Creamos diccionarios que van a contener a las pelotas y sus componentes de velocidad
imagenPelota=pygame.image.load("Imagenes/pelota.png")
rectangulosPelotas={}
velocidadesX={}
velocidadesY={}

 
imagenPresent=pygame.image.load("Imagenes/portada.png")
rectanguloPresent=imagenPresent.get_rect()
rectanguloPresent.top=0
rectanguloPresent.left=0


#Se crea un objeto de fuente tipográfica con el submódulo Sysfont, en este caso Bembo de tamaño 60 y 40
letra60=pygame.font.SysFont("Bembo",60)
letra40=pygame.font.SysFont("Bembo",40)
#la función render() traza un texto en una supercie recibe los atributos de texto,antialias/bordes suavizados(booleano),color de la letra, color de fondo
imagenTextoPresent=letra60.render("Pulsa Espacio para jugar",True,(0,255,0))
imagenTitulo=letra60.render("Pelota Rebota",True,(0,255,0))

rectanguloTextoPresent=imagenTextoPresent.get_rect()
rectanguloTitulo=imagenTitulo.get_rect()
#Usamos el atributo centerx para alinear el texto en el centro del eje horizontal con respecto a la pantalla
rectanguloTextoPresent.centerx=pantalla.get_rect().centerx
#Usamos el atributo centery para alinear el texto en el centro del eje vertical y bajarlo 20 pixeles
rectanguloTextoPresent.centery=pantalla.get_rect().centery-20
rectanguloTitulo.centerx=pantalla.get_rect().centerx
rectanguloTitulo.centery=60

imagenFondo=pygame.image.load("Imagenes/cancha.png")
rectanguloFondo=imagenFondo.get_rect()

sonidoRebote=pygame.mixer.Sound("Sonido/rebote.wav")

#Establecemos valor booleano para el estado de la partida
partidaEnMarcha=True

#Establecemos un bucle que se mantendrá hasta que la partida se detenga
while partidaEnMarcha:
    
 
    # ---- Presentación ----
    pantalla.fill((0,255,0))
    #Trazamos las imagenes sobre la pantalla con el módulo blit
    pantalla.blit(imagenPresent,rectanguloPresent)
    pantalla.blit(imagenTextoPresent,rectanguloTextoPresent)
    pantalla.blit(imagenTitulo,rectanguloTitulo)
    #El submódulo flip actualiza la pantalla, para que nuestra portada aparezca cuando debe
    pygame.display.flip() 
 
    entrarAlJuego=False
    while not entrarAlJuego:
        #el submódulo wait pausa el programa por una cantidad dada de milisegundos
        #Relentiza el compartir el procesador con otros programas
        #Un programa que se detiene incluso por unos pocos mseg va a consumir muy poco tiempo de procesador
        #Es menos preciso que la función pygame.time.delay()
        pygame.time.wait(100)
        for event in pygame.event.get(KEYUP):
            if event.key==K_SPACE:
                entrarAlJuego=True
 
    # ---- Comienzo de una partida de juego ----
    #Variable que almacenará el puntaje obtenido
    puntos=0                            
    rectanguloRaqueta.left=ancho/2
    rectanguloRaqueta.top=alto-50

    
    for i in range(cantidadPelotas):
        #Asignación de clave numérica para la imagen de una pelota dentro del diccionario
        rectangulosPelotas[i]=imagenPelota.get_rect()
        #Un valor aleatorio entre 50 y 750 se asigna como distancia entre el lado izquierdo de la pantalla y la pelota
        rectangulosPelotas[i].left=random.randrange(50,751)
        #Un valor aleatorio entre 10 y 301 se asigna como distancia entre el lado superior de la pantalla y la pelota
        rectangulosPelotas[i].top=random.randrange(10,301)
        #A unas claves numéricas se les asigna los componentes del vector velocidad
        velocidadesX[i]=5
        velocidadesY[i]=5
 
    terminado=False
 
    while not terminado:
        # ---- Comprobar acciones del usuario ----
        #El bucle evalua cola de eventos
        for event in pygame.event.get():
            #Evalua el tipo de evento, en este caso particular si hay un cierre por salida de pantalla, para terminar el programa
            if event.type==pygame.QUIT: 
                terminado=True
                partidaEnMarcha=False
                
        #Obtener el estado de todas las teclas, retorna una secuencia de valores booleanos que representan el estado de las teclas
        keys = pygame.key.get_pressed()
        #Podemos comprobar cualquier tecla en concreto
        #Al pulsar las teclas de dirección, la raqueta cambia su posición
        if keys[K_LEFT]:
            rectanguloRaqueta.left-=8
        if keys[K_RIGHT]:
            rectanguloRaqueta.left+=8
        if keys[K_DOWN]:
            rectanguloRaqueta.top+=8
        if keys[K_UP]:
            rectanguloRaqueta.top-=8
            
        # ---- Actualizar estado ----
        for i in range(cantidadPelotas):
            #En cada fotograma se desplaza la imagen por vía de la velocidad dada, estamos hablando de un cambio de posición justamente
            rectangulosPelotas[i].left+=velocidadesX[i]
            rectangulosPelotas[i].top+=velocidadesY[i]
            #Debemos cambiar la dirección del vector velocidad cada vez que se llegue al borde de la pantalla generando un efecto de rebote y evitando una caida al "vacío"
            if rectangulosPelotas[i].left<0 or rectangulosPelotas[i].right>ancho:
                velocidadesX[i]=-velocidadesX[i]
                sonidoRebote.play()
            if rectangulosPelotas[i].top<=0:
                velocidadesY[i]=-velocidadesY[i]
                sonidoRebote.play()
                
        
        # ---- Comprobar colisiones ----
        for i in range(cantidadPelotas):
            #Método que evalua si dos rectangulos colisionan
            if rectanguloRaqueta.colliderect(rectangulosPelotas[i]):            
                sonidoRebote.play()
                puntos+=1               
                velocidadesY[i]=-velocidadesY[i]-1
            
            #Si una pelota toca el "suelo" damos la partida por terminada    
            if rectangulosPelotas[i].bottom>alto:
                terminado=True               
 
        # ---- Dibujar elementos en pantalla ----
        pantalla.fill((255,255,255))
        pantalla.blit(imagenFondo,rectanguloFondo)
        
        for i in range(cantidadPelotas):
            pantalla.blit(imagenPelota,rectangulosPelotas[i])               
        pantalla.blit(imagenRaqueta,rectanguloRaqueta)
        #Creamos un objeto de funte tipográfica para el aviso de puntos
        imagenPuntos=letra40.render(f"Puntos: {puntos}",True,(0,255,0),(0,0,0))
        #Obtenemos superficie rectangular de los puntos
        rectanguloPuntos=imagenPuntos.get_rect()
        #Ubicamos nuestro aviso de puntaje
        rectanguloPuntos.left=10                           
        rectanguloPuntos.top=10
        #Mostramos en pantalla el aviso de puntaje
        pantalla.blit(imagenPuntos,rectanguloPuntos)        
        
        pygame.display.flip()
 
        #Ralentizar hasta 40 fotogramas por segundo hace que las velocidades de los elementos no sean desproporcionadas
        reloj.tick(40)
    
    
 
# ---- Final de partida ----
#Detiene todos los módulos previamente inicializados, esto no implica salir del programa
#Es necesario sobre todo cuando se requiere detener recursos del programa para luego continuar
pygame.quit()
