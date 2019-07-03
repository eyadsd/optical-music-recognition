import numpy as np
from midiutil import MIDIFile
from enum import Enum

class notes(Enum):
    F3=53
    G3=55
    A3=57
    B3=59
    C4=60
    D4=62
    D4sharp=63
    E4=64
    F4=65
    F4sharp=66
    G4=67
    G4sharp=68
    A4=69
    A4sharp=70
    B4=71
    C5=72
    C5sharp=73
    D5=74
    D5sharp=75
    E5=76
    F5=77
    F5sharp=78
    

def create_midi_file(staves, track_name):
    
    # Create the MIDIFile Object
    MyMIDI = MIDIFile(1)

    # Add track name and tempo. The first argument to addTrackName and
    # addTempo is the time to write the event.
    track = 0
    time = 0
    MyMIDI.addTrackName(track, time, "Sample Track")
    MyMIDI.addTempo(track, time, 120)
    for stave in staves:
        #create_midi_per_stave(stave.symbols,MyMIDI,track)
        # Add a note. addNote expects the following information:
        channel = 0
        duration = 1
        volume = 100
        i = 0

        """symbols = [Symbol("G-clef",0),Symbol("quarter-note",6),Symbol("quarter-note",6),Symbol("quarter-note",7),Symbol("quarter-note",8),
        Symbol("quarter-note",8),Symbol("quarter-note",7),Symbol("quarter-note",6),Symbol("quarter-note",5),Symbol("quarter-note",4),
        Symbol("quarter-note",4),Symbol("quarter-note",5),Symbol("quarter-note",6),Symbol("quarter-note",6),Symbol("quarter-note",5),Symbol("half-note",5)]"""

        G_clef = {1: notes.D4, 2: notes.E4, 3: notes.F4, 4: notes.G4, 5: notes.A4, 6: notes.B4, 7: notes.C5,
                  8: notes.D5, 9: notes.E5, 10: notes.F5}

        F_clef = {1: notes.F3, 2: notes.G3, 3: notes.A3, 4: notes.B3, 5: notes.C4, 6: notes.D4, 7: notes.E4,
                  8: notes.F4, 9: notes.G4, 10: notes.A4}
        clef = G_clef

        for symbol in stave.symbols:
            if symbol.label == "G_clef":
                clef = G_clef
            # elif symbol.label == "F_clef":
            #     clef = F_clef

        for i in range(len(stave.symbols)):
            print(i)
            if stave.symbols[i].position_in_stave == 0:
                continue
            if stave.symbols[i].label == "sixteenth_note":
                duration = 0.25
                pitch = clef[stave.symbols[i].position_in_stave].value
                MyMIDI.addNote(track, channel, pitch, time, duration, volume)
                time = time + duration
            if stave.symbols[i].label == "eighth_note":
                duration = 0.5
                pitch = clef[stave.symbols[i].position_in_stave].value
                MyMIDI.addNote(track, channel, pitch, time, duration, volume)
                time = time + duration
            elif stave.symbols[i].label == "quarter_note":
                duration = 1
                pitch = clef[stave.symbols[i].position_in_stave].value
                MyMIDI.addNote(track, channel, pitch, time, duration, volume)
                time = time + duration
            elif stave.symbols[i].label == "half_note":
                duration = 2
                pitch = clef[stave.symbols[i].position_in_stave].value
                MyMIDI.addNote(track, channel, pitch, time, duration, volume)
                time = time + duration
            elif stave.symbols[i].label == "whole_note":
                duration = 4
                pitch = clef[stave.symbols[i].position_in_stave].value
                MyMIDI.addNote(track, channel, pitch, time, duration, volume)
                time = time + duration

            """if i != 0 :
                if symbols[i-1].label == "sharp":
                    pitch=stave[symbols[i].position_in_stave ].value+1
                elif symbols[i-1].label == "flat":
                    pitch = stave[symbols[i].position_in_stave ].value-1"""

    print("anything")
    # And write it to disk.
    with open("media\\" + track_name + ".mid", 'wb') as binfile:
        MyMIDI.writeFile(binfile)




def create_midi_per_stave(symbols, MyMIDI,track):
    pass


