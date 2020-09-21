import dbus
import dbus.service

from gi.repository import GLib

BUS_NAME = 'com.canonical.AppMenu.Registrar'
BUS_PATH = '/com/canonical/AppMenu/Registrar'


class AppMenuService(dbus.service.Object):
  '''
    Types:
      - u: int
      - a: array
      - y: byte
      - s: string
      - o: DBus object path 
      - g: DBus type signature

    https://people.gnome.org/~ryanl/glib-docs/gvariant-format-strings.html
  '''
  def __init__(self):
    self.window_dict = dict()

    bus_name = dbus.service.BusName(BUS_NAME, bus=dbus.SessionBus())
    dbus.service.Object.__init__(self, bus_name, BUS_PATH)

  @dbus.service.method(BUS_NAME, in_signature='uo', sender_keyword='sender')
  def RegisterWindow(self, windowId, menuObjectPath, sender):
    self.window_dict[windowId] = [dbus.String(sender), dbus.ObjectPath(menuObjectPath)]

  @dbus.service.method(BUS_NAME, in_signature='u')
  def UnregisterWindow(self, windowId):
    if windowId in self.window_dict:
      del self.window_dict[windowId]

  @dbus.service.method(BUS_NAME, in_signature='u', out_signature='so')
  def GetMenuForWindow(self, windowId):
    if windowId in self.window_dict:
      return self.window_dict[windowId]

  @dbus.service.method(BUS_NAME)
  def GetMenus(self):
    return self.window_dict

  @dbus.service.method(BUS_NAME)
  def Q(self):
    GLib.MainLoop().quit()


class MyService(dbus.service.Object):

  BUS_PATH = '/com/gonzaarcr/appmenu'
  BUS_NAME = 'com.gonzaarcr.appmenu'

  def __init__(self):
    self.bus_name = dbus.service.BusName(self.BUS_NAME, bus=dbus.SessionBus())
    dbus.service.Object.__init__(self, self.bus_name, self.BUS_PATH)

  @dbus.service.signal(BUS_NAME, signature='s')
  def MenuActivated(self, menu):
    pass

  @dbus.service.method(BUS_NAME, in_signature='s')
  def EchoSignal(self, menu):
    self.MenuActivated(menu)
    return menu

  @dbus.service.method(BUS_NAME, in_signature='a{ss}')
  def WindowSwitched(self, window_data):
    self.WindowSwitchedSignal(window_data)

  @dbus.service.signal(BUS_NAME, signature='a{ss}')
  def WindowSwitchedSignal(self, window_data):
    pass