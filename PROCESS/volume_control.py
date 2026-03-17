from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

class VolumeController:
    def __init__(self):
        devices = AudioUtilities.GetSpeakers()
        activation = devices._dev.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        self.volume = cast(activation, POINTER(IAudioEndpointVolume))

    def set_volume(self, level):
        level = max(0.02, min(1.0, level))
        self.volume.SetMasterVolumeLevelScalar(level, None)

    def get_volume(self):
        return self.volume.GetMasterVolumeLevelScalar()

    def mute(self):
        self.volume.SetMute(1, None)

    def unmute(self):
        self.volume.SetMute(0, None)

    def is_muted(self):
        return self.volume.GetMute()