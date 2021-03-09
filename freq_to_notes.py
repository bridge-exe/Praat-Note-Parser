#create dictionary/list of notes relative to their frequencies
# takes in file_info = (float, int, str):(timestamp, length in ms, freq/undef)
# find range of frequencies within notes, 
# if it is higher than the variance, then analyze 
# it as more than one note?
import csv

def freq_to_notes(file_info, relative, undefined_included, instrument = 'JulaBalafon'): 
  open_file = open("praat_data/balafon_Frequencies.csv")
  notes = csv.reader(open_file, delimiter=',')
  balafon_notes = []
  #creates the note dict that we use to parse the notes in the future
  for x in notes:
    balafon_notes.append(x)

  notes_and_lengths = {}
  variance = 9
  
  instrument_col = balafon_notes[0].index(instrument)
  notes_and_lengths_info = []

  #goes through each note, compares it against a column within the instrument column of the csv, spits out the column index +1, which will be the note 

  for note in file_info: 
    note_info = []
     
    length = str(note[1])
    start = str(note[0])
    freq = note[2]

#finds the absolute note for each frequency
 
    #classifies undef as rest? 
    if 'undefined' in note:
      #if undef_included is true, this will include 'undefined' in the outputs 
      if undefined_included:
        notes_and_lengths['beat ' + str(count)] = 'rest for ' + length + 'ms' + ' at ' + start + 's'
        notes_and_lengths_info.append([start, length, 'undefined'])
      else: 
        continue 

    else: 
      note_freq = round(freq)
      note_range = range(round(note_freq) - variance, round(note_freq) + variance)
      note_found = False

      for row in balafon_notes: 
        #simple catch for first val, which will be a string with the name of the instrument
        if instrument in row[instrument_col]:
          continue

        #catches empty values, in case of shorter balafon
        elif row[instrument_col] == '': 
          continue

        #checks column for match of the_note +-variance 
        elif int(row[instrument_col]) in note_range: 
          if relative: 
            the_note = row[0]

          else: 
            the_note = row[instrument_col + 1]
          
          notes_and_lengths['beat ' + str(count)] = str(the_note) + ' for ' + length + 'ms' + ' at ' + start + 's'
          note_found = True
          notes_and_lengths_info.append([start, length, the_note])

      #in case the note is not found, the freq is applied instead
      if not note_found:  
        notes_and_lengths['beat ' + str(count)] = str(freq) + 'hz for ' + length + 'ms' + ' at ' + start + 's'
        notes_and_lengths_info.append([start, length, str(freq)])


  # for x in notes_and_lengths_info: 
  #   print(x)
  return notes_and_lengths_info

# spits out a list of lists, where each list is [timestamp, length in ms, and note (or freq)]
#using the average frequencies from the main.py calculations, hard code in encoder to return a dictionary that has the same format as the earlier print statement, but with Notes and their respective pentave range. 