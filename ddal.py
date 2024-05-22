import sys



class DDAL():
    """
    A Drift Detection Method Based on Active Learning.
    
    DDAL is a concept drift detection method based on  
    density variation of the most significant instances selected for Active Learning.
    
    More information:
        https://ieeexplore.ieee.org/document/8489364
        
        Albert França Josuá Costa
        Regis Antonio Saraiva Albuquerque
        Eulanda Miranda dos Santos
        
    Parameters
    ----------
    size_batch
        Size of instances batch.
    
    theta
        Drift threshold.

    lambida
        Uncertainty threshold.
        
    Methods
    ----------
    fixed_uncertainty
        Compute the uncertainty of the current instance.
    
    count_selected_instances
        Check if current instances fall in the virtual margin.
    
    compute_current_density
        Compute the current density into the current batch.
    
    detection_modulo
        Check if drift ocurred.
        
    reset
        Reset the detector.
        
    Example
    ----------
    >>> from sklearn.datasets import load_iris
    >>> from sklearn import tree
    >>> import pandas as pd
    >>> import numpy as np
    >>> from ddal import DDAL

    >>> iris = load_iris()

    >>> df_x = pd.DataFrame(data= np.c_[iris['data'], iris['target']], columns= iris['feature_names'] + ['target'])


    >>> df_y = df_x.pop('target')

    >>> df_x_train = df_x[0:50]

    >>> df_y_train = df_y[0:50]



    >>> classifier = tree.DecisionTreeClassifier()

    >>> classifier.fit(df_x_train, df_y_train)

    >>> ddal = DDAL(size_batch = 50, theta = 0.005, lambida = 0.95)

    >>> df_x_test_batch_1 = df_x[50:100]

    >>> df_y_test_batch_1 = (df_y[50:100]).to_frame()

    >>> df_x_test_batch_1.reset_index(inplace=True,drop=True)
    >>> df_y_test_batch_1.reset_index(inplace=True,drop=True)

    >>> for index, row in df_x_test_batch_1.iterrows():
        
        
        >>> y_pred = classifier.predict_proba(df_x_test_batch_1.iloc[[index]])

        >>> max_y_pred_prob = y_pred.max()
        
        >>> ddal.count_selected_instances(max_y_pred_prob)

    >>> ddal.compute_current_density()

    >>> if ddal.detection_module():
        
        >>> print('Drift Detected')
        >>> ddal.reset()
    
    """
    
    def __init__(self, size_batch: int = 500, theta: float = 0.005, lambida: float = 0.95):
        self.theta = theta
        self.lambida = lambida
        self.max_density = sys.float_info.min
        self.min_density = sys.float_info.max
        self.current_density = 0.0
        self.amount_selected_instances = 0
        self.size_batch = size_batch
        
    
    def fixed_uncertainty(self,maximum_posteriori):
        selected = False
        if maximum_posteriori < self.lambida:
            selected = True
        return selected
        
    def count_selected_instances(self,maximum_posteriori):
        s = self.fixed_uncertainty(maximum_posteriori)
        if s:
            self.amount_selected_instances+=1
    
    
    def compute_current_density(self):
        
        self.current_density = (float) (self.amount_selected_instances/self.size_batch)
        
    
    def detection_module(self):
        
        isDrift = False
        
        if self.current_density > self.max_density:
            self.max_density = self.current_density
        
        if self.current_density < self.min_density:
            self.min_density = self.current_density
        
        
        if (self.max_density-self.min_density) > self.theta:
            
            isDrift = True
        
        return isDrift
        
 
    
    def reset(self, size_batch: int = 500, theta: float = 0.95, lambida: float = 0.95):
        self.theta = theta
        self.lambida = lambida
        self.max_density = sys.float_info.min
        self.min_density = sys.float_info.max
        self.current_density = 0.0
        self.count_selected_instances = 0
        self.size_batch = size_batch