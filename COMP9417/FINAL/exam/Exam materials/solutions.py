
## STUDENT ID: z5224151
## STUDENT NAME: ZANNING WANG


## Question 2

import numpy as np
import matplotlib.pyplot as plt

np.random.seed(42)       # make sure you run this line for consistency 
x = np.random.uniform(1, 2, 100)
y = 1.2 + 2.9 * x + 1.8 * x**2 + np.random.normal(0, 0.9, 100)
plt.scatter(x,y)
plt.show()

## (c)

# YOUR CODE HERE

## plotting help
fig, ax = plt.subplots(3,3, figsize=(10,10))
alphas = [10e-1, 10e-2, 10e-3,10e-4,10e-5,10e-6,10e-7, 10e-8, 10e-9]
for i, ax in enumerate(ax.flat):
    # losses is a list of 9 elements. Each element is an array of length 100 storing the loss at each iteration for that particular step size
    ax.plot(losses[i])         
    ax.set_title(f"step size: {alphas[i]}")	 # plot titles	
    plt.tight_layout()      # plot formatting
    plt.show()





## Question 3

import numpy as np

#import the data
x0 = [1, 1, 1, 1, 1, 1, 1, 1]
x1 = [-0.8, 3.9, 1.4, 0.1, 1.2, -2.45, -1.5, 1.2]
x2 = [1, 0.4, 1, -3.3, 2.7, 0.1, -0.5, -1.5]
y = [1, -1, 1, -1, -1, -1, 1, 1]

#save into numpy
np_x0 = np.asarray(x0)
np_x1 = np.asarray(x1)
np_x2 = np.asarray(x2)
np_y = np.asarray(y)
w_start = [1.00, 1.00, 1.00]
learning_rate = 0.2
counter = 0

#check convergence or not
def check_positive(x0, x1, x2, y):
    print("--------------------")
    global w_start, counter
    wTx = (w_start[0] * x0) + (w_start[1] * x1) + (w_start[2] * x2)
    ywTx = wTx * y

    #use to count the total number of convergence in each iteration
    if ywTx >= 0:
        counter += 1
    else:
        w_start = [w_start[0] - y * (learning_rate * x0), w_start[1] - y * (learning_rate * x1),
                   w_start[2] - y * (learning_rate * x2)]


print("φ(xi)        yiφT(xi)w*")
counter2 = 0
while True:
    counter = 0
    #check each vector
    for i in range(8):
        check_positive(np_x0[i], np_x1[i], np_x2[i], np_y[i])
        list_w = [w_start[0], w_start[1], w_start[2]]

        if list_w:
            b = "ri > 0"
        print(list_w, b)
    #break when all convergence
    if counter == 8:
        break

    #in case infinite loop happen
    counter2 += 1
    if counter2 == 100:
        break


# Question 5


import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
import warnings
import random

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


#initial the dataset
dataset_x, dataset_y = create_dataset()

# split data
train_x, test_x, train_y, test_y = train_test_split(dataset_x, dataset_y, test_size=0.20)

# fit all model
Decision_tree = DecisionTreeClassifier().fit(train_x, train_y)
Random_forest = RandomForestClassifier().fit(train_x, train_y)
Multi_layer = MLPClassifier().fit(train_x, train_y)
Ada_boost = AdaBoostClassifier().fit(train_x, train_y)
Support_vector = SVC().fit(train_x, train_y)
Logistic_reg = LogisticRegression().fit(train_x, train_y)

#delcare dict to store each model accuracy and run_time
accuracy_dict = {}
time_dict = {}

#initial the different names for index
model_mames = [Decision_tree, Random_forest, Multi_layer, Logistic_reg, Ada_boost, Support_vector]
name_list = ['Decision_tree', 'Random_forest', 'Multi_layer', 'Logistic_reg', 'Ada_boost', 'Support_vector']
#save the value of each model into dict
for i in name_list:
    accuracy_dict[i] = []
    time_dict[i] = []

#this part refer the Sample exam
fig, ax = plt.subplots(2, 3, figsize=(10, 10))
for i, ax in enumerate(ax.flat):
    plotter(model_mames[i], train_x, test_x, test_y, name_list[i], ax=ax)
plt.tight_layout()
plt.show()
#end of refer

print_list = [50, 100, 200, 300, 400, 500, 600, 700, 800, 900, 1000]
x_train_count = list(range(train_x.shape[0]))

#get the time each program run
def get_time(k, x, y):
    start_time = time.time()
    model_mames[k].fit(x, y)
    end_time = time.time()
    time_use = end_time - start_time
    return time_use

#run by each model
for k in range(6):
    #run by each training set sizes
    for n in print_list:
        accuracy_list = []
        run_time = []

        #run by ten times
        for i in range(10):
            #get the train by random
            train_1_X = train_x[random.sample(x_train_count, n)]
            train_1_Y = train_y[random.sample(x_train_count, n)]

            #get the time each part run
            time_run = get_time(k, train_1_X, train_1_Y)
            run_time.append(time_run)

            #use score to get the accuracy directly
            model_score = model_mames[k].score(test_x, test_y)
            accuracy_list.append(model_score)

        out_accuracy = (sum(accuracy_list) / 10)
        accuracy_dict[name_list[k]].append(out_accuracy)
        time_dict[name_list[k]].append(sum(run_time) / 10)

        accuracy_list.clear()
        run_time.clear()
#check the dict content
#print(accuracy_dict)
#print(time_dict)

# print accuracy
#the color may wrong, I can not find exactly right color
plt.plot(print_list, accuracy_dict['Decision_tree'], color='aliceblue', label='Decision Tree')
plt.plot(print_list, accuracy_dict['Random_forest'], color='orange', label='Random Forest')
plt.plot(print_list, accuracy_dict['Logistic_reg'], color='red', label='Logistic Regression')
plt.plot(print_list, accuracy_dict['Support_vector'], color='yellowgreen', label='SVM')
plt.plot(print_list, accuracy_dict['Ada_boost'], color='limegreen', label='AdaBoost')
plt.plot(print_list, accuracy_dict['Multi_layer'], color='pink', label='Neural Network')

plt.ylabel('accuracy')
plt.xlabel('data size')
plt.legend()
plt.show()

# print time
plt.plot(print_list, time_dict['Decision_tree'], color='aliceblue', label='Decision Tree')
plt.plot(print_list, time_dict['Random_forest'], color='orange', label='Random Forest')
plt.plot(print_list, time_dict['Logistic_reg'], color='red', label='Logistic Regression')
plt.plot(print_list, time_dict['Support_vector'], color='yellowgreen', label='SVM')
plt.plot(print_list, time_dict['Ada_boost'], color='limegreen', label='AdaBoost')
plt.plot(print_list, time_dict['Multi_layer'], color='pink', label='Neural Network')


plt.ylabel('training time')
plt.xlabel('data size')
plt.legend()
plt.show()
a = 1