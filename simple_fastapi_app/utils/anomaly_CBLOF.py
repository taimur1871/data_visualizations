# python3
# imports
import numpy as np
from pyod.models.cblof import CBLOF
#import matplotlib.pyplot as plt

def detect_anomaly(df):
    x = np.array(df[['adj_x','adj_y']])

    # select model and method
    clf = CBLOF(n_clusters=4)
    try:
        clf.fit(x)
    except ValueError:
        return df

    scores_pred = clf.decision_function(x) * -1

    y_pred = clf.predict(x)
    n_inliers = len(y_pred) - np.count_nonzero(y_pred)
    n_outliers = np.count_nonzero(y_pred == 1)
    #plt.figure(figsize=(12, 12))

    df1 = df
    df1['outlier'] = y_pred.tolist()
        
    # sales - inlier feature 1,  profit - inlier feature 2
    inliers_x = np.array(df1['adj_x'][df1['outlier'] == 0]).reshape(-1,1)
    inliers_y = np.array(df1['adj_y'][df1['outlier'] == 0]).reshape(-1,1)
        
    # sales - outlier feature 1, profit - outlier feature 2
    outliers_x = df1['adj_x'][df1['outlier'] == 1].values.reshape(-1,1)
    outliers_y = df1['adj_y'][df1['outlier'] == 1].values.reshape(-1,1)
            
    #print('OUTLIERS: ',n_outliers,'INLIERS: ',n_inliers)
    '''
    b = plt.scatter(inliers_x, inliers_y, c='white',s=20, edgecolor='k')
        
    c = plt.scatter(outliers_x, outliers_y, c='black',s=20, edgecolor='k')
        
    plt.axis('tight')
    plt.title('CBLOF')
    plt.show()
    '''
    return df[(df['outlier']==0)]