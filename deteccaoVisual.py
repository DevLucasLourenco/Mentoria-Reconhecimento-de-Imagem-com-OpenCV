import os
import cv2
import mediapipe as mp



def tratar_obj_landmark(obj):
    obj_tratado = str(obj).split('\n')
    obj_tratado = [obj_eixo.split(': ') for obj_eixo in obj_tratado][:2]
    return {k:float(v) for k,v in obj_tratado}
    

def DeteccaoMovimento(polegar, indicador):
    
    # retornar função a partir da detecção do gesto
    #------------------------------
    delimitar_gesto:dict = {
        'Pinça' : 'criar função para quando detectado uma pinça',
        'V' : 'Criar função para quando detectado um V',
    }
    #------------------------------
    
    
    eixos_polegar = tratar_obj_landmark(polegar)
    eixos_indicador = tratar_obj_landmark(indicador)
    
    x_polegar, y_polegar = eixos_polegar.values()
    x_indicador, y_indicador = eixos_indicador.values()

    logica_deteccao_movimento:dict = {
        ((y_indicador - y_polegar) > -0.05) and ((y_indicador - y_polegar) < -0.007) : 'Pinça',
        False : 'V',
    }
    
    retorno_objeto_booleano_detectado = [v for k,v in logica_deteccao_movimento.items() if k]
    
    print('polegar:',type(eixos_polegar), eixos_polegar,'\n', sep='\n')
    print('indicador:',type(eixos_indicador), eixos_indicador,'\n', sep='\n')
    
    print(y_indicador - y_polegar)
    print(logica_deteccao_movimento)
    print(retorno_objeto_booleano_detectado)
    
    
    # Analisar e retornar função a partir da detecção do gesto
    #------------------------------
    if retorno_objeto_booleano_detectado:
        print(delimitar_gesto.get(retorno_objeto_booleano_detectado[0]))
    #------------------------------
    
    
# Vincular Webcam
#------------------------------
webcam = cv2.VideoCapture(0) # Cria coneção com a webcam default

# Inicializando mediapipe
#------------------------------
RECONHECIMENTO_HANDS = mp.solutions.hands
HAND = RECONHECIMENTO_HANDS.Hands()
#------------------------------
DESENHO_MP = mp.solutions.drawing_utils
#------------------------------

if webcam.isOpened():
    validacao, frameBGR = webcam.read()
    
    while validacao:
        validacao, frameBGR = webcam.read() # Retorna os frames na ordem invertado do rgb, em bgr (de trás pra frente)
        
        frameRGB = cv2.cvtColor(frameBGR, cv2.COLOR_BGR2RGB)
        hand_list = HAND.process(frameRGB) #identifica as mãos
        
        #------------------------------ Para cada mão identificada, mostrar os pontilhamentos
        if hand_list.multi_hand_landmarks:  
            for hand in hand_list.multi_hand_landmarks:
                os.system('cls')
                
                ponta_dedo_polegar = hand.landmark[4]
                ponta_dedo_indicador = hand.landmark[8]
                ponta_dedo_medio = hand.landmark[12]
                ponta_dedo_anelar = hand.landmark[16]
                ponta_dedo_mindinho = hand.landmark[20]
                
                DeteccaoMovimento(ponta_dedo_polegar, ponta_dedo_indicador)
                
                
                # print(hand.landmark)
                DESENHO_MP.draw_landmarks(frameBGR, hand, RECONHECIMENTO_HANDS.HAND_CONNECTIONS)
        #------------------------------
        
        
        # Mostrar frames da webcam
        cv2.imshow('Webcam - LL', frameBGR)
        
        
        # Tempo de espera entre os frames e detecção de tecla de encerramento
        #--------------------
        tecla = cv2.waitKey(2) # Tempo de espera em milissegundo  | 60s -> 2 -> 30fps | 1 -> 60fps
        if tecla == 27: # ESC em ASCII -> 27
            break
        #--------------------



webcam.release()
cv2.destroyAllWindows()
#------------------------------