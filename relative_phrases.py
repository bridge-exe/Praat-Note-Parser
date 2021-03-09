#how do we know when downstep happens? 
##find max val of phrase and go down 

#take in notes of notes from the csv file 
#use their locations to determine their relative position in the note phrase

#need data type of [[start, length, relnote1], [start, stop, relnote2]...]

#get to [start, length, relnote1], [start, stop, relnote2]...]

# two outcomes: one for individual notes, one for phrased notes. the individual notes need to come from the phrased notes, so do phrased notes first 
# in phrases find max val, make 5 - curr val 


#finds the phrases of notes, parses the high note of each phrase, uses that to compare, and output('42444')
def relative_phrases(file_info): 
  
  info = []
  count = 0 
  phrase_start = 0 
  
  #goes through each phrase in file_info 
  for phrase in file_info[1]: 
    phrase_list = []  
    phrase_length = 0 

    #checks for phrase_break 
    if 'phrase_break' in phrase: 
      info.append(phrase)
        
    else:
      phrase_start = phrase[0][0]
      
      high_note = 0 

      for note in phrase: 
        rel_note = note[2]

        if '.' in rel_note or 'undefined' in note: 
          phrase_length += note[1]  

        else: 
          rel_note = int(rel_note)
          if rel_note > high_note: 
            high_note = rel_note
          phrase_length += note[1]

      for note in phrase: 
        if not '.' in note[2] and not 'undefined' in note[2]: 
          new_note = str(5 - (high_note-int(note[2])))
          
          if int(new_note) <= 0 : 
            new_note = str(int(new_note) + 5) + 'a'

          phrase_list.append(new_note)
          # print(new_note)

        else: 
          phrase_list.append(note[2])

        

      new_list = [phrase_start, phrase_length] + [phrase_list]
      info.append(new_list)
      phrase_list = []
  
  info_outer = []
  info_outer.append(info)

  # for x in info: 
  #   print(x)

  return info

