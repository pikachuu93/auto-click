import win32api, win32gui, win32con
import time

class Window:
    def __init__(self, **kwargs):
        if "handle" in kwargs:
            self.handle = kwargs["handle"]
        elif "title" in kwargs:
            self.handle = self.getHandle(kwargs["title"])
        else:
            raise RuntimeError("No window info supplied")

        if not self.handle:
            raise RuntimeError("No window handle.")

        self.getGeometry()

    def getHandle(self, title):
        return win32gui.FindWindow(None, title)

    def getGeometry(self):
        self.rect   = win32gui.GetWindowRect(self.handle)
        self.width  = self.rect[2] - self.rect[0]
        self.height = self.rect[3] - self.rect[1]

        self.x = self.rect[0]
        self.y = self.rect[1]

    def click(self, x, y, timeout=0.1):
        pos = win32api.MAKELONG(x + self.x, y + self.y)

        win32gui.PostMessage(self.handle, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, pos)
        print(win32api.GetLastError());
        
        time.sleep(timeout)

        win32gui.PostMessage(self.handle, win32con.WM_LBUTTONUP, 0, pos)

    def getChildren(self):
        windows = []
        def go(handle, param):
            windows.append(Window(handle=handle))
            return True

        try:
            win32gui.EnumChildWindows(self.handle, go, None)
        except:
            pass

        return windows
