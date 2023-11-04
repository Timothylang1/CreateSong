AUDIO_FILE = "inputsongs/C Major Scale.wav"
# AUDIO_FILE = "inputsongs/Plain White T's - Hey There Delilah.wav"

# from pydub import AudioSegment
# sound = AudioSegment.from_file("inputsongs/Plain White T's - Hey There Delilah.wav")

# def speed_change(sound, speed=1.0):
#     # Manually override the frame_rate. This tells the computer how many
#     # samples to play per second
#     sound_with_altered_frame_rate = sound._spawn(sound.raw_data, overrides={
#         "frame_rate": int(sound.frame_rate * speed)
#     })

#     # convert the sound with altered frame rate to a standard frame rate
#     # so that regular playback programs will work right. They often only
#     # know how to play audio at standard frame rate (like 44.1k)
#     return sound_with_altered_frame_rate.set_frame_rate(sound.frame_rate)

# slow_sound = speed_change(sound, 0.75)
# slow_sound.export(out_f="outputsongs/test.wav", format="wav")


from scipy.io import wavfile
import librosa

print("Loading")
song, fs = librosa.load(AUDIO_FILE)
print("slowing")
song_2_times_slower = librosa.effects.time_stretch(y=song, rate=0.1)
print("writing")
wavfile.write("outputsongs/test3.wav", fs, song_2_times_slower) # save the song

