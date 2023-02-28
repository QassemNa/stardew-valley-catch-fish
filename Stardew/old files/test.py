from ctypes.wintypes import LPCWSTR

import autoit
from autoit.autoit import AUTO_IT

button = "left"
AUTO_IT.AU3_MouseDown(LPCWSTR(button))
AUTO_IT.AU3_MouseUp(LPCWSTR(button))
#autoit.run("notepad.exe")
#autoit.win_wait_active("[CLASS:Notepad]", 3)
#autoit.control_send("[CLASS:Notepad]", "Edit1", "hello world{!}")
#autoit.win_close("[CLASS:Notepad]")
#autoit.control_click(title = "", control = "Button1")