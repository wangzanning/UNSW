
## Please rename this file to your student ID.py. e.g. z1234567.py
## STUDENT ID: FILL IN YOUR ID
## STUDENT NAME: FILL IN YOUR NAME


## Question 6

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

from sklearn.tree import DecisionTreeClassifier
from sklearn.datasets import make_blobs

np.random.seed(2)
n_points = 15
X, y = make_blobs(n_points, 2, centers=[(0,0), (-1,1)])
y[y==0] = -1       # use -1 for negative class instead of 0

plt.scatter(*X[y==1].T, marker="+", s=100, color="red")
plt.scatter(*X[y==-1].T, marker="o", s=100, color="blue")
#plt.savefig("boosting_data.png")
plt.show()

def plotter(classifier, X, y, title, ax=None):
    # plot decision boundary for given classifier
    plot_step = 0.02
    x_min, x_max = X[:, 0].min() - 1, X[:,0].max() + 1
    y_min, y_max = X[:, 1].min() - 1, X[:,1].max() + 1
    xx, yy = np.meshgrid(np.arange(x_min, x_max, plot_step), 
                            np.arange(y_min, y_max, plot_step)) 
    Z = classifier.predict(np.c_[xx.ravel(),yy.ravel()])
    Z = Z.reshape(xx.shape)
    if ax:
        ax.contourf(xx, yy, Z, cmap = plt.cm.Paired)
        ax.scatter(X[:, 0], X[:, 1], c = y)
        ax.set_title(title)
    else:
        plt.contourf(xx, yy, Z, cmap = plt.cm.Paired)
        plt.scatter(X[:, 0], X[:, 1], c = y)
        plt.title(title)


## Question 6 part a
# your code here


## Question 6 part b
def weighted_error(w, y, yhat):
    # your code here

T = 15
w = np.zeros((T, n_points))
w[0] = np.ones(n_points)/n_points

# storage for boosted model
alphas = np.zeros(T-1); component_models = []


## Question 6 part d
class boosted_model:
    def __init__(self, T):
        self.alphas = # your code here
        # your code here
    
    def predict(self, x):
        # your code here

# your code here