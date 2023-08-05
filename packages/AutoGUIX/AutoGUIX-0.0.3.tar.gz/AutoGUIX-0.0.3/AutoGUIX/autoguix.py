"""
AutoGUIX is an extended or improved version of PyAutoGUI.
Currently, it is only available for Windows Platform.
"""
import os
import re
import time
try:
    import pyautogui as pag
except ImportError as exc:
    raise ImportError('Please install the pyautogui module to use AutoGUIX') from exc
try:
    import pygetwindow as gw
except ImportError as exc:
    raise ImportError('Please install the pygetwindow module to use AutoGUIX') from exc


class ElementNotFound(Exception):
    """
    This exception is raised when the element is not found
    """

class AUTOGUIX:
    """
    AutoGUIX is an extended or improved version of PyAutoGUI.
    Currently, it is only available for Windows Platform.
    """
    @classmethod
    def wait_for_window(cls, window_name: str, default_time: int = None):
        """
        This function waits until the window is active and default time is 60 seconds

        Args:
            window_name (str): The window which need to be checked
            default_time (int, Optional): The max time to wait

        Returns:
            None
        """

        if default_time is None:
            wait_time = 60
        else:
            wait_time = default_time

        found_wait_time = 1
        start_time = time.time()

        while True:
            is_window_found = False
            end_time = time.time()
            total_time = int(end_time - start_time)
            if total_time >= wait_time:
                exception_message = f'The window - {window_name} not found within the limited time!'
                raise ElementNotFound(exception_message)

            try:
                if window_name in gw.getAllTitles():
                    is_window_found = True
            except ElementNotFound:
                # No exception will raise as gw.getAllTitles() is a list
                is_window_found = False

            if is_window_found:
                time.sleep(found_wait_time)
                break
            time.sleep(1)

    @classmethod
    def enter_command(cls, command: str, post_wait_time: int = 0,
        exit_execution: str = None, execute_command: bool = True):
        """
        This function enters the command and can wait for the specified time and
        can exit the execution. Useful in case of long running commands.

        Args:
            command (str): The command to be executed
            post_wait_time (int, optional): The time to wait after the command is executed.
                Defaults to None.
            exit_execution (str, optional): The command to exit the execution. Defaults to None.
            Acceptable formats are: STOP_10, STOP_20 etc. where 10 and 20 are the seconds to wait.
            execute_command (bool, optional): The flag to execute the command. Defaults to True.

        Returns:
            None

        Note:
            If the post_wait_time is Zero, then the default time is 2 seconds.
            If exit_execution must be less than the post_wait_time at least 2 seconds
            else automation 2 seconds will be added to the exit_execution time.
            If exit_execution format is not correct, then the exit_execution will be ignored.
        """
        for each_char in command:
            if each_char in "~!@#$%^&*)(_+}{:\"<>?|" or each_char.isupper():
                pag.keyDown('shift')
                pag.press(each_char)
                pag.keyUp('shift')
            else:
                pag.press(each_char)
            time.sleep(0.01)

        if execute_command:
            pag.press('enter')

        start_time = time.time()

        # POST TIME WAIT & EXIT EXECUTION
        # check exit_execution format using regex
        if post_wait_time == 0:
            time.sleep(2)
        time.sleep(post_wait_time)

        if exit_execution is not None:
            if re.match(r'^STOP_\d+$', exit_execution) is None:
                exit_execution = None

            exit_execution_time = int(exit_execution.split('_')[1])

            # check the exit_execution_time is less than post_wait_time
            if exit_execution_time is not None and post_wait_time is not None:
                if exit_execution_time < post_wait_time:
                    exit_execution_time = post_wait_time + 2

            while True:
                end_time = time.time()
                total_time = int(end_time - start_time)
                if total_time >= exit_execution_time:
                    # Exit the execution
                    pag.hotkey('ctrl', 'c')
                    break

    @classmethod
    def close_app(cls, window_name: str, executable_name: str = None):
        """
        Close the active application

        Args:
            window_name (str): The window name of the application
            executable_name (str, optional): The executable name of the application.
                Defaults to None.

        Returns:
            None or raise an exception if the window is not active
        """
        try:
            application_obj = gw.getWindowsWithTitle(window_name)[0]
            application_obj.close()
            time.sleep(1)
            pag.press('enter')
            if executable_name is not None:
                os.system(f"taskkill /f /im {executable_name}")
        except Exception as error:
            raise ElementNotFound(f"{window_name} is not active to close") from error

    @classmethod
    def get_position(cls, window_name: str):
        """
        Get the position of the application window

        Args:
            window_name (str): The window name of the application

        Returns:
            dict: The positions of the application window
            or raise an exception if the window is not active
        """
        try:
            cls.wait_for_window(window_name)
            application_obj = gw.getWindowsWithTitle(window_name)[0]
            positions = {
                "top": application_obj.top,
                "right": application_obj.right,
                "bottom": application_obj.bottom,
                "left": application_obj.left
            }
            return positions
        except Exception as error:
            raise ElementNotFound(f"{window_name} is not active to fetch it's position") from error

    @classmethod
    def sigint_signal(cls):
        """
        Ctrl + C is used to send a SIGINT signal, which cancels or terminates
        the currently-running program.

        Returns:
            None
        """
        pag.hotkey('ctrl', 'c')
        time.sleep(2)

    @classmethod
    def run_app(cls, app_command: str = None, app_window_name_to_wait: str = None,
                wait_run_window: bool = True):
        """
        This function opens the App via Run dialog box

        Args:
            app_command (str, optional): The command to be executed. Defaults to None.
            app_window_name_to_wait (str, optional): The window name to wait. Defaults to None.
            wait_run_window (bool, optional): Wait for the Run window to appear. Defaults to True.

        Returns:
            None
        """
        pag.hotkey('win', 'r')
        time.sleep(2)

        if wait_run_window:
            cls.wait_for_window('Run')

        cls.enter_command(app_command)

        if app_window_name_to_wait is not None:
            cls.wait_for_window(app_window_name_to_wait)

        time.sleep(2)
