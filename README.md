# GUI Application built with Tkinter and Tkmacosx for coloring.

## The goal of this application is to automatically sync all of my assignments and tests in Canvas onto my G-Mail calendar

### If you'd like to modify this please fork the repo and download the requirements.txt file as well.

### Prerequeistes before running the file
#### Creating a virtual enviroment and downloading the requirements.txt
python3 -m venv venv **<- This will create a virtual enviroment named "venv"**
<br> pip3 install -r requirements.txt **<- This installs all dependencies for the project**
#### Authorization for Google Cloud Project
As of now, any users not on the google cloud project that try to use this will fail because of authorization. This is because the project is till in test.
I haven't yet made this public, if you would like to use this please either open a PR asking to be added to the Google Cloud Project.

#### Once you have the folder and files downloaded, please navigate to that folder where the canvasGUI.py file is held and run the following 
**python3 canvasGUI.py**
<br>
<br> This should bring up the following <br>
![Image of CanvasGUI](https://drive.google.com/uc?export=view&id=14of1iN4-ugV3tGc65r9M6B5l_7ItbzZx)

### Documentation and tutorials
tkmacosx - https://github.com/Saadmairaj/tkmacosx#button-widget<br>
Google Calendar API - https://developers.google.com/calendar/api/guides/overview<br>
Tkinter tutorial - https://realpython.com/python-gui-tkinter/<br>
