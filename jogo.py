import cv2
import numpy as np

#Função que escreve o texto
def escreve_texto(img, text, origem, color):
    font = cv2.FONT_HERSHEY_COMPLEX
    cv2.putText(img, text, origem, font, 1, color, 2, cv2.LINE_AA)

#Função que faz o filtro gray e blur, retornando o thresh
def gray_blur(crop_img):
    gray = cv2.cvtColor(crop_img, cv2.COLOR_BGR2GRAY)

    k_size = (35, 35)
    filtro_blur = cv2.GaussianBlur(gray, k_size, 0)

    _, thresh = cv2.threshold(filtro_blur, 127, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

    return thresh

#Função que retorna a area do objeto encontrado
def area(contours):
    max_area = -1    
    for i in range(len(contours)):
            area = cv2.contourArea(contours[i])
            if area > max_area:
                aux = contours[i]
                max_area = area
    
    cnt = aux

    M = cv2.moments(cnt)

    if M["m00"] != 0:
        cx = int(M['m10']/M['m00'])
        cy = int(M['m01']/M['m00'])
    else: 
        M["m00"] == 0.1
        cx = int(M['m10']/M['m00'])
        cy = int(M['m01']/M['m00'])

    return max_area

#Função de findContours
def contornos(thresh):
    contours, _ = cv2.findContours(thresh.copy(), \
        cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    return contours

#Função que define o que foi jodgado (PEDRA, PAPEL e TESOURA)
def jogada(max_area, x):
    if max_area > 14500 and max_area < 17000:
        txt = "PAPEL"
        escreve_texto(img, txt, (x, 120), (0, 255, 0))
    elif max_area > 11500 and max_area < 14000:
        txt = "PEDRA"
        escreve_texto(img, txt, (x, 120), (0, 255, 0))
    elif max_area < 11500 and max_area > 6000:
        txt = "TESOURA"
        escreve_texto(img, txt, (x, 120), (0, 255, 0))
    else:
        escreve_texto(img, "", (x, 120), (0, 255, 0))

    return txt

esq = 0
dir = 0
cont = 0
    
vc = cv2.VideoCapture("pedra-papel-tesoura.mp4")

while vc.isOpened():
    ret, img = vc.read()

    if img is None:
       cv2.destroyWindow('Pedra Papel e Tesoura')
       vc.release()   
    else:
        img = cv2.resize(img, (800, 600))

        #Faz o corte do video para analise
        crop_img = img[100:600, 100:450]
        crop_img1 = img[100:600, 350:800]

        #Filtro de Threshold
        thresh = gray_blur(crop_img)
        thresh1 = gray_blur(crop_img1)

        #FindContours
        contours = contornos(thresh)
        contours1 = contornos(thresh1)

        #Define as max_area e max_area1
        max_area = area(contours)
        max_area1 = area(contours1)

        #Define o que foi jogado por cada jogador (PEDRA, PAPEL e TESOURA)
        txt = jogada(max_area, 100)
        txt1 = jogada(max_area1, 500)
        
        #Define que lado ganha
        if (txt == "PEDRA" and txt1 == "TESOURA") or (txt == "TESOURA" and txt1 == "PAPEL" ) or (txt == "PAPEL" and txt1 == "PEDRA"):
            escreve_texto(img, "Jogador da esquerda venceu", (150, 40), (0, 0, 255))

        elif (txt == "TESOURA" and txt1 == "PEDRA") or (txt == "PAPEL" and txt1 == "TESOURA") or (txt == "PEDRA" and txt1 == "PAPEL"):
            escreve_texto(img, "Jogador da direita venceu", (150, 40), (0, 0, 255))

        else:
            escreve_texto(img, "Empate", (320, 40), (0, 0, 255))

        cont += 1
        if cont >= 90:
            cont = 0

            #Define quem pontua
            if (txt == "PEDRA" and txt1 == "TESOURA") or (txt == "TESOURA" and txt1 == "PAPEL" ) or (txt == "PAPEL" and txt1 == "PEDRA"):
                esq += 1

            elif (txt == "TESOURA" and txt1 == "PEDRA") or (txt == "PAPEL" and txt1 == "TESOURA") or (txt == "PEDRA" and txt1 == "PAPEL"):
                dir += 1

            else:
                escreve_texto(img, "Empate", (320, 40), (0, 0, 255))

        #Placar  
        texto = f"Esquerda: {esq} X Direita: {dir}"
        escreve_texto(img, texto, (150, 70), (0, 0, 255))         

        # Mostra a janela processada
        cv2.imshow('Pedra Papel e Tesoura', img)
        
        k = cv2.waitKey(10)
        if k == 27:
            break
    