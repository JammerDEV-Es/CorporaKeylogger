# 📋 Instructions: 

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

### 3 - Now go to the directory where you have the .py file from the CMD and type the following:

#### On the CMD: <br> `pyinstaller --onefile --noconsole  'Corpora Keylogger.py`

Now you have the keylogger .exe file, the Python libraries are not needed, so a requirements.txt file is not necessary in this case.

# Extra Steps (Optional):

### 4 - Set service name 

### To increase the keylogger's credibility, we'll need to disguise it somehow so it goes unnoticed. The first step to avoid detection is to associate it with the name of any service that's active in Windows, like `WMI Provider Host`, `COM Surrogate`, or `runSW`.

<div align="center">
</div>
<img width="256" height="256" src="https://github.com/JammerDEV-Es/CorporaKeylogger/blob/main/Images/Services.png">
</p>
So rename the file to a service similar to those, otherwise, you can search your task manager for more common service names.

#

### 5 - Change Icon 

### And the last and most important step to avoid suspicion is to change the program's .ico file, which by default will look something like this if you entered the exact parameters in the command prompt regarding the pyinstaller.

<div align="center">
</div>
<img width="170" height="230" src="https://github.com/JammerDEV-Es/CorporaKeylogger/blob/main/Images/.ico.png">
</p>

And finally, it will be completely discreet; its consumption is not high, so it won't be immediately noticeable in the task manager.
