import math
import sys


class DDM():
    
    
    def __init__(self, qtdInstanciasMinimas: int = 30, nivel_alerta: float = 2.0, nivel_mudanca: float = 3.0):
        
        self.qtdInstanciasMinimas = qtdInstanciasMinimas
        self.nivel_alerta = nivel_alerta
        self.nivel_mudanca = nivel_mudanca
        
        self.alerta = False
        self.mudanca = False
        
        self.erroPrequencial = 1.0
        self.desvioPadrao = 0
        self.qtdInstanciasAtual = 1
    
    
        self.p_min = sys.float_info.max
        self.s_min = sys.float_info.max
        self.p_s_minimo = sys.float_info.max
        
        
    def reset(self, qtdInstanciasMinimas: int = 30, nivel_alerta: float = 2.0, nivel_mudanca: float = 3.0):
        
        self.qtdInstanciasMinimas = qtdInstanciasMinimas
        self.nivel_alerta = nivel_alerta
        self.nivel_mudanca = nivel_mudanca
        
        self.alerta = False
        self.mudanca = False
        
        self.erroPrequencial = 1.0
        self.desvioPadrao = 0
        self.qtdInstanciasAtual = 1
    
    
        self.p_min = sys.float_info.max
        self.s_min = sys.float_info.max
        self.p_s_minimo = sys.float_info.max
        
    def qtdInstanciasMinimasAlcancado(self):
        
        if(self.qtdInstanciasAtual>=self.qtdInstanciasMinimas):
            return True
        else:
            return False
        
    def compute(self,acerto):
        
        self.erroPrequencial = (float) (self.erroPrequencial + ( (acerto - self.erroPrequencial)/ self.qtdInstanciasAtual) ) 
        self.desvioPadrao = math.sqrt(self.erroPrequencial * (1 - self.erroPrequencial)/ self.qtdInstanciasAtual )
        
   
        self.qtdInstanciasAtual+=1
        if(self.qtdInstanciasMinimasAlcancado()):
          
            if(self.erroPrequencial + self.desvioPadrao <= self.p_s_minimo):
                self.p_min = self.erroPrequencial
                self.s_min = self.desvioPadrao
                self.p_s_minimo = self.p_min + self.s_min
    
    def verifica_alerta(self):
        if(self.qtdInstanciasMinimasAlcancado()):
            if(self.erroPrequencial + self.desvioPadrao > self.p_min + self.nivel_alerta * self.s_min):
                print('Alerta')
                self.alerta = True
            
    def verifica_mudanca(self):
       
        if(self.qtdInstanciasMinimasAlcancado()):
            #print(self.erroPrequencial + self.desvioPadrao,self.p_min + self.nivel_mudanca * self.s_min)
            if(self.erroPrequencial + self.desvioPadrao > self.p_min + self.nivel_mudanca * self.s_min):
                print('Mudança')
                self.mudanca = True
                self.alerta = False
                
            
