import re
from pydub import AudioSegment

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
    startTime = 0
    endTime = 0
    audio_title = ''

    def __init__(self, author, sentence, startTime, endTime, audio_title):
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
        self.audio_title = audio_title
        self.startTime = startTime
        self.endTime = endTime
  
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
        t1 = float(self.startTime) * 1000
        t2 = float(self.endTime) * 1000
        newAudio = AudioSegment.from_wav(source_path)
        newAudio = newAudio[t1:t2]
        newAudio = newAudio.set_frame_rate(22050)
        newAudio = newAudio.set_channels(1)
        return newAudio.export(destination_path + '/' + self.audio_title + '.wav', format="wav")

    def duration(self):
        """
        Calculates the duration of the sentence given the start and end time.
        
        Returns
        ----------
        the duration of the file.

        """ 
        return (float(self.endTime) - float(self.startTime))

    def debug_print(self):
      print("Sentence: " + self.sentence + "\n" 
            + "start time: " + self.startTime + "\n"
            + "end time: " + self.endTime)
