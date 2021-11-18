import re
from pydub import AudioSegment
from silence_audio import vad_collector, frame_generator, read_wave, write_wave, webrtcvad
import os

class Audio_Sentence:
    """
    A class used to represent a sentence associated to an audio file with a particular start and end time.

    Attributes
    ----------
    author : str
        the name of the author that is pronuncing the sentence.
    audio_title : str
        a string that represent the title of the audio that you want to export.
    start_time : double
        a double that represents the exact moment in which the author is starting pronuncing the sentence(default 0.0).
    end_time : double
        a double that represents the exact moment in which the author is starting pronuncing the sentence(default 0.0). 

    Methods
    -------
    write_audiosentence(source_path, destination_path)
    
    Writes the .wav audio file to the assigned destination_path. The audio at the source_path will be extracted at the defined start and end time. The audio will be exported to the given path with the audio_title name '.wav'.
    
    duration()
    Calculates the duration of the sentence given the start and end time.
        
    """
    author = ''
    sentence = ''
    start_time = 0
    end_time = 0
    audio_title = ''

    def __init__(self, author, sentence, start_time, end_time, audio_title):
        """
        Parameters
        ----------
        author : str
        the name of the author that is pronuncing the sentence.
        audio_title : str
        a string that represent the title of the audio that you want to export.
        start_time : double
        a double that represents the exact moment in which the author is starting pronuncing the sentence(default 0.0).
        end_time : double
        a double that represents the exact moment in which the author is starting pronuncing the sentence(default 0.0). 
        """
        self.author = author
        self.sentence = sentence
        self.start_time = start_time
        self.end_time = end_time
        self.audio_title = audio_title
  
    def write_audiosentence(self, source_path, destination_path):
        """
        Writes the .wav audio file to the assigned destination_path. The audio at the source_path will be extracted at the defined start and end time. The audio will be exported to the given path with the audio_title name '.wav'.
        
        Parameters
        ----------
        source_path : str
        the path of the source audio.
        destination_path : str
        the path to assign to the extracted audio.

        Returns
        ----------
        an audio file.

        """        
        t1 = float(self.start_time) * 1000
        t2 = float(self.end_time) * 1000
        new_audio = AudioSegment.from_wav(source_path)
        new_audio=new_audio[t1:t2]
        new_audio = new_audio.set_frame_rate(32000)
        new_audio = new_audio.set_channels(1)
        new_audio = new_audio.set_sample_width(2)

        # trimming first and last silences.
        start_trim = self.detect_silence(new_audio)
        end_trim = self.detect_silence(new_audio.reverse())
        duration = len(new_audio)    
        trimmed_sound = new_audio[start_trim:duration-end_trim]
        trimmed_sound.export('tmp.wav', format='wav')

        audio, sample_rate = read_wave('tmp.wav')
        vad = webrtcvad.Vad(3)
        frames = frame_generator(30, audio, sample_rate)
        frames = list(frames)
        segments = vad_collector(sample_rate, 30, 300, vad, frames)

    # Segmenting the Voice audio and save it in list as bytes
        concataudio = [segment for segment in segments]
        joinedaudio = b"".join(concataudio)
        if os.path.exists('tmp.wav'):
            os.remove('tmp.wav')
        write_wave(destination_path + '/' + self.audio_title + '.wav', joinedaudio, sample_rate)
    
    def detect_silence(self, sound, silence_threshold=-50.0, chunk_size=10) -> float:
        """
        sound is a pydub.AudioSegment
        silence_threshold in dB
        chunk_size in ms

        iterate over chunks until you find the first one with sound
        """
        trim_ms = 0 # ms

        assert chunk_size > 0 # to avoid infinite loop
        while sound[trim_ms:trim_ms+chunk_size].dBFS < silence_threshold and trim_ms < len(sound):
            trim_ms += chunk_size

        return trim_ms

    def duration(self):
        """
        Calculates the duration of the sentence given the start and end time.
        
        Returns
        ----------
        the duration of the file.

        """ 
        return (float(self.end_time) - float(self.start_time))

    def debug_print(self):
      print("Sentence: " + self.sentence + "\n" 
            + "start time: " + self.start_time + "\n"
            + "end time: " + self.end_time)
