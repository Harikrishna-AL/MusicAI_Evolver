from pyswarm import pso
from music21 import stream, note, chord, tempo, meter, instrument
import random
from midi2audio import FluidSynth


c_major_scale = [60, 62, 64, 65, 67, 69, 71]  
c_major_chords = [[60, 64, 67], [62, 65, 69], [64, 67, 71], [65, 69, 72], [67, 71, 74]]  

chord_progressions = [
    [[60, 64, 67], [67, 71, 74], [69, 72, 76], [65, 69, 72]],  
    [[60, 64, 67], [65, 69, 72], [67, 71, 74], [60, 64, 67]]  
]

def melody_similarity_fitness(melody, input_melody):
    fitness = 0
    for i in range(len(melody) - 1):
        interval = abs(melody[i] - melody[i + 1])
        input_interval = abs(input_melody[i % len(input_melody)] - input_melody[(i + 1) % len(input_melody)])

        if interval == input_interval:
            fitness += 2
        elif interval <= 2:
            fitness += 1  
        
        if melody[i] in c_major_scale:
            fitness += 1
        else:
            fitness -= 2 
        
        if melody[i] == melody[i + 1]:
            if input_melody[i % len(input_melody)] == input_melody[(i + 1) % len(input_melody)]:
                fitness += 1  
            else:
                fitness -= 1
        
    unique_notes = len(set(melody))
    if unique_notes < len(melody) // 2:
        fitness -= 5

    return -fitness

def add_phrasing_to_melody(melody, input_melody, phrase_length):
    phrase = melody[:phrase_length]
    input_phrase = input_melody[:phrase_length]
    variation = [(n + random.choice([-1, 1])) for n in input_phrase] 
    return (phrase + variation + phrase)[:len(melody)]

def generate_regular_rhythm(length):
    rhythm = []
    for i in range(length):
        if i % 4 == 0:
            rhythm.append(1.0)  
        else:
            rhythm.append(0.5)  
    return rhythm

def create_melody_stream(melody, rhythm):
    s = stream.Part()
    s.append(tempo.MetronomeMark(number=120)) 
    s.append(meter.TimeSignature('4/4'))       
    s.append(instrument.Piano())               
    for pitch, dur in zip(melody, rhythm):
        n = note.Note()
        n.pitch.midi = int(pitch)
        n.quarterLength = dur
        s.append(n)
    return s

def add_harmonic_progression(melody_stream, progression):
    harmony_stream = stream.Part()
    harmony_stream.append(instrument.Piano())  # Piano for harmony
    for i, note_obj in enumerate(melody_stream.notes):
        chord_index = i // 4  # Change chords every 4 notes
        base_chord = progression[chord_index % len(progression)]
        chord_notes = [note.Note(midi=n) for n in base_chord]
        harmony_chord = chord.Chord(chord_notes)
        harmony_chord.quarterLength = note_obj.quarterLength
        harmony_stream.append(harmony_chord)
    return harmony_stream

def convert_midi_to_wav(input_midi, output_audio):
    fs = FluidSynth()
    fs.midi_to_audio(input_midi, output_audio)