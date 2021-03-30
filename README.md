# Typee-Typo
<a href="url"><img src="https://github.com/eliot-portevin/Typee-Typo/blob/main/Preview.png" align="center"></a>

## Introduction
The main purpose of Typee Typo is to help people evaluate the evolution of their typing speed. This tool wasn't optimised for regular training, but can be used so if wished. The long term objective would be for me to make my Maturarbeit on this, firstly explaining how I got the program to work, and in a second part analysing the evolution of your performances and comparing them (you won't be put at competition don't worry). Some of the services included so far:
- Speed testing in English, French and German
- Analysis of personal data each time the program runs
- Possibility to turn the awful music off

***This program is Open-Source, so you are free to modify it according to your desires. However, I won't be able to help you if it doesn't run after your modifications.***

## Getting Help
If you're struggling with the installation, or if you need any kind of advice from and old and wise man, please contact me at ***eliot.portevin@stud.edubs.ch***. 

If you wish to add a feature to the program, you are also free to modify the one you have cloned from this repository, and to show it to me when it is fully tested (if it is a good idea of course).

## Installation
### Mac OS
*(All the commands listed below have to be run in the terminal application without the dollar sign, which just shows the beginning of the commands. Don't be scared of the command line, you'll have to use it anyways to run the program, and you'll look like a hacker.)*

On this Operating System, Python is already installed by default. You can check it with this command ```$ python --version```. If you don't have version 3 or higher, go and install it at their website https://www.python.org/downloads/.

Next, you will need to install the Git command in order to clone this repository. To do so, run
```
$ git version
```
If you don’t have it installed already, it will prompt you to install it.
If you want a more up to date version, you can also install it via a binary installer. A macOS Git installer is maintained and available for download at the Git website, at https://git-scm.com/download/mac.

Now you can clone this repository (all the files at the top of the page) in your desired directory. To do so, open your terminal and move to the desired path with the  ```cd```  command. If you do not know how this works, this video explains it well: https://www.youtube.com/watch?v=j6vKLJxAKfw. Next you can run this command to download the repository:
```
$ git clone https://github.com/eliot-portevin/Typee-Typo.git
```
You now have all the needed files to run this program in you new Typee-Typo directory! Go to the Running part to see how you can use it now.

### Linux
If you're running Linux (congrats' because I wouldn't expect any of you to), I'm assuming you know how to use the command line, clone a repository and run a python script, so I'm not including any directions for you. If you're really in a struggle though, just take a look at the MacOS tutorial, it's literaly the same thing. To install git, just run ```sudo apt install git```if you're on a debian-based machine, or ```yay -S git```if you're on Arch (I'm not sure about this one though).

### Windows
Now to all the windows users, I am terribly sorry but I don't have a windows machine at home, and when I tried running this program on some friend's computers, it didn't work. You are welome to give it a go, but I can't guarantee that it will work...

*(All the commands listed below have to be run in the Command Line application without the dollar sign, which just shows the beginning of the commands. Don't be scared of the terminal, you'll have to use it anyways to run the program, and you'll look like a hacker.)*

Firstly, install Python if it isn't installed yet. To check if you have it, you can run ```$ python --version```. If it outputs that python is not a recognised command, then install from this website: https://www.python.org/downloads/windows/ by following their instructions. Pay attention to which version you're installing: from my experience, versions lower than Python 3.0 didn't work... After that, if you run the previously mentionned command, you should get an output similar to this:
```
C: \Users\yourusername\directory>python --version
Python 3.8.3
```
Next you will need the git command which you can download from this website: https://git-scm.com/download/win. The graphical interface will guide you through the installation.

Now you have all the dependencies needed to copy this repository, but not all to run it yet. You may now navigate to the folder you wish to have your game in with the  ```cd```  command. If you do not know how this works, please watch this video that will inform you about it: https://www.youtube.com/watch?v=zZshUoznlH4. You will need to be able to do this in order to run the program. Next you can run this command to download the repository:
```
$ git clone https://github.com/eliot-portevin/Typee-Typo.git
```
You now have all the needed files to run this program in you new Typee-Typo directory! Go to the Running part to see how you can use it now.

## Running
The running process is the exact same for every Operating System, run:
```
$ cd /path/to/your/directory
$ python3 TypeeTypo.py
```
*Don't put the 3 if you don't have Python version 3.*

Each time the program runs, it checks whether you have all necessary packages installed. The first time, it may therefore take up to a minute before launching. Afterwards, the process only takes a second and the output will look like this:
```
$ python3 TypeeTypo.py 
[LOG] Looking for numpy
[LOG] numpy is already installed, skipping...
[LOG] Looking for matplotlib
[LOG] matplotlib is already installed, skipping...
[LOG] Looking for pygame
[LOG] pygame is already installed, skipping...
[LOG] Looking for datetime
[LOG] datetime is already installed, skipping...
[LOG] Looking for csv
[LOG] csv is already installed, skipping...
[LOG] Looking for sys
[LOG] sys is already installed, skipping...
[LOG] Looking for random
[LOG] random is already installed, skipping...

$
```
When you are playing, you have to type all the words you see as fast as you can. You'll never run out, it's set so there's always a certain number of them on the screen. Each time you have typed one word, you can press [SPACE] to make it count. Those of you who have already tried 10fastfingers.com will be familiar with this principle. Pressing [ESC] in game shows a little pop-up with some stats and pauses the game. To quit, you just have to close the window, which can be inconvenient if you want to play several times in a row but hey, I'm not Elon Musk so this isn't optimal.

All your scores are saved automatically at Media/score.csv . If you wish to delete a score because you didn't take the test seriously, you can just delete the last line. However, please don't play around with them because as mentionned above, your performances will be the support for my Maturarbeit. You can also add words in the word lists in the Media folder (words.txt for English, mots.txt for French and Wörtern.txt for German). If you wish to change the ingame music, just download your own music file, name it "game_music.aiff" and replace the old file (you may have to convert a .mp3 or .wav file to .aiff if downloaded in those formats, otherwise it won't work).

### Thank you
Thanks to Xiokraze for intitially making this project up and literaly building the program in the first place. I'm pretty sure I wouldn't have made it without him, and I kind of feel bad because he doesn't even know about me building upon his project. Link to his repo: https://github.com/Xiokraze/Python/tree/master/TypingGame.

Also thanks to you guys who downloaded the game, you're cool.
