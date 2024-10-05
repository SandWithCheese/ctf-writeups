import mido
import random

for i in range(1338):
    seed = i
    print(f"Trying seed {seed}")
    random.seed(seed)

    mid = mido.MidiFile('maestro.mid')

    note_on_messages = []
    for track in mid.tracks:
        for msg in track:
            if msg.type == 'note_on':
                note_on_messages.append(msg)
    
    random.shuffle(note_on_messages)

    bin_message = ""
    for msg in note_on_messages:
        if msg.velocity & 1:
            bin_message += "1"
        else:
            bin_message += "0"
    
    message = ""
    for i in range(0, len(bin_message), 8):
        message += chr(int(bin_message[i:i+8], 2))
    
    if "IFEST" in message:
        print(message)
        break