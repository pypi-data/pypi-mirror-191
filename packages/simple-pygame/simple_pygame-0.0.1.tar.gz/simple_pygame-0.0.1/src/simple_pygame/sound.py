import os
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"

import pygame, moviepy.editor, time

class Sound:
    def __init__(self, path: str, channel: int = 0, bit_depth: int = 4) -> None:
        """
        A sound read from a file contains audio. This class is mainly used to load and play sound from video.

        Parameters
        ----------

        path: Path to the file contains audio.

        channel: Channel id for playing the sound. The id must be a value from 0 to the value of `pygame.mixer.get_num_channels()`.

        bit_depth: Bit depth to encode the audio.
        - 1 for 8-bit sound.
        - 2 for 16-bit sound.
        - 4 for 32-bit sound.

        Requirements
        ------------
        
        - Pygame.
        - MoviePy.
        """
        self.path = path
        self.bit_depth = bit_depth
        self.digit = 2
        self.is_pausing = False

        self.channel = pygame.mixer.Channel(channel)

        self.audio = moviepy.editor.AudioFileClip(path)
        self.sound = self.make_sound(self.audio, self.audio.fps, self.bit_depth)

    def make_sound(self, audio: moviepy.editor.AudioFileClip, sample_rate: int = None, bit_depth: int = 4) -> pygame.mixer.Sound:
        """
        Transform the audio into a sound. This function is meant for use by the `Class` and not for general use.

        Parameters
        ----------

        audio: `AudioFileClip` to transform.

        sample_rate: Sample rate of the audio for the conversion.
        - None for original audio sample rate.

        bit_depth: Bit depth to encode the audio.
        - 1 for 8-bit sound.
        - 2 for 16-bit sound.
        - 4 for 32-bit sound.
        """
        array = audio.to_soundarray(fps = sample_rate, nbytes = bit_depth, quantize = True)
        sound = pygame.sndarray.make_sound(array)
        return sound
    
    def play(self) -> None:
        """
        Play the sound. If a sound is current playing it will be restarted.
        """
        self.channel.play(self.sound)
        self.start = time.time_ns()

        self.offset = 0
        self.pause_time = 0
        self.start_pause = False
        self.is_pausing = False
    
    def pause(self) -> None:
        """
        Pause the sound if it's current playing and not paused. It can be resumed with `unpause()` function.
        """
        if self.get_busy() and not self.is_pausing:
            self.channel.pause()
            self.start_pause = time.time_ns()

            self.is_pausing = True
    
    def unpause(self) -> None:
        """
        Resume the sound after it has been paused.
        """
        if self.get_busy() and self.is_pausing:
            self.channel.unpause()

            self.pause_time += time.time_ns() - self.start_pause
            self.start_pause = False
            self.is_pausing = False
    
    def stop(self) -> None:
        """
        Stop the sound if it's current playing.
        """
        self.channel.stop()

        self.is_pausing = False
    
    def set_position(self, position: float) -> None:
        """
        Set the current sound position where the sound will continue to play. It function also works like the `play()` function.

        Parameters
        ----------

        position: Where to set the sound position in seconds.
        """
        is_pausing = self.is_pausing

        if is_pausing:
            self.unpause()
        self.stop()

        if position <= 0:
            self.play()

            if is_pausing:
                self.pause()
        elif position >= self.get_length():
            self.stop()
        else:
            sound = self.make_sound(self.audio.cutout(0, position), self.audio.fps, self.bit_depth)
            
            self.channel.play(sound)
            self.start = time.time_ns()

            self.offset = position * 1000000000
            self.pause_time = 0
            self.start_pause = False
            self.is_pausing = False

            if is_pausing:
                self.pause()
    
    def get_position(self) -> float:
        """
        Return the current sound position.
        """
        if self.get_busy():
            if self.start_pause:
                return self.nanoseconds_to_seconds(self.pause_time + self.offset + self.start_pause - self.start)
            else:
                return self.nanoseconds_to_seconds(time.time_ns() - self.start - self.pause_time + self.offset)
        else:
            return -1
    
    def set_volume(self, volume: float) -> None:
        """
        Set the current channel volume.

        Parameters
        ----------

        volume: Channel volume.
        """
        if volume >= 0 and volume <= 1:
            self.channel.set_volume(volume)

    def get_volume(self) -> float:
        """
        Return the current channel volume.
        """
        return self.channel.get_volume()
    
    def get_busy(self) -> bool:
        """
        Return `True` if the channel is current playing or pausing, otherwise `False`.
        """
        return self.channel.get_busy()

    def get_length(self) -> float:
        """
        Return the total sound length.
        """
        return round(self.sound.get_length(), self.digit)

    def nanoseconds_to_seconds(self, time: float) -> float:
        """
        Convert nanoseconds to seconds. It's meant for use by the `Class` and not for general use.

        Parameters
        ----------

        time: Time in nanoseconds.
        """
        return round(time / 1000000000, self.digit)