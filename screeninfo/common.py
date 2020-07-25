import enum


class Monitor:
    """Stores the resolution and position of a monitor."""

    def __init__(self, x, y, width, height, width_mm=None, height_mm=None, name=None):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.width_mm = width_mm
        self.height_mm = height_mm
        self.name = name

    def __repr__(self) -> str:
        return (
            f"Monitor("
            f"x={self.x}, y={self.y}, "
            f"width={self.width}, height={self.height}, "
            f"width_mm={self.width_mm}, height_mm={self.height_mm}, "
            f"name={self.name!r}"
            f")"
        )


class ScreenInfoError(Exception):
    pass


class Enumerator(enum.Enum):
    Windows = "windows"
    Cygwin = "cygwin"
    Xrandr = "xrandr"
    Xinerama = "xinerama"
    DRM = "drm"
    OSX = "osx"
