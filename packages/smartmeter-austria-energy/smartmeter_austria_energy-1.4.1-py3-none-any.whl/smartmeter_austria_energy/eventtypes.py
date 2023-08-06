"""Defines several objects around events."""


class EventArgs():
    None


class DerivedEventArgs(EventArgs):
    def __init__(self, speed: int) -> None:
        self._is_derived = False
        self._speed = speed

    @property
    def is_derived(self):
        return self._is_derived

    @is_derived.setter
    def is_derived(self, new_is_derived):
        self._is_derived = new_is_derived

    @property
    def Speed(self) -> int:
        return self._speed

    @Speed.setter
    def Speed(self, new_speed):
        self._speed = new_speed


class Event(object):
    def __init__(self):
        self.handlers = []

    def add(self, handler):
        self.handlers.append(handler)
        return self

    def remove(self, handler):
        self.handlers.remove(handler)
        return self

    def notify(self, sender, args : EventArgs = None) -> None:
        for handler in self.handlers:
            handler(sender, args)

    __iadd__ = add
    __isub__ = remove
    __call__ = notify
