## Configuring your GIT Account

The following section brings information about the pre-configuration necessary to download and use GIT with public key cryptography in your computer. The description were made for Windows, Mac OS, and Linux.

### Windows and Mac OS

Please download the Source Tree using the link and follow the instructions to download the program: https://www.sourcetreeapp.com/. You can use your prefered app to manage git operations and it will have the same effect.

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
