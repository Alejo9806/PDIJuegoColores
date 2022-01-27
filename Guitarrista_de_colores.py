#--------------------------------------------------------------------------
#------- PLANTILLA DE CÓDIGO POR POLOMBIA ----------------------------------------------
#------- Coceptos básicos de PDI-------------------------------------------
#------- Por: Alejandro Muñoz Acevedo alejandro.munoza@udea.edu.co CC 1037663148 - Manuel Calle Garces manuel.calle@udea.edu.co CC 1036401014--------------
#------- Profesor Facultad de Ingenieria BLQ 21-409  -----------------
#------- enero de 2022--------------------------------------------------
#--------------------------------------------------------------------------

#------- Importación de librerías---------------------------------------------
import cv2
import numpy as np
import random



#------- Inicialización de camara, contadores, variables y umbrales de color---
video = cv2.VideoCapture(0)#Abre la Webcam
marcador= 0 #Marcador de votos ganados 
perdidas= 0#marcador de votos falladas
fondoFinal = cv2.imread('./image/fondo.png') #Variable global para la imagen que se mostrara al final del juego

azul_bajo = np.array ([100,100,20]) #Umbral bajo de color azul
azul_alto=np.array ([125,255,255])#Umbral alto de color azul

verde_bajo = np.array ([36,202,59]) #Umbral bajo de color verde
verde_alto=np.array ([71,255,255])#Umbral alto de color verde

roja_bajo= np.array ([175, 100, 20]) #Umbral bajo de color rojo
roja_alto = np.array([179,255, 255])#Umbral alto de color rojo

#------- Función para identificar colores--------------------------------------
def captura_color(color_bajo, color_alto,color,confirmacion,frame):
    """Esta función captura el video e identifica los colores que esten en el rango [color_bajo, color_alto]"""
    x=0#coordenada que se busca ifentificar con el objeto de color en el video
    if confirmacion==True:#Si se logran leer las capturas de la camara se confirmará
        # El modelo HSV (Hue, Saturation, Brightness – Matiz, Saturación, Brillo), 
        # define un modelo de color en términos de sus componentes. 
        frame_hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV) #convierte de RGB a HSV
        mascara = cv2.inRange(frame_hsv, color_bajo, color_alto) #Crea la mascara dependiendo del rango de colores definido
        mascaraColor = cv2.bitwise_and(frame,frame, mask=mascara) #Crea la mascara dependiendo del rango de colores definido y muestra el color real en el frame
        contorno, _ = cv2.findContours(mascara, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE) # Crea un contorno del objeto del color determinado que se muestra en el video 
        for q in contorno: # Mapea el contorno
            area = cv2.contourArea(q) #Captura y calcula el area
            if area > 3000:
                M = cv2.moments(q)#Obtiene los momentos de la imagen
                if (M["m00"] == 0): M["m00"]=1
                x = int(M["m10"]/M["m00"]) #Obtiene la coordenada en X del centroide
                y = 0 #No se calcula la coordenada en Y del centroide, aunque se utiliza en los pasos siguientes
                cv2.circle(frame, (x,y), 7, (0,255,0), -1) #se obtiene un circulo colo centro en X e Y
                font = cv2.FONT_HERSHEY_SIMPLEX #Fuente del texto que se mostrara en la ventana
                cv2.putText(frame, '{},{}'.format(x,y),(x+10,500), font, 0.75,color,1,cv2.LINE_AA)
                nuevoContorno = cv2.convexHull(q) # Suaviza el contorno que mostraremos en la ventana con el color
                cv2.drawContours(frame, [nuevoContorno], 0, color, 3) #dibuja los nuevos contornos
        
        cv2.imshow('mascaraColor',mascaraColor)#Ventana de detencion de color en su color.
        cv2.imshow('mascara',mascara) #Ventana de detencion de color en blanco y negro.
    return x #Retorna componente en X del centroide del objeto de color definido.




#------- Inicio del juego-----------------------------------------------------
inicio = cv2.imread('./image/FONDOINICIO.jpg') #Carga la imagen de inicio.
cv2.imshow('GUITARRISTA DE COLORES', inicio) #Vizualiza la ventana con la imagen de inicio, en donde el usuario escogera personaje a partir de un color.



#------- Ciclo para detectar objeto azul y mover al personaje-----------------
#Una vez se cierra la imagen de inicio
#Funcion para empezar el juego que recive un personaje 
def juego(personaje):
    i=0 #contador vertical, simula la bajada de u objeto al aumentar en y
    b = random.randint(1,510) #posición aleatoria en x
    marcador=0 #Marcador de votos ganados
    marcador_aux=0 #marcador para resetear
    perdidas=0#marcador de votos falladas
    while True: #Se comienza a jugar con este nuevo ciclo
        #se cargan las imagenes que se van a mostrar en pantalla 
        fondo = cv2.imread('./image/fondo.png') #640x480
        nota_verde = cv2.imread('./image/nota_verde_1.png') #70X32
        fil,col,_= personaje.shape #Se obtienen las dimensiones de la imagen del personaje
        ret, frame=video.read()# lee las capturas de la camara (video) y las muestra   
        frame=cv2.flip(frame,1)#evita el efecto espejo
        x_azul=captura_color(azul_bajo, azul_alto,(255,0,0),ret,frame)#Identifica objeto de color azul y retorna su componente en X
        if x_azul !=0:#Si se logra identificar dicho objeto la componente de X será diferente de 0, entonces continuara lo siguiente
            if x_azul+col<=640: #Identifica que el objeto azul se mantenga dentro de las dimenciones de la ventana de juego
                fondo[318:318+fil, x_azul:x_azul+col] = personaje #cambia parte del fondo por la imagen del personaje dependiendo de donde se ubique el objeto azul
                print(x_verde)#Imprime la coordenada X del objeto azul dependiendo de su ubicacion en la imagen de la camara
                fondo[i:i+32, b:b+70,:] = nota_verde#cambia parte del fondo por la imagen de la nota_verde dependiendo de la aleatoriedad de la variable b
                if i>=318 and i<=350 and b>=x_azul and b<=x_azul+col: #Cuando hay contacto entre la imagen de la del voto y el personaje se hace un punto a favor
                    marcador=marcador+1 #Aumenta el marcador 
                    marcador_aux=marcador #Se necesita para refrescar la imagen del personaje
                    if marcador_aux>0:#Si se aumenta el marcador se debe cargar nuevamente el fondo y la imagen del personaje
                        fondo = cv2.imread('./image/fondo.png') #Se carga la imagen del fondo
                        fondo[318:318+fil, x_azul:x_azul+col] = personaje #cambia parte del fondo por la imagen del personaje dependiendo de donde se ubique el objeto azul
                        #Reincio de marcadores y variables
                        i=0 
                        b = random.randint(1,510) 
                        marcador_aux=0
        
        else:#Si no se logra identificar el objeto quiere decir que está por fuera de la pantalla, se sugiere ubicarlo nuevamente dentro
            fondo = cv2.imread('./image/fondo.png') #Carga la imagen de fondo
            cv2.putText(fondo, 'FAVOR MOSTRAR OBJETO AZUL ', (80, 200),cv2.FONT_HERSHEY_DUPLEX,1,(255,255,255),2)#Escribe sobre la imagen de fondo
            cv2.putText(fondo, 'EN CAMARA, UBICA PARA JUGAR', (80, 250), cv2.FONT_HERSHEY_DUPLEX, 1,(255,255,255),2)  #Escribe sobre la imagen de fondo
        cv2.putText(fondo, 'MARCADOR: '+str(marcador), (530,15),cv2.FONT_HERSHEY_DUPLEX, 0.5,(255,255,255),1) #Escribe y actualiza el marcador de puntos a favor en la imagen de fondo
        cv2.putText(fondo, 'PERDIDAS: '+str(perdidas),(530,30),cv2.FONT_HERSHEY_DUPLEX, 0.5,(255,255,255),1)#Escribe y actualiza el marcador de puntos en contra en la imagen de fondo
        if marcador==10 or perdidas==10: #Cuando de tengan 10 puntos en contra o a favor se termina el juego
            break#Cierra el ciclo
        cv2.imshow('GUITARRISTA DE COLORES', fondo) #Muestra la ventana donde se va a jugar
        cv2.imshow('', frame)   #Muestra la imagen de la camara simultaneamente con la ventana del juego
        key = cv2.waitKey(1) #Condicion para vizualización de las ventanas y cierre de dichas ventanas
        if key==ord('s') or key==ord('S'): #Al presionar la letra S en mayuscula o nimuscula se cerrará el juego
            break 
        i=i+10#Contador vertical para la bajada de la nota_verde
        if i>=420:#Si la imagen del voto baja a mas de 350 en Y no contara como punto a favor, igual si la imagen del voto llega a 420 en Y se confirma el punto en contra
        #Reinicio de contadores    
            i=0
            b = random.randint(1,510) 
        #Aumenta marcador de puntos en contra
            perdidas=perdidas+1
    # video.release() 
    cv2.destroyAllWindows()#Destruye las ventanas
    return marcador, perdidas


#------- Ciclo para detectar color rojo, azul o verde y comenzar a jugar--------------------
while True: #Con el siguiente ciclo se bucará identificar un objeto de color rojo, azul o verde
    ret, frame=video.read() # lee las capturas de la camara (video) y las muestra 
    frame=cv2.flip(frame,1)#evita el efecto espejo
    cv2.imshow('Camara principal', frame) #Vizualiza la ventana con la imagen de la camara
    key2=cv2.waitKey(1)#Condicion para vizualización de la ventana con la imagen de la camara y cierre de dicha ventana
    x_roja=captura_color(roja_bajo, roja_alto,(0,0,255),ret,frame)#Identifica objeto de color rojo y retorna su componente en X
    x_azul=captura_color(azul_bajo, azul_alto,(255,0,0),ret,frame)#Identifica objeto de color azul y retorna su componente en X
    x_verde=captura_color(verde_bajo, verde_alto,(0,255,0),ret,frame)#Identifica objeto de color verde y retorna su componente en X
    if x_roja!=0:#Si se logra identificar un color rojo la componente de X será diferente de 0, entonces se cerrarán las ventanas
        personaje = cv2.imread('./image/personaje.png') #Cargamos la imagen del personaje seleccionado 130x162
        cv2.destroyAllWindows() #Destruye las ventanas
        marcador,perdidas = juego(personaje)#Llamamos la funcion jugar le enviamos el personaje y obtenemos el marcador y las perdidas
        break#Cierra el ciclo
    if x_azul!=0:
        cv2.destroyAllWindows() #Destruye las ventanas
        personaje = cv2.imread('./image/nota_verde_1.png') #Cargamos la imagen del personaje seleccionado 130x162
        marcador,perdidas = juego(personaje) #Llamamos la funcion jugar le enviamos el personaje y obtenemos el marcador y las perdidas
        break#Cierra el ciclo
    if x_verde!=0:
        cv2.destroyAllWindows() #Destruye las ventanas
        personaje = cv2.imread('./image/nota_roja_1.png') #Cargamos la imagen del personaje seleccionado 130x162
        marcador,perdidas = juego(personaje) #Llamamos la funcion jugar le enviamos el personaje y obtenemos el marcador y las perdidas
        break#Cierra el ciclo

    #------- Carga de imagenes y definición de ganar, perder, o retirarse----------
def pantallaFinal(marcador,perdidas):
    fondo =  cv2.imread('./image/fondo.png')#Carga imagen de fondo con dimensiones de 640x480
    ganador = cv2.imread('./image/you_rock.png')   #Carga imagen de ganador con dimensiones de 640x480
    perdedor = cv2.imread('./image/GAME_OVER.png')#Carga imagen de perdedor con dimensiones de 640x480
    retiro=cv2.imread('./image/retiro.png')#Carga imagen de retiro con dimensiones de 640x480
    marcadorFinal = marcador # Llevamos el marcador de votos ganados a una nueva variable
    perdidasFinal = perdidas # LLevamos el marcador de votos perdidos a una nueva variable

    if marcadorFinal==10:#Si se llega a 10 puntos a favor se carga la imagen de ganador y pide mostrar objeto rojo para salir o verde para volver a jugar
        fondo=ganador #Guardamos la imagen nueva de fondo
        cv2.putText(fondo, 'GANASTE',(250,50),cv2.FONT_HERSHEY_DUPLEX, 1, (0,0,0), 2) #Se coloca texto en la encima de la imagen
        cv2.putText(fondo, 'MUESTRA COLOR ROJO PARA SALIR', (80,200),cv2.FONT_HERSHEY_DUPLEX, 0.8, (255,255,255), 3)   #Se coloca texto en la encima de la imagen
        cv2.putText(fondo, 'MUESTRA COLOR VERDE PARA VOLVER A JUGAR',(80,250),cv2.FONT_HERSHEY_DUPLEX, 0.8, (255,255,255), 2)  #Se coloca texto en la encima de la imagen
    elif perdidasFinal==10:#Si se llega a 10 puntos en contra se carga la imagen de perdedor y pide mostrar objeto rojo para salir
        fondo=perdedor #Guardamos la imagen nueva de fondo
        cv2.putText(fondo, 'PERDISTE', (250, 50),cv2.FONT_HERSHEY_DUPLEX, 1, (255,255,255), 2)   #Se coloca texto en la encima de la imagen
        cv2.putText(fondo, 'MUESTRA COLOR ROJO PARA SALIR', (80,200),cv2.FONT_HERSHEY_DUPLEX, 0.8, (255,255,255), 2)  #Se coloca texto en la encima de la imagen
        cv2.putText(fondo, 'MUESTRA COLOR VERDE PARA VOLVER A JUGAR',(80,250),cv2.FONT_HERSHEY_DUPLEX, 0.8, (255,255,255), 2)  #Se coloca texto en la encima de la imagen
    else:#Si se presiona la letra Q se carga la imagen de retiro y pide mostrar objeto rojo para salir
        fondo=retiro #Guardamos la imagen nueva de fondo
        cv2.putText(fondo, 'SALISTE', (400, 100),cv2.FONT_HERSHEY_DUPLEX,1,(255,255,255), 2)  #Se coloca texto en la encima de la imagen
        cv2.putText(fondo, 'MUESTRA COLOR ROJO PARA SALIR',(80,200),cv2.FONT_HERSHEY_DUPLEX, 0.8, (255,255,255), 2) #Se coloca texto en la encima de la imagen
        cv2.putText(fondo, 'MUESTRA COLOR VERDE PARA VOLVER A JUGAR',(80,250),cv2.FONT_HERSHEY_DUPLEX, 0.8, (255,255,255), 2) #Se coloca texto en la encima de la imagen
    return fondo # Retornamos la imagen de fondo

fondoFinal = pantallaFinal(marcador,perdidas) #Llamamos la funcion de pantalla final donde le enviamos el marcador y la perdida, y guardamos en el retorno en una variable

#------- Ciclo para detectar el color rojo o verde  para finalizar o reiniciar el juego------------------
while True:#Se inicia otro ciclo para salir del juego, al igual que al comeinzo se busca un objeto rojo para salir
    ret, frame=video.read() # lee las capturas de la camara (video) y las muestra 
    frame=cv2.flip(frame,1)#evita el efecto espejo
    cv2.imshow('', frame) #Vizualiza la ventana con la imagen de la camara
    cv2.imshow('RESULTADO', fondoFinal)#dependiendo de si gano, perdió o se retiró el usuario se mostrará la imagen respectiva
    key2=cv2.waitKey(1)#Condicion para vizualización de la ventana con la imagen de la camara y cierre de dicha ventana
    x_roja=captura_color(roja_bajo, roja_alto,(0,0,255),ret,frame)#Identifica objeto de color rojo y retorna su componente en X
    x_verde=captura_color(verde_bajo, verde_alto,(255,0,0),ret,frame)#Identifica objeto de color verde y retorna su componente en X
    if x_verde !=0: #Si la componenete en x del color verde es diferente de 0 
        cv2.destroyAllWindows()  #Destruye las ventanas
        marcador,perdidas = juego()  # LLama la funcion de jugar para volver a reiniciar el juego
        fondoFinal = pantallaFinal(marcador,perdidas) # Y llama la funcion de pantalla final para mostrar su resultado
    if x_roja!=0:#Si se logra identificar dicho objeto la componente de X será diferente de 0, entonces se cerrarán las ventanas
        video.release()  #Apaga la camara  
        cv2.destroyAllWindows() #Destruye las ventanas
        break#Cierra el ciclo    

#--------------------------------------------------------------------------
#---------------------------  FIN DEL PROGRAMA ----------------------------
#--------------------------------------------------------------------------
    
    

































