# Starting Steps

Follow this steps to get ready to work

## Configuring your GIT Account

The following section brings information about the pre-configuration necessary to download and use GIT with public key cryptography in your computer. The description were made for Windows, Mac OS, and Linux.

### Windows and Mac OS

Please download the Source Tree using the link and follow the instructions to download the program: https://www.sourcetreeapp.com/ . You can use your prefered app to manage git operations and it will have the same effect.

### Linux

    In your command line execute the following commands or equivalent ones for your distribution. The distributions used in this example was Ubuntu 15.04.
* git config --global user.name "You full name here"
* git config --global user.email you@yourdomain.example.com
* git config --global color.diff auto
* git config --global color.status auto
* git config --global color.branch auto
* mkdir ~/.ssh (If already created skip this step)
* cd ~/.ssh
* sh-keygen -t rsa -C "your_gitaccount@youremail.com"
* gedit ~/.ssh/id_rsa.pub (Follow the instructions on terminal)
* Copy the public key to the your public key list on GitHub, BitBucket or the service that you are using at the moment. (Watch the video tutorial number 1 to see how to do that on GitHub)
* Create a folder (~/Developer/heavy) in a place of your preference for store the files of the project that you are going to clone.
* Inside of this folder execute git init
* git remote add origin git@github.com:HeavyConnected/api.git (go to the project on GitHub or BitBucket and replace the red part with the link given by the service when you select the option to clone with SSH.).
* git remote -v (check if the name for push and fetch match the git@github.com:HeavyConnected/api.git that you have just added.
* git fetch origin
* git pull origin master
* You are ready to the next step :)!

## Configuring Django

The following steps will help you to configure the development environment that you developer will use to implement the functions that are part of the Heavy Connect App. Follow these steps to configure the development environment in your computer. At the moment this document was written the last version of Python 2.7.X available was the version 2.7.10. Additionally the Windows version used was Windows 8.1, the Mac OS version was the 10.10.3, and the Linux Distribution used was Ubuntu (the steps described in this document may vary according to the distribution that you are using)

### Windows
* Make sure you have installed any version of Python 2.7.X in your system. You can get the last build for the version 2.7.X in the following address https://www.python.org/downloads/
* Install the MSI file in your system.

### Mac OS and Linux
* Make sure you have installed any version of Python 2.7.X in your system. You can get the last build for the version 2.7.X in the following address https://www.python.org/downloads/
* Install the PKG or TAR file in your system.
* Check if Python was successfully installed in your system by executing the following commands:
    ** $PATH | grep "python” (MAC only)d that the default configure settings work fine for Ubuntu 10.04 and there's no real need to specify extra --with flags.- You should expect to see the path to the place where Python was installed 
    ** python --version - You should expect to see the version that you just installed in your system
* You now will install the setuptools package in your system. Go to https://pypi.python.org/pypi/setuptools and download the setuptools.
* Extract the content of the setuptools to a folder of your preference.
* Throught command line access the folder that you have extracted the file.
*  Run the following command:
    ** python setup.py install
    ** easy_install virtualenv
* Create a folder in your home directory called Developer with the following command: mkdir ~/Developer
* Go to this folder: cd ~/Developer
* Clone the Heavy Connect project from github to this folder
* Inside of the folder of the project execute the following commands.
    ** virtualenv venv --distribute
    ** source venv/bin/activate
    ** pip install -r requirements.txt
    ** pip freeze
    ** Go to the heavyconnect folder.
    ** python manage.py syncdb (create a super user with the following name heavy and password 123)
    ** python manage.py migrate
