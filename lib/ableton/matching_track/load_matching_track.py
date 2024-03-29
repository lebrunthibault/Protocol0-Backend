from api.client.p0_script_api_client import p0_script_client
from api.settings import DOWN_BBOX
from lib.ableton.interface.track import get_focused_track_coords
from lib.ableton_set import AbletonSet
from lib.explorer import drag_file_to
from lib.mouse.mouse import keep_mouse_position
from protocol0.application.command.EmitBackendEventCommand import (
    EmitBackendEventCommand,
)


@keep_mouse_position
def drag_matching_track(set: AbletonSet):
    track_path = f"{set.tracks_folder}\\{set.current_track.name}.als"
    drag_file_to(
        track_path,
        get_focused_track_coords(),
        bbox=DOWN_BBOX,
        drag_duration=0.5,
        close_window=False,
    )
    p0_script_client().dispatch(EmitBackendEventCommand("matching_track_loaded"))
