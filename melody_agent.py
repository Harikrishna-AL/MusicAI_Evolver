from pyswarm import pso
from music21 import stream, note, chord, tempo, meter, instrument
import random
from extract_feat import extract_feat, hz_to_midi
from utils import melody_similarity_fitness, add_phrasing_to_melody, generate_regular_rhythm, create_melody_stream, add_harmonic_progression, convert_midi_to_wav


c_major_scale = [60, 62, 64, 65, 67, 69, 71]  
c_major_chords = [[60, 64, 67], [62, 65, 69], [64, 67, 71], [65, 69, 72], [67, 71, 74]]  

chord_progressions = [
    [[60, 64, 67], [67, 71, 74], [69, 72, 76], [65, 69, 72]],  
    [[60, 64, 67], [65, 69, 72], [67, 71, 74], [60, 64, 67]]  
]


def main(input_file):
    num_notes = 64
    bounds = [(min(c_major_scale), max(c_major_scale)) for _ in range(num_notes)]

    input = extract_feat(input_file)  # Use the input_file directly
    input_melody = [hz_to_midi(pitch) for pitch in input if pitch > 0]
    input_melody = input_melody[:num_notes]  

    best_melody, best_fitness = pso(melody_similarity_fitness, [60]*num_notes, [72]*num_notes, 
                                    args=(input_melody,), swarmsize=20, maxiter=100)

    best_melody = [int(round(n)) for n in best_melody]
    best_melody = add_phrasing_to_melody(best_melody, input_melody, phrase_length=8)

    rhythm = generate_regular_rhythm(num_notes)
    melody_stream = create_melody_stream(best_melody, rhythm)
    progression = random.choice(chord_progressions)
    harmony_stream = add_harmonic_progression(melody_stream, progression)

    full_score = stream.Score()
    full_score.insert(0, melody_stream)
    full_score.insert(0, harmony_stream)

    full_score.write('midi', fp='similar_melody_with_harmony.mid')  # Use the default MIDI output path
    convert_midi_to_wav('similar_melody_with_harmony.mid', 'output.wav')  # Use the default MIDI output path
    print("WAV file 'output.wav' has been created successfully.")


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='Generate a melody similar to a given input melody')
    parser.add_argument('input_file', type=str, help='Path to the input melody file')
    args = parser.parse_args()
    main(args.input_file)  # Pass the input_file directly to the main() function



