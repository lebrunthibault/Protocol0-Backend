import os

from pydantic import BaseSettings

LEFT_BBOX = (0, 0, 1100, 1080)
RIGHT_BBOX = (960, 0, 1920, 1080)
DOWN_BBOX = (660, 300, 1920, 1080)


class Settings(BaseSettings):
    class Config:
        env_file = ".env"

    user_home: str
    ableton_version: str

    @property
    def ableton_major_version(self) -> str:
        return self.ableton_version.split(".")[0]

    @property
    def log_file(self) -> str:
        return f"{self.user_home}\\AppData\\Roaming\\Ableton\\Live {self.ableton_version}\\Preferences\\Log.txt"

    project_directory = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))

    @property
    def ableton_exe(self) -> str:
        return f"C:\\ProgramData\\Ableton\\Live {self.ableton_major_version} Suite\\Program\\Ableton Live {self.ableton_major_version} Suite.exe"

    @property
    def ableton_process_name(self) -> str:
        return f"Ableton Live {self.ableton_major_version} Suite.exe"

    @property
    def preferences_directory(self) -> str:
        return f"{self.user_home}\\AppData\\Roaming\\Ableton\\Live {self.ableton_version}\\Preferences"

    @property
    def crash_directory(self) -> str:
        return f"{self.preferences_directory}\\Crash"

    ableton_set_directory: str
    ableton_test_set_path = "D:\\ableton projects\\tracks\\Toto\\Toto.als"
    ableton_default_set = "Default.als"

    http_api_url = "http://127.0.0.1:8000"

    rev2_editor_window_title = "REV2Editor/m"
    tracks_folder = "tracks"
    instrument_tracks_folder = "instruments\\default"
    log_window_title = "logs terminal"

    # Midi port names are relative to the Protocol0 script and not this midi backend
    p0_output_port_name = "P0_OUT"
    p0_input_port_name = "P0_IN_MIDI"
    p0_input_from_http_port_name = "P0_IN_HTTP"
    p0_backend_loopback_name = "P0_BACKEND_LOOPBACK"

    # 1 is 1080p, 2 is 4K
    display_resolution_factor = 1
