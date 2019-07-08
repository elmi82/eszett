from pychromecast.controllers.media import MediaStatus


class CastState(object):
    def __init__(self):
        self.content_id = None
        self.player_state = None
        self.idle_reason = None

        self.content_changed = False
        self.player_state_changed = False
        self.idle_reason_changed = False

    @property
    def has_changed(self) -> bool:
        return self.content_changed or self.player_state_changed or self.idle_reason_changed

    def reset_state(self):
        self.content_changed = False
        self.player_state_changed = False
        self.idle_reason_changed = False

    def set_to_status(self, status: MediaStatus):
        self.content_id = status.content_id
        self.player_state = status.player_state
        self.idle_reason = status.idle_reason

        self.reset_state()

    def update(self, status: MediaStatus):
        self.reset_state()

        if self.content_id is not status.content_id:
            self.content_changed = True
            self.content_id = status.content_id

        if self.player_state is not status.player_state:
            self.player_state_changed = True
            self.player_state = status.player_state

        if self.idle_reason is not status.idle_reason:
            self.idle_reason_changed = True
            self.idle_reason = status.idle_reason
