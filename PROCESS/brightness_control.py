import screen_brightness_control as sbc

class BrightnessController:
    def set_brightness(self, level):
        # level 0 to 100
        level = max(2, min(100, level))
        sbc.set_brightness(level)

    def get_brightness(self):
        return sbc.get_brightness(display=0)