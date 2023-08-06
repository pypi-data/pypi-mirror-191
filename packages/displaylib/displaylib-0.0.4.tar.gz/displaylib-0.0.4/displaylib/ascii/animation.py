import os
from typing_extensions import Self
from ..template import Node
from .types import ModeFlags, ASCIISurface


__all__ = [
    "Frame",
    "Animation",
    "EmptyAnimation",
    "AnimationPlayer"
]


class Frame:
    def __init__(self, fpath: str) -> None:
        f = open(fpath)
        self.content = []
        for line in f.readlines():
            self.content.append(list((line.rstrip("\n"))))
        f.close()


class Animation:
    __slots__ = ("frames")
    def __init__(self, path: str, reverse: bool = False) -> None:
        fnames = os.listdir(path)
        step = 1 if not reverse else -1
        self.frames = [Frame(os.path.join(path, fname)) for fname in fnames][::step]


class EmptyAnimation(Animation):
    def __init__(self) -> None:
        self.frames = []


class AnimationPlayer(Node): # TODO: add buffered animations on load
    FIXED = 0 # TODO: implement FIXED and DELTATIME mode
    # DELTATIME = 1

    def __init__(self, owner: Self | None = None, fps: float = 16, /, mode: ModeFlags = FIXED, **animations) -> None:
        super().__init__(owner=None, x=0, y=0, z_index=0, force_sort=False) # TODO: change Node.owner --> Node.parent
        self.owner = owner
        self.fps = fps
        self.mode = mode # process mode (FIXED | DELTATIME)
        self.animations: dict[Animation] = dict(animations)
        self._animation = EmptyAnimation()
        self.is_playing = False
        self._current_frames = None
        self._next = None
        self._has_updated = False # indicates if the first frame (per animation) have been displayed
        self._accumulated_time = 0.0
        # -- dummy variables
        self.visible = False
        self.content = []
    
    def __iter__(self):
        return self

    def __next__(self) -> Frame:
        try:
            self._next = next(self._current_frames) # next of generator
            return self._next
        except StopIteration:
            self.is_playing = False
            self._current_frames = None
            self._next = None
            return None

    @property    
    def animation(self) -> Animation:
        return self._animation
    
    @animation.setter
    def animation(self, animation: str) -> None:
        self._animation = self.animations[animation]
        # make generator
        self._current_frames = (frame for frame in self._animation.frames)
        try:
            self._next = next(self._current_frames)
        except StopIteration:
            self.is_playing = False
            self._current_frames = None
            self._next = None
    
    def add(self, name: str, animation: Animation) -> None:
        self.animations[name] = animation
    
    def remove(self, name: str) -> None:
        del self.animations[name]
    
    def play(self, animation: str) -> None:
        """Plays an animation given the name of the animation

        Args:
            animation (str): the name of the animation to play
        """
        self.is_playing = True
        self._animation = animation
        self._current_frames = (frame for frame in self.animations[self.animation].frames)
        try:
            self._next: Frame = next(self._current_frames)
        except StopIteration:
            self.is_playing = False
            self._current_frames = None
            self._next: Frame = None
        if self._next != None:
            self.owner.content = self._next.content
            self._has_updated = False
    
    def play_backwards(self, animation: str) -> None:
        """Plays an animation backwards given the name of the animation

        Args:
            animation (str): the name of the animation to play backwards
        """
        self.is_playing = True
        self._animation = animation
        # reverse order frames
        self._current_frames = (frame for frame in reversed(self.animations[self.animation].frames))
        try:
            self._next: Frame = next(self._current_frames)
        except StopIteration:
            self.is_playing = False
            self._current_frames = None
            self._next: Frame = None
        if self._next != None:
            self.owner.content = self._next.content
            self._has_updated = False
        
    def advance(self) -> bool:
        """Advances 1 frame

        Returns:
            bool: whether it was NOT stopped
        """
        if self._current_frames == None:
            return False
        frame = self._next
        try:
            self._next = next(self._current_frames)
        except StopIteration:
            self.is_playing = False
            self._current_frames = None
            self._next = None
        if frame != None:
            self.owner.content = frame.content
            self._has_updated = False
        return frame != None # returns true if not stopped


    def stop(self) -> None:
        """Stops the animation from playing
        """
        self.is_playing = False

    def _render(self, surface: ASCIISurface) -> None: # dummy method
        return

    def _update(self, delta: float) -> None:
        if self.is_playing and self._has_updated:
            # if self.mode == AnimationPlayer.FIXED:
            frame = next(self)
            if frame == None:
                return
            self.owner.content = frame.content

            # elif self.mode == AnimationPlayer.DELTATIME:
            #     # apply delta time
            #     self._accumulated_time += delta
            #     if self._accumulated_time >= self._fps_ratio:
            #         self._accumulated_time -= self._fps_ratio # does not clear time
            #         frame = next(self)
            #         self.owner.content = frame.content
        self._has_updated = True
