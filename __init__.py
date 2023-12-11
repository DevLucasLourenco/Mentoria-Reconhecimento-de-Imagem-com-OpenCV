import os
import cv2
import mediapipe as mp


class DeteccaoVisual:
    # Rec's
    #------------------------------
    RECONHECIMENTO_HANDS = mp.solutions.hands
    HAND = RECONHECIMENTO_HANDS.Hands()
    DESENHO_MP = mp.solutions.drawing_utils
    #------------------------------
    
    def __init__(self):
        self.webcam = cv2.VideoCapture(0)
        self.frameBGR:object = None
        self.frameRGB:object = None
    
    
    def __del__(self):
        self.webcam.release()
        cv2.destroyAllWindows()
        print('end')
    
        
    def run(self):
        if self.webcam.isOpened():
            obj_validador, self.frameBRG = self.webcam.read()
            
            while obj_validador:
                obj_validador, self.frameBGR = self.webcam.read()
                
                # Identificar as mãos e tratar os frames de BGR para RGB.
                #------------------------------------------------------------
                self.frameRGB = cv2.cvtColor(self.frameBGR, cv2.COLOR_BGR2RGB)
                lista_ObjMaos = DeteccaoVisual.HAND.process(self.frameRGB) 
                #------------------------------------------------------------
            
                if lista_ObjMaos.multi_hand_landmarks:
                    for obj_Mao in lista_ObjMaos.multi_hand_landmarks:
                        os.system('cls')
                        
                        ponta_dedo_polegar = obj_Mao.landmark[4]
                        ponta_dedo_indicador = obj_Mao.landmark[8]
                        ponta_dedo_medio = obj_Mao.landmark[12]
                        ponta_dedo_anelar = obj_Mao.landmark[16]
                        ponta_dedo_mindinho = obj_Mao.landmark[20]
                        
                        _DeterminarGestos(PDP=ponta_dedo_polegar, PDI=ponta_dedo_indicador, PDM=ponta_dedo_medio, PDA=ponta_dedo_anelar, PDMI=ponta_dedo_mindinho)
                        
                        DeteccaoVisual.DESENHO_MP.draw_landmarks(self.frameBGR, obj_Mao, DeteccaoVisual.RECONHECIMENTO_HANDS.HAND_CONNECTIONS)

                # Mostrar frames da webcam
                cv2.imshow('Webcam - Detecção Visual', self.frameBGR)
                                
                # Tempo de espera entre os frames e detecção de tecla de encerramento
                #--------------------
                tecla = cv2.waitKey(2) # Tempo de espera em milissegundo  | 2 -> 30fps | 1 -> 60fps
                if tecla == 27: # ESC em ASCII -> 27
                    break
                #--------------------


class _DeterminarGestos:
    
    
    def __init__(self, PDP, PDI, PDM, PDA, PDMI) -> None:
        # Eixos -> {x:y}
        #----------------------------------------------------------------------
        print(PDP)
        self.eixo_ponta_polegar:dict = self._tratar_obj_landmark(PDP)
        self.eixo_ponta_indicador:dict = self._tratar_obj_landmark(PDI)
        self.eixo_ponta_medio:dict = self._tratar_obj_landmark(PDM)
        self.eixo_ponta_anelar:dict = self._tratar_obj_landmark(PDA)
        self.eixo_ponta_mindinho:dict = self._tratar_obj_landmark(PDMI)
        #----------------------------------------------------------------------
        
        # X e Y dos Eixos
        #----------------------------------------------------------------------
        self.X_ponta_polegar, self.Y_ponta_polegar = self.eixo_ponta_polegar.values()
        self.X_ponta_indicador, self.Y_ponta_indicador = self.eixo_ponta_indicador.values()
        self.X_ponta_medio, self.Y_ponta_medio = self.eixo_ponta_medio.values()
        self.X_ponta_anelar, self.Y_ponta_anelar = self.eixo_ponta_anelar.values()
        self.X_ponta_mindinho, self.Y_ponta_mindinho = self.eixo_ponta_mindinho.values()
        #----------------------------------------------------------------------
        
        # Dict's Auxiliares
        #------------------------------
        self.delimitar_gesto_funcao:dict = {
            'Pinça' : 'função pinça',
            'V' : 'função V',
            "II" : 'função II',
            }
        
        #----- 
        
        self.logica_deteccao_movimento:dict = {
            ((self.Y_ponta_indicador - self.Y_ponta_polegar) > -0.05) and ((self.Y_ponta_indicador - self.Y_ponta_polegar) < -0.007) : 'Pinça',
            False : 'V',
            }
        #------------------------------
    
        
    def _tratar_obj_landmark(self, obj):
        obj_tratado = str(obj).split('\n')
        obj_tratado = [obj_eixo.split(': ') for obj_eixo in obj_tratado][:2]
        return {k:float(v) for k,v in obj_tratado}
    
    
    # def 


if __name__ == "__main__":
    
    def abrir_explorador_de_arquivos():
        os.system('start explorer')
    
    app = DeteccaoVisual()
    app.run()
    