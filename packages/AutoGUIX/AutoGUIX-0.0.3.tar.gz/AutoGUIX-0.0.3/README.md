AutoGUIX
========

AutoGUIX is an extended or improved version of PyAutoGUI. Currently, it is only available for Windows Platform.

```pip install pyautogui```

```pip install autoguix```

It uses the PyAutoGUI library. Some of the features of AutoGUIX are listed below:

* You can execute the actions based on the window title till the window is active.
* You can get control over your commands which you want to execute.
* You can send a SIGINT signal in PuTTY.
* You can close the applications.
* You can get the window application coordinates.
* You can open the applications via RUN Dialog Box.

There above features are not available in PyAutoGUI. You can use AutoGUIX for automating the tasks in Windows Platform.

Example Usage
=============

```python
from AutoGUIX import AUTOGUIX as agx

# Open the Notepad application using RUN Dialog Box
agx.run_app(app_command = 'notepad', app_window_name_to_wait = 'Untitled - Notepad')

# Type the text in Notepad application
# The 'enter_command' function will also used to type the text in the application
agx.enter_command(command = 'Hello World', execute_command = False)

# Get the Notepad application coordinates
agx.get_position(window_name = 'Untitled - Notepad')

# Close the Notepad application
agx.close_app(window_name = 'Untitled - Notepad', executable_name = 'notepad.exe')
```
