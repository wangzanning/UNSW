capstoneproject-comp9900-h18a-yyds


My Recipes is a recipes sharing platform that can let you look through and find
out wanted recipes by exploring the community. Final submission has been uploaded
to our team's GitHub classroom account on time. The zip file can be accessed by link. 
https://github.com/COMP3900-9900-Capstone-Project/capstoneproject-comp9900-h18a-yyds/blob/master/YYDSFinalSoftwareQuality.zip

The project is executable in the CSE vlab machines, please access the project by 
login the vlab gateway. Configuration and installation will be illustrated, and 
how to explore the platform will be explained in the following sections. 

To get the source code, please clone or download this repository. The website was 
developed in two streams including frontend and backend which should be configured 
and launched respectively. 

Before setting up the backend, Redis need to be installed manually by 

$ wget https://download.redis.io/releases/redis-6.2.5.tar.gz
$ tar xzf redis-6.2.5.tar.gz
$ cd redis-6.2.5
$ make

Make process will take few minutes, once it has been done, start Redis by:

$ src/redis-server

Run the following commands to create a virtual environment then install all 
libraries inside it automatically: 

$ cd backend/
$ python3 -m venv venv
$ source venv/bin/activate
$ pip install -r requirements.txt

If some of the libraries cannot be installed successufully, please run 

$ python3 -m pip install <library>

where replace the <library> to the missing dependency.

Then running 

$ python3 run.py

to launch the backend, the message shown below indicates the backend has started.

For the frontend, enter the frontend folder and install all the project dependencies by

$ cd frontend/
$ yarn install

If your local machine has not installed the Yarn, please install this package 
manager via npm and then do the command above to install dependencies.

$ npm install --global yarn

Finally, the website can be executed by 

$ yarn start

The browser will be launched automatically and display the welcome page, then 
you can start exploration.
