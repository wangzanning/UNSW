
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

# e.g.
dt = DecisionTreeClassifier(max_depth=5)
dt.fit(X, y)
plotter(dt, X, y, "Decision Tree")



## Question 6 part a
fig, ax = plt.subplots(3,3, figsize=(10,10))
titles = [f"DT max_depth={i}" for i in range(1,10)]
for i, ax in enumerate(ax.flat):
    dt = DecisionTreeClassifier(max_depth=i+1).fit(X, y)
    plotter(dt, X, y, titles[i], ax)
#plt.savefig("boosting_a.png")
plt.tight_layout()
plt.show()




## Question 6 part b
def weighted_error(w, y, yhat):
    return np.sum(w*(y!=yhat))

T = 15
w = np.zeros((T, n_points))
w[0] = np.ones(n_points)/n_points

# storage for boosted model
alphas = np.zeros(T-1); component_models = []

def boosted_model(x, alphas, component_models): 
    individual_preds = np.array([m.predict(x) for m in component_models])
    alphaM = alphas * individual_preds.T
    return np.sign(alphaM.sum(axis=1))

for t in range(1, T):
    
    # select weak classifier that minimises weighted error
    dt = DecisionTreeClassifier(max_depth=1).fit(X, y, sample_weight=w[t-1])
    
    # compute predictions from current model
    yhat = dt.predict(X)
    
    # comptue weighted error epsilon_t
    eps_t = weighted_error(w[t-1], y, yhat)
    
    # compute alpha_t (model weight)
    alpha_t = 0.5 * np.log((1-eps_t)/eps_t)
    
    # update weights for next round 
    for i in range(n_points):
        if y[i] == yhat[i]: 
            # correctly classified instances
            w[t, i] = w[t-1, i]/(2 * (1-eps_t))
        else:
            # misclassified instances
            w[t, i] = w[t-1, i]/(2 * eps_t)
    
    # save model 
    alphas[t-1] = alpha_t
    component_models.append(dt)
    
boosted_preds = boosted_model(X, alphas, component_models)
np.all((boosted_preds * y) == 1)     # check all classified correctly




## Question 6 part d
class boosted_model:
    def __init__(self, T):
        self.alphas = np.zeros(T-1)
        self.component_models = []
    
    def predict(self, x):
        individual_preds = np.array([m.predict(x) for m in self.component_models])
        alphaM = self.alphas * individual_preds.T
        return np.sign(alphaM.sum(axis=1))

bms = []

for T in range(2, 18):
    w = np.zeros((T, n_points))
    w[0] = np.ones(n_points)/n_points

    bm = boosted_model(T)
    for t in range(1, T):

        # select weak classifier that minimises weighted error
        dt = DecisionTreeClassifier(max_depth=1).fit(X, y, sample_weight=w[t-1])

        # compute predictions from current model
        yhat = dt.predict(X)

        # comptue weighted error epsilon_t
        eps_t = weighted_error(w[t-1], y, yhat)

        # compute alpha_t (model weight)
        alpha_t = 0.5 * np.log((1-eps_t)/eps_t)

        # update weights for next round 
        for i in range(n_points):
            if y[i] == yhat[i]: 
                # correctly classified instances
                w[t, i] = w[t-1, i]/(2 * (1-eps_t))
            else:
                # misclassified instances
                w[t, i] = w[t-1, i]/(2 * eps_t)

        # save model 
        bm.alphas[t-1] = alpha_t
        bm.component_models.append(dt)
    
    # store current boosted model
    bms.append(bm)
    

fig, ax = plt.subplots(4,4, figsize=(12,12))
titles = [f"n_components={i}" for i in range(2,18)]
for i, ax in enumerate(ax.flat):
    plotter(bms[i], X, y, titles[i], ax)
#plt.savefig("boosting_grid.png")
plt.tight_layout()
plt.show()