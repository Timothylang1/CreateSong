import wave
import midiutil
 
def create_midi_from_wav(wav_file_path: str, midi_file_path: str):
    """
    Converts a WAV sound file to a MIDI file.
 
    Parameters:
    - wav_file_path: str
        The path to the input WAV sound file.
    - midi_file_path: str
        The path to save the output MIDI file.
 
   """
 
    # Open the WAV file
    with wave.open(wav_file_path, 'rb') as wav_file:
        # Get the audio parameters
        sample_width = wav_file.getsampwidth()
        frame_rate = wav_file.getframerate()
        num_frames = wav_file.getnframes()
        num_channels = wav_file.getnchannels()
 
        # Read the audio data from the WAV file
        audio_data = wav_file.readframes(num_frames)
 
    # Create a MIDI file
    midi_file = midiutil.MIDIFile(num_channels)
 
    # Set the tempo and time signature
    # tempo = 120  # Adjust the tempo as needed
    # time_signature = (4, 4)  # Adjust the time signature as needed
    # midi_file.addTempo(0, 0, tempo)
    # midi_file.addTimeSignature(0, 0, *time_signature)
 
    # Convert the audio data to MIDI events
    for i in range(num_frames):
        # Get the sample value for each channel
        sample_values = []
        for j in range(num_channels):
            sample_start = i * num_channels * sample_width
            sample_end = sample_start + sample_width
            sample_data = audio_data[sample_start:sample_end]
            sample_value = int.from_bytes(sample_data, byteorder='little', signed=True)
            sample_values.append(sample_value)
 
        # Add the MIDI events for each channel
        for channel, sample_value in enumerate(sample_values):
            # Scale the sample value to the MIDI range (0-127)
            midi_value = int((sample_value / (2 ** (8 * sample_width))) * 127)
 
            # Add a note event with the MIDI value
            midi_file.addNote(0, channel, midi_value, i, i + 1, 100)
 
    # Save the MIDI file
    with open(midi_file_path, 'wb') as midi_file:
        midi_file.writeFile(midi_file_path)
 
# Example usage:
wav_file_path = "inputsongs/Plain White T's - Hey There Delilah.wav"
midi_file_path = "outputsongs/output.mid"
create_midi_from_wav(wav_file_path, midi_file_path)
print("Finished")