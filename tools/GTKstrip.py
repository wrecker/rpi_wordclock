# coding: utf8

import threading
import gi
gi.require_version("Gtk", "3.0")
gi.require_version("Pango", "1.0")

from gi.repository import Gtk, Gdk, GLib, Pango

import os
from interfaces import event_handler as weh

FILL = Gtk.AttachOptions.FILL

class Color:
    def __init__(self, r, g, b):
        self.r = r
        self.g = g
        self.b = b

    def __clamp(self, x):
        return max(0, min(x, 255))

    def rgb_string(self):
        return "#{0:02x}{1:02x}{2:02x}".format(self.__clamp(self.r),
                self.__clamp(self.g), self.__clamp(self.b))


class GTKstrip(threading.Thread):
    def __init__(self, weh):
        super(GTKstrip, self).__init__()
        self.label = "GTKstrip"

        #chars = "ESKISTLFUNFZEHNZWANZIGDREIVIERTELTGNACHVORJMHALBQZWOLFPZWEINSIEBENKDREIRHFUNFELFNEUNVIERWACHTZEHNRSBSECHSFMUHR...."

        chars = "THE##TIME##IS####ABOUT###TEN##FIFTEEN##FORTY#TWENTY#THIRTY##FIFTY##FIVE#####MINUTES##PAST#ONE#TWO##THREE#FOURFIVE#ELEVEN#EIGHT#NINE#TENSIX#SEVENTWELVE#OCLOCK##AM#PM#TIME##TO##FOR##COFFEELUNCH#TEAWHISKEY#GO#HOMEAWAKE"

        self.labels = []
        self.colors = []
        self.brightness = 180

        self.weh = weh

        self.markup = '<span font="monospace Normal 32" foreground="{0}" background="#000000">!</span>'

        #self.win = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.win = Gtk.Window()

        self.win.connect("delete_event", self.delete_event)
        self.win.connect("destroy", self.destroy)
        self.win.connect("key_press_event", self.key_press_event)

        #table = gtk.Table(11, 11, True)
        table = Gtk.Table(n_rows=15, n_columns=15, homogeneous=True)
        table.set_col_spacings(35)
        table.modify_bg(Gtk.StateFlags.NORMAL, Gdk.color_parse("#000000"))
        table.set_margin_top(30)
        table.set_margin_left(30)
        table.set_margin_right(30)
        table.set_margin_bottom(15)
        
        x = 0
        y = 0
        for i in unicode(chars):
            #label = gtk.Label(i)
            label = Gtk.Label(label=i)
            self.labels.append(label)
            self.colors.append(Color(0, 0, 0))

            table.attach(label, x, x + 1, y, y + 1, FILL, FILL)

            x += 1
            if x == 15:
                x = 0
                y += 1

            #attrs = pango.AttrList()
            # attrs.insert(pango.AttrLanguage("de"))
            #attrs.insert(pango.AttrForeground(0, 0, 0))
            #attrs.insert(pango.AttrSize(30 * 1000))
            #attrs.insert(pango.AttrBackground(0, 0, 0))

            markup = self.markup.format("#340000")
            attrs = Pango.parse_markup(markup, len(markup), "0")[1]
            label.set_attributes(attrs)
            label.show()

        color = Gdk.color_parse('#000000')
        self.win.modify_bg(Gtk.StateFlags.NORMAL, color)
        self.win.add(table)
        self.win.show_all()
        self.labels.reverse()
        self.colors.reverse()

    def key_press_event(self, widget, event):
        if event.keyval == 65361:
            self.weh.setEvent(weh.event_handler.EVENT_BUTTON_LEFT)
        elif event.keyval == 65363:
            self.weh.setEvent(weh.event_handler.EVENT_BUTTON_RIGHT)
        elif event.keyval == 65362:
            self.weh.setEvent(weh.event_handler.EVENT_BUTTON_RETURN)

    def delete_event(self, widget, event, data=None):
        return False

    def destroy(self, widget, data=None):
        Gtk.main_quit()

    def run(self):
        Gtk.main()
        os._exit(1)

    def begin(self):
        self.start()

    def setPixelColor(self, index, color):
        self.colors[index] = color

    def getBrightness(self):
        return self.brightness

    def setBrightness(self, brightness):
        self.brightness = brightness
        print "Set mock brightness value to " + str(self.brightness)

    def update(self):
        for label, color in zip(self.labels, self.colors):
            #attrs = label.get_attributes()
            #attrs.change(pango.AttrForeground(int(color.r / 255.0 * 65535), int(color.g / 255.0 * 65535),
            #                                  int(color.b / 255.0 * 65535)));

            markup = self.markup.format(color.rgb_string())
            attrs = Pango.parse_markup(markup, len(markup), "0")[1]
            label.set_attributes(attrs)

    def show(self):
        #gobject.idle_add(self.update)
        GLib.idle_add(self.update)
