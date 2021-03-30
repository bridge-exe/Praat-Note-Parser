#how do we know when downstep happens? 
##find max val of phrase and go down 

#take in notes of notes from the csv file 
#use their locations to determine their relative position in the note phrase

#need data type of [[start, length, relnote1], [start, stop, relnote2]...]

#get to [start, length, relnote1], [start, stop, relnote2]...]

# two outcomes: one for individual notes, one for phrased notes. the individual notes need to come from the phrased notes, so do phrased notes first 
# in phrases find max val, make 5 - curr val 

def relative_notes(file_info): 
  info = []
  count = 0 
  
  #goes through each phrase in file_info 
  for phrase in file_info[1]: 
    # print(phrase)
    phrase_list = []
    #checks for phrase_break 
    if 'phrase_break' in phrase: 
      info.append(phrase)
      #can remove if desired 
        
    else:
      high_note = 0 

      for note in phrase: 
        rel_note = note[2]

        if '.' in rel_note or 'undefined' in note: 
          # info.append(note)
          continue

        else: 
          rel_note = int(rel_note)
          if rel_note > high_note: 
            high_note = rel_note
          # phrase_length += note[1]

      for note in phrase: 
        #gets the note relative to others 
        if not '.' in note[2] and not 'undefined' in note[2]: 
          #the note is 5 minus (the highest note of the phrase minus the row number of the note)
          new_note = [note[0], note[1], str(5 - (high_note-int(note[2])))]

          #if this new note is 0, then it equals the high note and should be 5, if it less than 0, it is an octave below, and should have 5 added to it. 
          if int(new_note[2]) <= 0 : 
            new_note = str(int(new_note[2]) + 5) + 'a'
            if new_note == '0a': 
              new_note = '5aa'
            phrase_list.append(new_note)
            new_note = [note[0], note[1], new_note]
            phrase_list.append(new_note)
            
          info.append(new_note)

        else: 
          info.append(note)

  info_outer = []
  info_outer.append(info)
  
  # for x in info: 
    # print(x)

  return info

