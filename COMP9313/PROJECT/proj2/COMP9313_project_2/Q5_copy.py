# Question 5

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
import warnings

warnings.simplefilter(action='ignore', category=FutureWarning)

import time
from sklearn.svm import SVC
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import AdaBoostClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.datasets import make_classification


def create_dataset():
    X, y = make_classification(n_samples=1250,
                               n_features=2,
                               n_redundant=0,
                               n_informative=2,
                               random_state=5,
                               n_clusters_per_class=1)
    rng = np.random.RandomState(2)
    X += 3 * rng.uniform(size=X.shape)
    linearly_separable = (X, y)
    X = StandardScaler().fit_transform(X)
    return X, y


x, y = create_dataset()
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2)

dt = DecisionTreeClassifier().fit(x_train, y_train)
rf = RandomForestClassifier().fit(x_train, y_train)
ab = AdaBoostClassifier().fit(x_train, y_train)
lr = LogisticRegression().fit(x_train, y_train)
mlp = MLPClassifier().fit(x_train, y_train)
svm = SVC().fit(x_train, y_train)

models = [dt, rf, ab, lr, mlp, svm]
names = ['Decision Tree', 'Random Forest', 'AdaBoost', 'Logistic Regression',
         'Neural Network', 'SVM']
names_acc_dic = {i:[] for i in names}
names_time_dic = {i:[] for i in names}



def plotter(classifier, X, X_test, y_test, title, ax=None):
    # plot decision boundary for given classifier
    plot_step = 0.02
    x_min, x_max = X[:, 0].min() - 1, X[:, 0].max() + 1
    y_min, y_max = X[:, 1].min() - 1, X[:, 1].max() + 1
    xx, yy = np.meshgrid(np.arange(x_min, x_max, plot_step),
                         np.arange(y_min, y_max, plot_step))
    Z = classifier.predict(np.c_[xx.ravel(), yy.ravel()])
    Z = Z.reshape(xx.shape)
    if ax:
        ax.contourf(xx, yy, Z, cmap=plt.cm.Paired)
        ax.scatter(X_test[:, 0], X_test[:, 1], c=y_test)
        ax.set_title(title)
    else:
        plt.contourf(xx, yy, Z, cmap=plt.cm.Paired)
        plt.scatter(X_test[:, 0], X_test[:, 1], c=y_test)
        plt.title(title)


fig, ax = plt.subplots(2, 3, figsize=(10, 10))
for i, ax in enumerate(ax.flat):
    plotter(models[i], x_train, x_test, y_test, names[i], ax=ax)
plt.tight_layout()
plt.show()

sample_nums = [50, 100, 200, 300, 400, 500, 600, 700, 800, 900, 1000]

ls = list(range(x_train.shape[0]))
for m in range(len(models)):
    for nums in sample_nums:
        accs = []
        secs = []
        for i in range(10):
            indexes = random.sample(ls, nums)
            train_x1 = x_train[indexes]
            train_y1 = y_train[indexes]

            start = time.time()
            models[m].fit(train_x1, train_y1)
            end = time.time()
            secs.append(end-start)
            accs.append(models[m].score(x_test, y_test))
        acc = sum(accs) / 10
        accs.clear()
        names_time_dic[names[m]].append(sum(secs) / 10)
        secs.clear()
        names_acc_dic[names[m]].append(acc)

# accuracy
x1 = names_acc_dic['Decision Tree']
x2 = names_acc_dic['Random Forest']
x3 = names_acc_dic['AdaBoost']
x4 = names_acc_dic['Logistic Regression']
x5 = names_acc_dic['Neural Network']
x6 = names_acc_dic['SVM']

plt.plot(sample_nums, x1, color='blue',label='Decision Tree')
plt.plot(sample_nums, x2,color = 'orange', label='Random Forest')
plt.plot(sample_nums, x3, color ='green' ,label='AdaBoost')
plt.plot(sample_nums, x4, color = 'red', label='Logistic Regression')
plt.plot(sample_nums, x5, color = 'pink',label='Neural Network')
plt.plot(sample_nums, x6, color = 'goldenrod',label='SVM')

plt.xlabel('Data size')
plt.ylabel('Accuracy')
plt.legend()
plt.show()

# time
plt.clf()
x1 = names_time_dic['Decision Tree']
x2 = names_time_dic['Random Forest']
x3 = names_time_dic['AdaBoost']
x4 = names_time_dic['Logistic Regression']
x5 = names_time_dic['Neural Network']
x6 = names_time_dic['SVM']

plt.plot(sample_nums, x1, color='blue',label='Decision Tree')
plt.plot(sample_nums, x2,color = 'orange', label='Random Forest')
plt.plot(sample_nums, x3, color ='green' ,label='AdaBoost')
plt.plot(sample_nums, x4, color = 'red', label='Logistic Regression')
plt.plot(sample_nums, x5, color = 'pink',label='Neural Network')
plt.plot(sample_nums, x6, color = 'goldenrod',label='SVM')

plt.xlabel('Data size')
plt.ylabel('Training time(millisecond)')
plt.legend()
plt.show()
a =1