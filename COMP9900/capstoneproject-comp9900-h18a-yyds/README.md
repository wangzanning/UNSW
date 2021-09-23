# capstoneproject-comp9900-h18a-yyds

### Team Members:

* z5288155	Weizhou Ren
* z5244619	Yunze Shi
* z5300340	Xiaoheng Hong
* z5238743	Yu Zhang
* z5224151	Zanning Wang


## **Overview**
---
My Recipes is a recipes sharing platform that can let you look through and find out wanted recipes by exploring the community. The project is executable in the CSE vlab machines, please access the project by login the vlab gateway. Configuration and installation will be illustrated, and how to explore the platform will be explained in the following sections. 

## **Installation and Setup**
---
To get the source code, please clone or download this repository. The website was developed in two streams including frontend and backend which should be configured and launched respectively. 

### Backend
**Redis**
Before setting up the backend, redis need to be installed manually by 
```
$ wget https://download.redis.io/releases/redis-6.2.5.tar.gz
$ tar xzf redis-6.2.5.tar.gz
$ cd redis-6.2.5
$ make
```
Make process will take few minutes, once it has been done, start Redis by:
```
$ src/redis-server
```
**Virtual Environment and Dependencies**

To run the backend and access the database, several libraries need to be installed. Enter the backend folder and access the files of ```README.md``` and ```requirement.txt``` to see the needed libraries. And run the following commands to create a virtual environment then install all libraries inside it automatically: 
```
$ cd backend/
$ python3 -m venv venv
$ source venv/bin/activate
$ pip install -r requirements.txt
```

Then running 
```
$ python3 run.py
```
to launch the backend, the message shown below indicates the backend has started.


### Frontend

Enter the frontend folder and install all the project dependencies by
```
$ cd frontend/
$ yarn install
```
If your local machine has not installed the Yarn, please install this package manager via npm and then do the command above to install dependencies.
```
$ npm install --global yarn
```
Finally, the website can be executed by 
```
$ yarn start
```

The browser will be launched automatically and display the welcome page, then you can start exploration.
