import mediapipe as mp
import math
import cv2 # opencv-python
import os


class DeteccaoVisual:
    # Reconhecimentos e exibição
    #------------------------------
    RECONHECIMENTO_HANDS = mp.solutions.hands
    HAND = RECONHECIMENTO_HANDS.Hands()
    #------------------------------
    DESENHO_MP = mp.solutions.drawing_utils
    #------------------------------
    
    def __init__(self, exibir_webcam:bool=True):
        self.exibir_webcam = exibir_webcam
        self.webcam = cv2.VideoCapture(0)
        self.frameBGR:object = None
        self.frameRGB:object = None
    
    
    def __del__(self):
        self.webcam.release()
        cv2.destroyAllWindows()
    
        
    def run(self):
        if self.webcam.isOpened():
            obj_validador, self.frameBRG = self.webcam.read()
            
            while obj_validador:
                obj_validador, self.frameBGR = self.webcam.read()
                
                # Tratativa de frames de BGR para RGB e identificação das mãos.
                #------------------------------------------------------------
                self.frameRGB = cv2.cvtColor(self.frameBGR, cv2.COLOR_BGR2RGB)
                lista_ObjMaos = DeteccaoVisual.HAND.process(self.frameRGB) 
                #------------------------------------------------------------
            
                if lista_ObjMaos.multi_hand_landmarks:
                    for obj_Mao in lista_ObjMaos.multi_hand_landmarks:
                        os.system('cls')
                        
                        inicio_dedo_polegar = obj_Mao.landmark[1]
                        inicio_dedo_indicador = obj_Mao.landmark[5]
                        inicio_dedo_medio = obj_Mao.landmark[9]
                        
                        ponta_dedo_polegar = obj_Mao.landmark[4]
                        ponta_dedo_indicador = obj_Mao.landmark[8]
                        ponta_dedo_medio = obj_Mao.landmark[12]
                        ponta_dedo_anelar = obj_Mao.landmark[16]
                        ponta_dedo_mindinho = obj_Mao.landmark[20]
                        
                        deteccao_gesto = DeterminarGestos(IDP=inicio_dedo_polegar, IDI=inicio_dedo_indicador, IDM=inicio_dedo_medio, PDP=ponta_dedo_polegar, PDI=ponta_dedo_indicador, PDM=ponta_dedo_medio, PDA=ponta_dedo_anelar, PDMI=ponta_dedo_mindinho)
                        deteccao_gesto.identificar()
                        
                        DeteccaoVisual.DESENHO_MP.draw_landmarks(self.frameBGR, obj_Mao, DeteccaoVisual.RECONHECIMENTO_HANDS.HAND_CONNECTIONS)

                if self.exibir_webcam:
                    cv2.imshow('Webcam - Deteccao Visual', self.frameBGR)
                                
                # Tempo de espera entre os frames e detecção de tecla de encerramento
                #--------------------
                tecla = cv2.waitKey(2) # Tempo de espera em milissegundo  | 2 -> 30fps | 1 -> 60fps
                if tecla == 27: # ESC em ASCII -> 27
                    break
                #--------------------



class DeterminarGestos:
    
    def __init__(self,IDP, IDI, IDM, PDP, PDI, PDM, PDA, PDMI) -> None:
        # Eixos -> {x:y}
        #----------------------------------------------------------------------
        self.eixo_inicio_polegar:dict = self._tratar_obj_landmark(IDP)
        self.eixo_inicio_indicador:dict = self._tratar_obj_landmark(IDI)
        self.eixo_inicio_medio:dict = self._tratar_obj_landmark(IDM)
        
        #-----

        self.eixo_ponta_polegar:dict = self._tratar_obj_landmark(PDP)
        self.eixo_ponta_indicador:dict = self._tratar_obj_landmark(PDI)
        self.eixo_ponta_medio:dict = self._tratar_obj_landmark(PDM)
        self.eixo_ponta_anelar:dict = self._tratar_obj_landmark(PDA)
        self.eixo_ponta_mindinho:dict = self._tratar_obj_landmark(PDMI)
        #----------------------------------------------------------------------
        
        # Unpacking de X e Y dos Eixos
        #----------------------------------------------------------------------
        self.X_inicio_polegar, self.Y_inicio_polegar = self.eixo_inicio_polegar.values()
        self.X_inicio_indicador, self.Y_inicio_indicador = self.eixo_inicio_indicador.values()
        self.X_inicio_medio, self.Y_inicio_medio = self.eixo_inicio_medio.values()
        
        #-----
        
        self.X_ponta_polegar, self.Y_ponta_polegar = self.eixo_ponta_polegar.values()
        self.X_ponta_indicador, self.Y_ponta_indicador = self.eixo_ponta_indicador.values()
        self.X_ponta_medio, self.Y_ponta_medio = self.eixo_ponta_medio.values()
        self.X_ponta_anelar, self.Y_ponta_anelar = self.eixo_ponta_anelar.values()
        self.X_ponta_mindinho, self.Y_ponta_mindinho = self.eixo_ponta_mindinho.values()
        #----------------------------------------------------------------------
        
        # Dict's Auxiliares
        #------------------------------
        self.delimitar_gesto_funcao:dict = {
            'Pinça' : 'print("Pinça")',
            'L' : 'função L',
            'V' : 'função V',
            'II' : 'função II',
            }
        
        #-----
        
        self.logica_deteccao_movimento:dict = {
            ((self.Y_ponta_indicador - self.Y_ponta_polegar) > -0.05) and ((self.Y_ponta_indicador - self.Y_ponta_polegar) < -0.007) and ((self.Y_ponta_medio*1.50) < self.Y_ponta_indicador) : 'Pinça',
            (False) : 'L',
            }
        #------------------------------
        
        # Cálculo para Testes 
        #------------------------------
        print(f'Polegar - Ponta: {self.eixo_ponta_polegar} - Inicio: {self.eixo_inicio_polegar} \n',
              f'Indicador - Ponta: {self.eixo_ponta_indicador} - Inicio: {self.eixo_inicio_indicador} \n',
              f'Médio - Ponta: {self.eixo_ponta_medio} - Inicio: {self.eixo_inicio_medio} \n',
              f'Anelar - Ponta: {self.eixo_ponta_anelar}\n',
              f'Mindinho - Ponta: {self.eixo_ponta_mindinho}\n')


        print('inicio e fim polegar: ', (self.X_ponta_polegar - self.X_inicio_polegar), ((self.X_ponta_polegar - self.X_inicio_polegar)  <= 0.2) and ((self.X_ponta_polegar - self.X_inicio_polegar) >= 0.125))
        print('hipotenusa: ',math.sqrt((self.Y_ponta_indicador**2)+(self.Y_ponta_polegar**2)))
        #------------------------------

    
    def _tratar_obj_landmark(self, obj):
        obj_tratado = str(obj).split('\n')
        obj_tratado = [obj_eixo.split(': ') for obj_eixo in obj_tratado][:2]
        return {k:float(f'{float(v):.5f}') for k,v in obj_tratado}
    
    
    def identificar(self):
        retorno_objeto_booleano_detectado = [v for k,v in self.logica_deteccao_movimento.items() if k]
        
        print(self.logica_deteccao_movimento)
        print(retorno_objeto_booleano_detectado)
        
        if retorno_objeto_booleano_detectado:
            eval(self.delimitar_gesto_funcao.get(retorno_objeto_booleano_detectado[0]))
            
            
if __name__ == "__main__":
    def abrir_explorador_de_arquivos():
        os.system('start explorer')
    
    app = DeteccaoVisual(exibir_webcam=True)
    app.run()