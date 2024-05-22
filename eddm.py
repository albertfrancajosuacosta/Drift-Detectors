import math
import sys


class EDDM():
    
    
    def __init__(self, qtdMinimaErros: int = 30, alpha: float = 0.95, beta: float = 0.90):
        
        
        self.posicaoInstanciaAtual = 0
        
        self.qtdMinimaErros = qtdMinimaErros
        self.alpha = alpha
        self.beta = beta
        
        self.qtdErrosAtual = 1
        self.posicaoUltimoErro = 0
        
        self.alerta = False
        self.mudanca = False
        
        self.mediaDistanciaErro = 0.0
        self.desvioPadrao = 0.0
        
        
        self.m2s = sys.float_info.min
        self.m2s_maxima = sys.float_info.min
       
        
        
        
    def reset(self, qtdMinimaErros: int = 30, alpha: float = 0.95, beta: float = 0.90):
        self.posicaoInstanciaAtual = 0
        
        self.qtdMinimaErros = qtdMinimaErros
        self.alpha = alpha
        self.beta = beta
        
        self.qtdErrosAtual = 1
        self.posicaoUltimoErro = 0
        
        self.alerta = False
        self.mudanca = False
        
        self.mediaDistanciaErro = 0.0
        self.desvioPadrao = 0.0
        
        
        self.m2s = sys.float_info.min
        self.m2s_maxima = sys.float_info.min
        
        
    def qtdErrosLimiteInferior(self):
        if(self.qtdErrosAtual>=self.qtdMinimaErros):
            return True
        else:
            return False
        
    def compute(self,acerto):
        
        self.posicaoInstanciaAtual+=1
        
        if acerto == 1:
            distancia = (self.posicaoInstanciaAtual - self.posicaoUltimoErro)
            
            self.posicaoUltimoErro = self.posicaoInstanciaAtual
            
            mmediaDistanciaErroAnterior = self.mediaDistanciaErro
            
            self.mediaDistanciaErro = (float)(self.mediaDistanciaErro + ( (distancia-self.mediaDistanciaErro)/self.qtdErrosAtual) )
      
            self.desvioPadrao = self.desvioPadrao + (distancia - self.mediaDistanciaErro) * (distancia - mmediaDistanciaErroAnterior)
    
            std = math.sqrt( self.desvioPadrao/self.qtdErrosAtual)
            
            self.m2s = self.mediaDistanciaErro + 2 * std
            
            self.qtdErrosAtual+=1
            
            if(self.qtdErrosLimiteInferior()):
                if self.m2s > self.m2s_maxima:
                    self.m2s_maxima = self.m2s
            
            
   
    def verifica_alerta(self):
        if(self.qtdErrosLimiteInferior()):
            if( (self.m2s/self.m2s_maxima) < self.alpha ):
                print('Alerta')
                self.alerta = True
            
    def verifica_mudanca(self):
       
        if(self.qtdErrosLimiteInferior()):
            if( (self.m2s/self.m2s_maxima) < self.beta ):
                print('Mudança')
                self.mudanca = True
                self.alerta = False
                
            
