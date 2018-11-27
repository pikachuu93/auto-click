import win32api, win32gui, win32con, win32ui
import numpy as np
from matplotlib import pyplot as plt
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
        self.pixels = None

    def getHandle(self, title):
        return win32gui.FindWindow(None, title)

    def getGeometry(self):
        self.rect   = win32gui.GetWindowRect(self.handle)
        self.width  = self.rect[2] - self.rect[0]
        self.height = self.rect[3] - self.rect[1]

        self.x = self.rect[0]
        self.y = self.rect[1]

    def click(self, x, y, timeout=0.01, right=False):
        win32gui.PostMessage(self.handle, win32con.WM_ACTIVATE, 0, 0)

        pos = win32api.MAKELONG(x + self.x, y + self.y)

        if right:
            down = win32con.WM_RBUTTONDOWN
            button = win32con.MK_RBUTTON
            up = win32con.WM_RBUTTONUP
        else:
            down = win32con.WM_LBUTTONDOWN
            button = win32con.MK_LBUTTON
            up = win32con.WM_LBUTTONUP

        win32gui.PostMessage(self.handle, win32con.WM_MOUSEMOVE, 0, pos)
        time.sleep(0.1)
        win32gui.PostMessage(self.handle, down, 0, pos)
        time.sleep(0.01)
        win32gui.PostMessage(self.handle, up, button, pos)

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

    def getContent(self):
        self.getGeometry()
        hwindc = win32gui.GetWindowDC(self.handle)

        srcdc = win32ui.CreateDCFromHandle(hwindc)
        memdc = srcdc.CreateCompatibleDC()
        bmp = win32ui.CreateBitmap()
        bmp.CreateCompatibleBitmap(srcdc, self.width, self.height)
        memdc.SelectObject(bmp)
        memdc.BitBlt((0, 0), (self.width, self.height), srcdc, (0, 0), win32con.SRCCOPY)

        # bmp.SaveBitmapFile(memdc, "output.bmp")

        bits = bmp.GetBitmapBits(True)

        srcdc.DeleteDC()
        memdc.DeleteDC()
        win32gui.ReleaseDC(self.handle, hwindc)
        win32gui.DeleteObject(bmp.GetHandle())

        self.pixels = bits
