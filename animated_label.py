"""Module introduces AnimatedLabel class which is the base for building
classes with different animations. AnimatedLabel itself contains no
specific animation effects and visually works as ordinary TextLabel.
Though it encapsulates self.progress attribute for keeping the status
of some continuous process."""
from text_label import TextLabel, DEFAULT_COLOR, DEFAULT_SIZE, TYPEFACE_NORMAL

DEFAULT_MAX_PROGRESS = 100

class AnimatedLabel(TextLabel):
    def __init__(self, scr, text='', color=DEFAULT_COLOR, size=DEFAULT_SIZE,
                 typeface=TYPEFACE_NORMAL):
        """The parameters are the same as for TextLabel."""
        super().__init__(scr, text, color, size, typeface)
        self.speed = 1
        self.max_progress = DEFAULT_MAX_PROGRESS
        self.repeat = True
        self._reset()

    def _reset(self):
        self.finished = False
        self.progress = 0

    def restart(self):
        """Forces the animation effect to start again."""
        self._reset()
        # This is needed for complete reset in child class instances
        self.update()
        self._reset()

    def update(self):
        """Respectively updates self.progress attribute."""
        if not self.finished:
            self.progress += self.speed
            if self.progress > self.max_progress:
                if self.repeat:
                    self.progress = 0
                else:
                    self.progress = self.max_progress
                    self.finished = True

    def set_speed(self, speed=1):
        """Sets the speed of animation effect. It means the increment
        for self.progress attribute.
        Input value should be positive float or int."""
        self.speed = speed

    def set_max_progress(self, max_progress=DEFAULT_MAX_PROGRESS):
        """Sets maximum value for self.progress attribute.
        Input value should be positive float or int."""
        self.max_progress = max_progress
        if self.progress > self.max_progress:
            if self.repeat:
                self.progress = 0
            else:
                self.progress = self.max_progress
                self.finished = True

    def set_repeat(self, repeat=True):
        """Changes 'repeat' parameter of the animation effect. If the
        animation has finished, then setting repeat to True will start
        it again."""
        self.repeat = repeat
        if self.finished and self.repeat:
            self.finished = False
