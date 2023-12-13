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
                        inicio_dedo_anelar = obj_Mao.landmark[13]
                        inicio_dedo_minimo = obj_Mao.landmark[17]
                        
                        ponta_dedo_polegar = obj_Mao.landmark[4]
                        ponta_dedo_indicador = obj_Mao.landmark[8]
                        ponta_dedo_medio = obj_Mao.landmark[12]
                        ponta_dedo_anelar = obj_Mao.landmark[16]
                        ponta_dedo_minimo = obj_Mao.landmark[20]
                        
                        deteccao_gesto = DeterminarGestos(IDP=inicio_dedo_polegar, IDI=inicio_dedo_indicador, IDM=inicio_dedo_medio,
                                                          IDA=inicio_dedo_anelar, IDMI=inicio_dedo_minimo, PDP=ponta_dedo_polegar, 
                                                          PDI=ponta_dedo_indicador, PDM=ponta_dedo_medio, PDA=ponta_dedo_anelar, 
                                                          PDMI=ponta_dedo_minimo)
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
    
    def __init__(self,IDP, IDI, IDM, IDA, IDMI, PDP, PDI, PDM, PDA, PDMI) -> None:        
        # Eixos -> {x:y}
        #----------------------------------------------------------------------
        self.eixo_inicio_polegar:dict = self._tratar_obj_landmark(IDP)
        self.eixo_inicio_indicador:dict = self._tratar_obj_landmark(IDI)
        self.eixo_inicio_medio:dict = self._tratar_obj_landmark(IDM)
        self.eixo_inicio_anelar:dict = self._tratar_obj_landmark(IDA)
        self.eixo_inicio_minimo:dict = self._tratar_obj_landmark(IDMI)
        
        #-----

        self.eixo_ponta_polegar:dict = self._tratar_obj_landmark(PDP)
        self.eixo_ponta_indicador:dict = self._tratar_obj_landmark(PDI)
        self.eixo_ponta_medio:dict = self._tratar_obj_landmark(PDM)
        self.eixo_ponta_anelar:dict = self._tratar_obj_landmark(PDA)
        self.eixo_ponta_minimo:dict = self._tratar_obj_landmark(PDMI)
        #----------------------------------------------------------------------
        
        # Unpacking de X e Y dos Eixos
        #----------------------------------------------------------------------
        self.X_inicio_polegar, self.Y_inicio_polegar = self.eixo_inicio_polegar.values()
        self.X_inicio_indicador, self.Y_inicio_indicador = self.eixo_inicio_indicador.values()
        self.X_inicio_medio, self.Y_inicio_medio = self.eixo_inicio_medio.values()
        self.X_inicio_anelar, self.Y_inicio_anelar = self.eixo_inicio_anelar.values()
        self.X_inicio_minimo, self.Y_inicio_minimo = self.eixo_inicio_minimo.values()
        
        #-----
        
        self.X_ponta_polegar, self.Y_ponta_polegar = self.eixo_ponta_polegar.values()
        self.X_ponta_indicador, self.Y_ponta_indicador = self.eixo_ponta_indicador.values()
        self.X_ponta_medio, self.Y_ponta_medio = self.eixo_ponta_medio.values()
        self.X_ponta_anelar, self.Y_ponta_anelar = self.eixo_ponta_anelar.values()
        self.X_ponta_minimo, self.Y_ponta_minimo = self.eixo_ponta_minimo.values()
        #----------------------------------------------------------------------
        
        # Dict's Auxiliares
        #------------------------------
        self.delimitar_gesto_funcao:dict = {
            'Pinça' : 'print("Retorno de Pinça")',
            'L' : 'print("Retorno de L")',
            'V' : 'função V',
            'II' : 'função II',
            }
        
        #-----
        
        self.logica_deteccao_movimento:dict = {
            Gestos.Pinca(self) : 'Pinça',
            Gestos.L(self) : 'L',
            }
        #------------------------------
        
        # Cálculo para Testes 
        #------------------------------
        
        print(type(self.eixo_inicio_indicador))
        print(type(self.X_inicio_indicador))
        print(f'Polegar - Inicio: {self.eixo_inicio_polegar} - Ponta: {self.eixo_ponta_polegar}\n',
              f'Indicador - Inicio: {self.eixo_inicio_indicador} - Ponta: {self.eixo_ponta_indicador}\n',
              f'Médio - Inicio: {self.eixo_inicio_medio} - Ponta: {self.eixo_ponta_medio}\n',
              f'Anelar - Inicio: {self.eixo_inicio_anelar} - Ponta: {self.eixo_ponta_anelar}\n',
              f'Minimo - Inicio: {self.eixo_inicio_minimo} - Ponta: {self.eixo_ponta_minimo}\n',
        )


        
        print('Reta do polegar: ', (self.X_ponta_polegar - self.X_inicio_polegar), (((self.X_ponta_polegar - self.X_inicio_polegar)  <= 0.2) or ((self.X_ponta_polegar - self.X_inicio_polegar)  <= -0.2)) and (((self.X_ponta_polegar - self.X_inicio_polegar) >= 0.125) or (self.X_ponta_polegar - self.X_inicio_polegar) <= -0.125))
        hipotenusa = math.sqrt((self.Y_ponta_indicador**2)+(self.X_ponta_polegar**2))
        print('Hipotenusa: ', hipotenusa, (hipotenusa >= 0.4) and (hipotenusa <= 0.73))
        #------------------------------
        


    def _tratar_obj_landmark(self, obj):
        obj_tratado = str(obj).split('\n')
        obj_tratado = [obj_eixo.split(': ') for obj_eixo in obj_tratado][:2]
        return {k:float(v) for k,v in obj_tratado}
    
    
    def identificar(self):
        retorno_objeto_booleano_detectado = [v for k,v in self.logica_deteccao_movimento.items() if k]
        
        print(self.logica_deteccao_movimento)
        print(retorno_objeto_booleano_detectado)
        
        if retorno_objeto_booleano_detectado:
            eval(self.delimitar_gesto_funcao.get(retorno_objeto_booleano_detectado[0]))          

            
            
class Gestos:
    
        def Pinca(objeto_self_classe):
            #----------------------------------------
            diferenca_eixoY_PDP = (objeto_self_classe.Y_ponta_indicador - objeto_self_classe.Y_ponta_polegar)
            #----------------------------------------
            
            # Validações de Prosseguimento
            #----------------------------------------
            validacao1:bool = (diferenca_eixoY_PDP > -0.05)
            validacao2:bool = (diferenca_eixoY_PDP < -0.007)
            validacao3:bool = ((objeto_self_classe.Y_ponta_medio*1.30) < objeto_self_classe.Y_ponta_indicador)
            #----------------------------------------
            
            if validacao1 and validacao2 and validacao3:
                return True

            
        def L(objeto_self_classe):
            #----------------------------------------
            hipotenusa = math.sqrt((objeto_self_classe.Y_ponta_indicador**2)+(objeto_self_classe.X_ponta_polegar**2))
            dif_reta_polegar = (objeto_self_classe.X_ponta_polegar - objeto_self_classe.X_inicio_polegar)
            dif_proximidade_inicio_indicador_medio = (objeto_self_classe.X_ponta_indicador - objeto_self_classe.X_ponta_medio)
            #----------------------------------------
            
            # Validações de Prosseguimento
            #----------------------------------------
            validacao_reta_polegar = (((dif_reta_polegar)  <= 0.2) or ((dif_reta_polegar)  <= -0.2)) and (((dif_reta_polegar) >= 0.125) or (dif_reta_polegar) <= -0.125)
            validacao_delimitacao_hipotenusa = (hipotenusa >= 0.4) and (hipotenusa <= 0.73)
            validacao_proximidade_inicio_indicador_medio = ((dif_proximidade_inicio_indicador_medio >= 0.015) and (dif_proximidade_inicio_indicador_medio <= 0.023)) or ((((dif_proximidade_inicio_indicador_medio <= 0.015) and (dif_proximidade_inicio_indicador_medio >= 0)) and ((dif_proximidade_inicio_indicador_medio >= -0.023) and (dif_proximidade_inicio_indicador_medio <= 0 ))))
            
            # Criar validação da proximidade dos dedos indicadores e médio
            print(validacao_proximidade_inicio_indicador_medio, dif_proximidade_inicio_indicador_medio)
            
            # Criar validação de o dedo médio e o dedo mínimo estarem abaixados
            
            #----------------------------------------
            
            if validacao_reta_polegar and validacao_delimitacao_hipotenusa:
                return True
        
            
        def V(objeto_self_classe):
            ...
        
        def II(objeto_self_classe):
            #polegar abaixo do dedo indicador
            ...
            
if __name__ == "__main__":
    def abrir_explorador_de_arquivos():
        os.system('start explorer')
    
    app = DeteccaoVisual(exibir_webcam=True)
    app.run()