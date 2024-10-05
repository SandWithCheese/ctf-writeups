import mido
import random

def text_to_bits(text):
    return ''.join(format(ord(c), '08b') for c in text)

def encode_message_in_midi(midi_file, message, output_file, seed=None):
    mid = mido.MidiFile(midi_file)
    binary_message = text_to_bits(message)
    message_index = 0
    max_len = len(binary_message)
    
    if seed:
        random.seed(seed)

    note_on_messages = []
    for track in mid.tracks:
        for msg in track:
            if msg.type == 'note_on':
                note_on_messages.append(msg)

    random.shuffle(note_on_messages)
    print(note_on_messages)

    for msg in note_on_messages:
        if message_index < max_len:
            bit = int(binary_message[message_index])
            if bit == 1:
                msg.velocity = min(127, msg.velocity | 1)
            else:
                msg.velocity = msg.velocity & ~1
            message_index += 1

    mid.save(output_file)
    print(f"Message encoded and saved to {output_file}")

# encode_message_in_midi('beginner.mid', 'IFEST{xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx}', 'maestro.mid', seed=random.randint(0,1337))
encode_message_in_midi('beginner.mid', 'IFEST{xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx}', 'test.mid', seed=0)