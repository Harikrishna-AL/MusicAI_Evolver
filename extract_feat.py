import librosa
import librosa.display
import numpy as np


def extract_feat(file_name):
    y, sr = librosa.load(file_name, sr=None)

    tempo, beat_frames = librosa.beat.beat_track(y=y, sr=sr)
    beat_times = librosa.frames_to_time(beat_frames, sr=sr)
    pitches, magnitudes = librosa.piptrack(y=y, sr=sr)

    midi_notes = []
    rhythm_durations = []
    pitch_values = []
    for i in range(pitches.shape[1]):
        index = magnitudes[:, i].argmax()
        pitch = pitches[index, i]
        if pitch > 0:
            pitch_values.append(pitch)
    
    return pitch_values

def hz_to_midi(hz):
    return int(np.round(69 + 12 * np.log2(hz / 440.0)))

