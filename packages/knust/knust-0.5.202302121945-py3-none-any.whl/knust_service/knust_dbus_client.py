# The DBUS client class for the Knust service.

from pydbus import SessionBus, SystemBus
from knust_service.knust_dbus_service import KnustDbusService
from gi.repository import GLib, GObject

class KnustDBusClient():
    def __init__(self):
        self._bus = None
        self._proxy = None

    def connect(self, use_sessionbus):
        self._bus = SessionBus() if use_sessionbus else SystemBus()
        try:
            self._proxy = self._bus.get(KnustDbusService.KnustDbusServiceName)
        except GLib.Error as e:
            raise RuntimeError('Unable to connect to service: {}. Is this the correct bus?'.format(str(e)))

    def status(self):
        assert self._proxy != None
        reply = self._proxy.Status()
        return reply

    def add_session(self, target_temp, duration):
        assert self._proxy != None
        reply = self._proxy.AddSession(target_temp, duration)
        return reply

    def drop_session(self):
        assert self._proxy != None
        reply = self._proxy.DropSession()
        return reply

    def quit(self):
        assert self._proxy != None
        reply = self._proxy.Quit()
        return reply

if __name__ == '__main__':
    client = KnustDBusClient()
    client.connect(True)
    print(client.status())
