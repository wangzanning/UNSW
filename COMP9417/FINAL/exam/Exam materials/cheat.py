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

#######################
#my:
dataset_x = create_dataset()
dataset_y = create_dataset()

#split data
train_x , test_x = train_test_split(dataset_x,test_size = 0.20)
train_y , test_y = train_test_split(dataset_y,test_size = 0.20)

#fit all model
Decision_tree = DecisionTreeClassifier().fit(train_x, train_y)
Random_forest = RandomForestClassifier().fit(train_x, train_y)
Multi_layer = MLPClassifier().fit(train_x, train_y)
Logistic_reg = LogisticRegression().fit(train_x, train_y)
Ada_boost = AdaBoostClassifier().fit(train_x, train_y)
Support_vector = SVC().fit(train_x, train_y)
accuracy_dict = {}
time_dict = {}

model_mames = [dt, rf, mlp, lr, ab, svm]
name_list = ["Decision_tree", "Random_forest", "Multi_layer", "Logistic_reg", "Ada_boost", "Support_vector"]
for i in name_list:
    accuracy_dict[i] = []
    time_dict[i] = []

###########################
#改：
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

#my：

fig, ax = plt.subplots(2, 3, figsize=(10, 10))
for i, ax in enumerate(ax.flat):
    plotter(model_mames[i], train_x, test_x, test_y, name_list[i], ax=ax)
plt.tight_layout()
plt.show()

print_list = [50, 100, 200, 300, 400, 500, 600, 700, 800, 900, 1000]
x_train_count = list(range(train_x.shape[0]))

for k in range(6):
    for n in print_list:
        accuracy_list = []
        run_time = []

        for i in range(10):
            ind = random.sample(x_train_count, n)
            train_1_X = train_x[ind]
            train_1_Y = train_y[ind]

            start_time = time.time()
            model_mames[k].fit(train_1_X,train_1_Y)
            end_time = time.time()
            run_time.append(end_time-start_time)

            model_score = model_mames[k].score(test_x, test_y)
            accuracy_list.append(model_score)


        out_accuracy = sum(accuracy_list) / 10
        accuracy_list.clear()
        time_dict[names[k]].append(sum(run_time) / 10)
        run_time.clear()
        time_dict[names[k]].append(out_accuracy)

##############
#改

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

#########
#my

#print accuracy
plt.plot(print_list, accuracy_dict['Decision Tree'], color='aliceblue',label='Decision Tree')
plt.plot(print_list, accuracy_dict['Random Forest'],color = 'orange', label='Random Forest')
plt.plot(print_list, accuracy_dict['Logistic Regression'], color = 'red', label='Logistic Regression')
plt.plot(print_list, accuracy_dict['SVM'], color = 'darksage',label='SVM')
plt.plot(print_list, accuracy_dict['AdaBoost'], color ='limegreen' ,label='AdaBoost')
plt.plot(print_list, accuracy_dict['Neural Network'], color = 'pink',label='Neural Network')

plt.xlabel('data size')
plt.ylabel('accuracy')
plt.legend()
plt.show()

#print time
plt.plot(print_list, time_dict['Decision Tree'], color='aliceblue',label='Decision Tree')
plt.plot(print_list, time_dict['Random Forest'],color = 'orange', label='Random Forest')
plt.plot(print_list, time_dict['Logistic Regression'], color = 'red', label='Logistic Regression')
plt.plot(print_list, time_dict['SVM'], color = 'darksage',label='SVM')
plt.plot(print_list, time_dict['AdaBoost'], color ='limegreen' ,label='AdaBoost')
plt.plot(print_list, time_dict['Neural Network'], color = 'pink',label='Neural Network')

plt.xlabel('data size')
plt.ylabel('training time')
plt.legend()
plt.show()
a =1
