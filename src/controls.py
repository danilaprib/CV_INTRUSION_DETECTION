import sys

_IS_WINDOWS = sys.platform.startswith('win')

_VK = {
    'q': 0x51, 'p': 0x50, 'r': 0x52, 'f': 0x46,
    'j': 0x4A, 's': 0x53, 'z': 0x5A,
}

if _IS_WINDOWS:
    import ctypes

    _user32 = ctypes.windll.user32
    _user32.GetAsyncKeyState.restype = ctypes.c_short
    _user32.GetAsyncKeyState.argtypes = [ctypes.c_int]
    _user32.GetForegroundWindow.restype = ctypes.c_void_p
    _user32.FindWindowW.restype = ctypes.c_void_p
    _user32.FindWindowW.argtypes = [ctypes.c_wchar_p, ctypes.c_wchar_p]


class KeyPoller:
    def __init__(self, window_name):
        self.window_name = window_name
        self._down = {name: False for name in _VK}
        self._hwnd = None

    def poll(self, waitkey_code):
        if _IS_WINDOWS:
            return self._poll_windows()
        return self._poll_waitkey(waitkey_code)

    def _poll_windows(self):
        pressed = set()
        active = self._is_foreground()
        for name, vk in _VK.items():
            is_down = (_user32.GetAsyncKeyState(vk) & 0x8000) != 0
            if active and is_down and not self._down[name]:
                pressed.add(name)
            self._down[name] = is_down
        return pressed

    def _is_foreground(self):
        if not self._hwnd:
            self._hwnd = _user32.FindWindowW(None, self.window_name)
        if not self._hwnd:
            return True
        return _user32.GetForegroundWindow() == self._hwnd

    @staticmethod
    def _poll_waitkey(code):
        if code is None or code < 0:
            return set()
        ch = chr(code & 0xFF)
        return {ch} if ch in _VK else set()
