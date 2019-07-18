# pocketUSOS
pocketUSOS is an unofficial communication and integration client for polish student system "USOS". Program was fully writen in Python3 and integrated with Qt interface by PyQt5 project.

**!IMPORTANT:** This application is no longer in development and may not work with current version of USOS Web application.

### Features
- program is divided to modules (new ones can be added with easy) and base code
- you can login to and logout from USOS services
- dynamic interface build up on Qt
- you can check your grades and automatically calculate the average of them
- you can check and download (as png image) schedule of your courses

### Dependencies
Application include several dependencies that are needed to run this program.
###### Python-3.*
Program is fully writen in python so you will need Python version 3 or higher to run or compile it to binary form
You can download Python3 from it [official site](https://www.python.org/).

###### PyQt5
This wrapper is needed to build pocketUSOS interface with Qt. If you had Python3 installed and you have it in your system path. Open your system console and write ```pip install pyqt5```

###### Requests
Requests library is needed to provide easy interface for creating requests to USOS and to handle sessions and cookies.
Similar to PyQt, write ```pip install requests``` in your system console.

###### Beautiful Soup
BS helps to find needed things in raw HTML code.
Similar to PyQt, write ```pip install bs4``` in your system console.

### How to use this program
Program can be started by command ```python pocketUSOS.py```

### Documentation
Documentation for older version of pocketUSOS is still available at ```tutorial_old``` folder.
