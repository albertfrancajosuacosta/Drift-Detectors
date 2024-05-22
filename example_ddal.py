"""
Example of use the DDAL detector.
"""

from sklearn.datasets import load_iris
from sklearn import tree
import pandas as pd
import numpy as np
from ddal import DDAL

iris = load_iris()


df_x = pd.DataFrame(data= np.c_[iris['data'], iris['target']], columns= iris['feature_names'] + ['target'])


df_y = df_x.pop('target')

df_x_train = df_x[0:50]

df_y_train = df_y[0:50]



classifier = tree.DecisionTreeClassifier()

classifier.fit(df_x_train, df_y_train)

ddal = DDAL(size_batch = 50, theta = 0.005, lambida = 0.95)

df_x_test_batch_1 = df_x[50:100]

df_y_test_batch_1 = (df_y[50:100]).to_frame()

df_x_test_batch_1.reset_index(inplace=True,drop=True)
df_y_test_batch_1.reset_index(inplace=True,drop=True)

for index, row in df_x_test_batch_1.iterrows():
    
    
    y_pred = classifier.predict_proba(df_x_test_batch_1.iloc[[index]])

    max_y_pred_prob = y_pred.max()
    
    ddal.count_selected_instances(max_y_pred_prob)

ddal.compute_current_density()

if ddal.detection_module():
    
    print('Drift Detected')
    ddal.reset()