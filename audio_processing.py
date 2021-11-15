import moviepy.editor as mp
import subprocess

def extract_audio(videoName):
    subprocess.run( #converts the webm to wav using ffmpeg
        (['ffmpeg', '-y', '-i', videoName, 'audio.wav']))