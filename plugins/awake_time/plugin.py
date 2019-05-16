import datetime
import os
import time
import tools.wordclock_colors as wcc
try:
    from rpi_ws281x import Color
except:
    from GTKstrip import Color

class plugin:
    """
    A class to display the current time (default mode).
    This default mode needs to be adapted to the hardware
    layout of the wordclock (the chosen stencil) and is
    the most essential time display mode of the wordclock.
    """

    def __init__(self, config):
        """
        Initializations for the startup of the current wordclock plugin
        """
        # Get plugin name (according to the folder, it is contained in)
        self.name = os.path.dirname(__file__).split('/')[-1]
        self.pretty_name = "Awake Wordclock"
        self.description = "Display the Awake Custom Wordclock"
        self.current_time = None
        self.developer_mode = config.getboolean('wordclock', 'developer_mode')

        try:
            self.typewriter = config.getboolean('plugin_' + self.name, 'typewriter')
        except:
            print(
            '  No typewriter-flag set for default plugin within the config-file. Typewriter animation will be used.')
            self.typewriter = True

        try:
            self.typewriter_speed = config.getint('plugin_' + self.name, 'typewriter_speed')
        except:
            self.typewriter_speed = 5
            print('  No typewriter_speed set for default plugin within the config-file. Defaulting to ' + str(
                self.typewriter_speed) + '.')

	try:
            self.purist = config.getboolean('plugin_time_default', 'purist')
        except:
            print('  No purist-flag set for default plugin within the config-file. Prefix will be displayed.')
            self.purist = False

        self.bg_color = wcc.BLACK  # default background color
        self.word_color = wcc.WHITE  # default word color
        self.minute_color = wcc.WHITE  # default minute color

        # Other color modes...
        self.color_modes = \
            [[wcc.BLACK, wcc.WWHITE, wcc.WWHITE],
             [wcc.BLACK, wcc.WHITE, wcc.WHITE],
             [wcc.BLACK, wcc.ORANGE, wcc.ORANGE],
             [wcc.BLACK, wcc.ORANGE, wcc.WWHITE],
             [wcc.BLACK, wcc.PINK, wcc.GREEN],
             [wcc.BLACK, wcc.RED, wcc.YELLOW],
             [wcc.BLACK, wcc.BLUE, wcc.RED],
             [wcc.BLACK, wcc.RED, wcc.BLUE],
             [wcc.YELLOW, wcc.RED, wcc.BLUE],
             [wcc.RED, wcc.BLUE, wcc.BLUE],
             [wcc.RED, wcc.WHITE, wcc.WHITE],
             [wcc.GREEN, wcc.YELLOW, wcc.PINK],
             [wcc.WWHITE, wcc.BLACK, wcc.BLACK],
             [wcc.BLACK, wcc.Color(30, 30, 30), wcc.Color(30, 30, 30)]]
        self.color_mode_pos = 0
        self.rb_pos = 0  # index position for "rainbow"-mode
        try:
            self.brightness_mode_pos = config.getint('wordclock_display', 'brightness')
        except:
            print(
                "WARNING: Brightness value not set in config-file: To do so, add a \"brightness\" between 1..255 to the [wordclock_display]-section.")
            self.brightness_mode_pos = 255
        self.brightness_change = 8

    def get_time(self):
        if not self.developer_mode:
            self.current_time = datetime.datetime.now()
        elif not self.current_time:
            self.current_time = datetime.datetime.now()
        else:
            self.current_time += datetime.timedelta(minutes=5)
        return self.current_time

    def run(self, wcd, wci):
        """
        Displays time until aborted by user interaction on pin button_return
        """
        # Some initializations of the "previous" minute
        prev_min = -1
        prev_second = -1
        prev_interval = -1
        while True:
            # Get current time
            #now = datetime.datetime.now()
            now = self.get_time()
            # Check, if a minute has passed (to render the new time)
            #if prev_min < now.minute:
            update_display = False
            if now.minute % 5 == 0:
                if prev_min != now.minute:
                    prev_min = now.minute
                    update_display = True
            else:
                current_interval = now.minute / 5
                if prev_interval != current_interval:
                    prev_interval = current_interval
                    update_display = True
            if update_display:
                self.show_time(wcd, wci)

            if prev_second != now.second:
                self.change_logo_color(wcd, wci)
                prev_second = now.second

            event = wci.waitForEvent(2)
            # Switch display color, if button_left is pressed
            if event == wci.EVENT_BUTTON_LEFT:
                self.color_mode_pos += 1
                if self.color_mode_pos == len(self.color_modes):
                    self.color_mode_pos = 0
                self.bg_color = self.color_modes[self.color_mode_pos][0]
                self.word_color = self.color_modes[self.color_mode_pos][1]
                self.minute_color = self.color_modes[self.color_mode_pos][2]
                self.show_time(wcd, wci)
                time.sleep(0.2)
            if (event == wci.EVENT_BUTTON_RETURN) \
                    or (event == wci.EVENT_EXIT_PLUGIN) \
                    or (event == wci.EVENT_NEXT_PLUGIN_REQUESTED):
                return
            if event == wci.EVENT_BUTTON_RIGHT:
                time.sleep(wci.lock_time)
                self.color_selection(wcd, wci)

    def show_time(self, wcd, wci):
        # now = datetime.datetime.now()
        now = self.current_time
        # Set background color
        wcd.setColorToAll(self.bg_color, includeMinutes=True)
        # Returns indices, which represent the current time, when beeing illuminated
        taw_indices = wcd.taw.get_time(now, self.purist)
        if self.typewriter and now.minute % 5 == 0:
            for i in range(len(taw_indices)):
                wcd.setColorBy1DCoordinates(wcd.strip, taw_indices[0:i + 1], self.word_color)
                wcd.show()
                time.sleep(1.0 / self.typewriter_speed)
            #wcd.setMinutes(now, self.minute_color)
            wcd.show()
        else:
            wcd.setColorBy1DCoordinates(wcd.strip, taw_indices, self.word_color)
            #wcd.setMinutes(now, self.minute_color)
            wcd.show()
        taw_indices = []
    
    def change_logo_color(self, wcd, wci):
        now = datetime.datetime.now()
        logo_indices = [210, 211, 212, 213, 214]
        # Inspired by the ColorClock OSX Screensaver
        # https://blog.edwardloveall.com/colorclocksaver | https://github.com/edwardloveall/colorclocksaver
        color = Color(int(round(256/23.0 * now.hour)), int(round(256/59.0 * now.minute)), int(round(256/59.0 * now.second)))
        wcd.setColorBy1DCoordinates(wcd.strip, logo_indices, color)
        wcd.show()

    def color_to_rgb(self, color):
        return "[%d:%d:%d]" % ((color >> 16) & 0xFF, (color >> 8) & 0xFF, color & 0xFF)

    def color_selection(self, wcd, wci):
        while True:
            # BEGIN: Rainbow generation as done in rpi_ws281x strandtest example! Thanks to Tony DiCola for providing :)
            if self.rb_pos < 85:
                self.word_color = self.minute_color = wcc.Color(3 * self.rb_pos, 255 - 3 * self.rb_pos, 0)
            elif self.rb_pos < 170:
                self.word_color = self.minute_color = wcc.Color(255 - 3 * (self.rb_pos - 85), 0, 3 * (self.rb_pos - 85))
            else:
                self.word_color = self.minute_color = wcc.Color(0, 3 * (self.rb_pos - 170),
                                                                255 - 3 * (self.rb_pos - 170))
            # END: Rainbow generation as done in rpi_ws281x strandtest example! Thanks to Tony DiCola for providing :)
            # TODO: Evaluate taw_indices only every n-th loop (saving resources)
            now = datetime.datetime.now()  # Set current time
            taw_indices = wcd.taw.get_time(now, self.purist)
            wcd.setColorToAll(self.bg_color, includeMinutes=True)
            wcd.setColorBy1DCoordinates(wcd.strip, taw_indices, self.word_color)
            wcd.setMinutes(now, self.minute_color)
            wcd.show()
            self.rb_pos += 1
            if self.rb_pos == 256: self.rb_pos = 0
            event = wci.waitForEvent(0.1)
            if event != wci.EVENT_INVALID:
                time.sleep(wci.lock_time)
                break
        while True:
            self.brightness_mode_pos += self.brightness_change
            # TODO: Evaluate taw_indices only every n-th loop (saving resources)
            now = datetime.datetime.now()  # Set current time
            taw_indices = wcd.taw.get_time(now, self.purist)
            wcd.setColorToAll(self.bg_color, includeMinutes=True)
            wcd.setColorBy1DCoordinates(wcd.strip, taw_indices, self.word_color)
            wcd.setMinutes(now, self.minute_color)
            wcd.setBrightness(self.brightness_mode_pos)
            wcd.show()
            if self.brightness_mode_pos < abs(self.brightness_change) or self.brightness_mode_pos > 255 - abs(
                    self.brightness_change):
                self.brightness_change *= -1
            event = wci.waitForEvent(0.1)
            if event != wci.EVENT_INVALID:
                time.sleep(wci.lock_time)
                return
