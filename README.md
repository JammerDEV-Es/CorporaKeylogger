# Corpora Keylogger

### This project is a keylogger that reports to your Telegram bot. I've tried to polish it as much as possible. I've been working on it for months, and now the most polished version is the one I'll publish.
#
If you have ever used a keylogger, you know that the text reports all keystrokes in a raw format like `[CAPSLOCK]`, `[SPACE]`, `[BACKSPACE]`. This is a problem that will no longer occur with this keylogger.

#

## First version: 
This is the first keylogger version that shows raw info.

<div align="center">
</div>
<img width="400" height="400" src="https://github.com/JammerDEV-Es/CorporaKeylogger/blob/main/Images/FirstVersion.jpg">
</p>

#

## Actual Version:
This is the version that doesn't show a raw format and embellishes it so that all the information is clear.


<div align="center">
</div>
<img width="400" height="400" src="https://github.com/JammerDEV-Es/CorporaKeylogger/blob/main/Images/LastVersion.jpg">
</p>

#

## Next, I will explain all the steps to carry it out and be able to use it correctly.

### 1- Edit the `.py` file with any editor and replace the following characters. <br>
Specifically the placeholder in the line 15 and 16.
<div align="center">
</div>
<img width="512" height="512" src="https://github.com/JammerDEV-Es/CorporaKeylogger/blob/main/Images/Placeholder.png">
</p>

#

### 2- Now that you've entered your user ID and bot token, the next thing you'll need to do (if you're using Windows) is download PyInstaller from your command prompt. This is used to convert .py files to .exe files.
#### On the CMD: <br> `pip install pyinstaller`

#

### 3- Now go to the directory where you have the .py file from the CMD and type the following:

#### On the CMD: <br> `pyinstaller --onefile --noconsole  'Corpora Keylogger.py`

Now you have the keylogger .exe file, the Python libraries are not needed, so a requirements.txt file is not necessary in this case.

# Extra Steps (Optional):

### 5- To increase the keylogger's credibility, we'll need to disguise it somehow so it goes unnoticed. The first step to avoid detection is to associate it with the name of any service that's active in Windows, like `WMI Provider Host`, `COM Surrogate`, or `runSW`.

<div align="center">
</div>
<img width="256" height="256" src="https://github.com/JammerDEV-Es/CorporaKeylogger/blob/main/Images/Services.png">
</p>
So rename the file to a service similar to those, otherwise, you can search your task manager for more common service names.






