from pydub import AudioSegment
from pydub.playback import play


sound = AudioSegment.from_wav("Larks_Theme_Heheheha.wav")
play(sound)