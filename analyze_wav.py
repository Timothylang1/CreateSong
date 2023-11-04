import numpy as np
from scipy.io import wavfile # get the api
from mingus.core import chords

from decimal import Decimal


# Configuration
FPS = 8 # How many samples we take per second

MAX_NOTES = 6

# Names of the notes
NOTE_NAMES = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]

# Or download my sample audio
# AUDIO_FILE = "inputsongs/C Major Scale.wav"
AUDIO_FILE = "inputsongs/Plain White T's - Hey There Delilah.wav"
# AUDIO_FILE = "outputsongs/test3.wav"

fs, audio = wavfile.read(AUDIO_FILE) # load the data

# First, check if it's stereo or mono
try:
  audio = audio[:, 0] # Get left channel
except:
  pass

AUDIO_LENGTH = len(audio)/fs # In terms of seconds

FRAME_COUNT = int(AUDIO_LENGTH*FPS)
FRAME_OFFSET = int(len(audio)/FRAME_COUNT)

def find_top_notes(fft):
  lst = [x for x in enumerate(fft.real)][1:] # Remove 0 frequency
  lst = sorted(lst, key=lambda x: x[1],reverse=True)

  notes = []
  strengths = []

  for note, strength in lst:
    note = int(round(freq_to_number(note)))
    if (note not in notes): 
      notes.append(note)
      strengths.append(strength)
      if len(notes) == MAX_NOTES + 1: 
        break # If we have the maximum number of notes, break
  return notes, strengths

# See https://newt.phys.unsw.edu.au/jw/notes.html
def freq_to_number(f): return 69 + 12*np.log2(f/440.0) + 24
def number_to_freq(n): return 440 * 2.0**((n-69)/12.0)
def note_name(n): return NOTE_NAMES[n % 12] + str(int(n/12 - 1))

def filter_cutoff_strength(notes, strengths):
  # We want to find the cutoff for the strength so that the maximum number of notes we would have is MAX_NOTES
  cutoff = strengths[0][MAX_NOTES]
  for subStrengths in strengths:
    cutoff = max(subStrengths[MAX_NOTES], cutoff)
  cutoff += 1

  print("Cutoff: %.2E\t" % Decimal(cutoff))

  for i in range(len(notes)):
    current_notes = notes[i]
    current_strengths = strengths[i]
    for j in reversed(range(MAX_NOTES + 1)):
      if current_strengths[j] < cutoff: current_notes.pop(j)
  
  return notes


def printnotes(notes, strengths):
  for note in notes:
    print(note_name(note) + "\t\t", end="")
  print()
  for strength in strengths:
    print("%.2E\t" % Decimal(strength), end="")
  print()

# Get all notes, then get all strengths
all_notes = []
all_strengths = []

for i in range(FRAME_COUNT):
  fft = np.fft.rfft(audio[i * FRAME_OFFSET: (i + 1) * FRAME_OFFSET])
  fft = np.abs(fft) 
  notes, strengths = find_top_notes(fft)
  all_notes.append(notes)
  all_strengths.append(strengths)

filter_cutoff_strength(all_notes, all_strengths)

from midiutil.MidiFile import MIDIFile

# create your MIDI object
mf = MIDIFile(1)
track = 0   # the only track
channel = 0 # Only on one channel
volume = 100
time = 0    # time counter
previous_notes = {}   # Tracker to see how long a note lasts


mf.addTrackName(track, time, "Track 1")
mf.addTempo(track, time, int(60 * FPS))

# Update duration of notes
for notes in all_notes:
  time += 1 # Updates timer

  # If no notes being played, then we hold down the last known notes
  if len(notes) == 0:
    for note in previous_notes:
      if previous_notes[note] != 0: previous_notes[note] += 1
    continue

  # Increment all notes that are still playing
  for note in notes:
    if note in previous_notes: previous_notes[note] += 1 # For every first encounter with a new note, we have to add it into the dictionary
    else: previous_notes[note] = 1
  
  # Add in notes whose duration has ended
  for note in previous_notes:
    if note not in notes and previous_notes[note] != 0:
      mf.addNote(track, channel, note, time - previous_notes[note], previous_notes[note], volume)
      previous_notes[note] = 0

mf.writeFile(open("outputsongs/conversion.mid", 'wb'))



# # write it to disk
# with open("outputsongs/conversion.mid", 'wb') as outf:
#     mf.writeFile(outf)



# s = find_top_notes(fft)
# s = ["E", "C", "A"]
# print(s)
# chord = chords.determine(s, shorthand=True, no_inversions=False, )
# print(chord)