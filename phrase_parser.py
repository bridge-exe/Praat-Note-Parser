#takes note data and parses into phrases based on rest time between 
#takes in file_info = (float, int, str): (timestamp, length in ms, note/undef)

def phrase_parser(file_info): 
 #go through times, find undef sequences, parse out undef rest length, use to create chunks of 'phrases', use those phrases to make definite and relative frequency phrases
  phrase_info = []
  phrase = []

  note_time_variance = 1000
  
  for info in file_info:
    note = info[2]
    note_length = int(info[1])
    start_time = float(info[0])
    note_a = [start_time, note_length, note]
    
    #checks if the phrase is a rest
    if 'undefined' in info: 
      #if it is over 1 sec, consider it a phrase break
      
      if note_length > note_time_variance: 
        phrase_info.append(phrase)
        phrase = []
        phrase_break = [start_time, note_length, 'phrase_break']
        phrase_info.append(phrase_break)
        
      #if it is not a rest, consider it a phrase, have the notes and rests appended to phrase info as lists in a list 
      else: 
        phrase.append(note_a)      
       
    #appends undefined notes as info 
    else: 
      phrase.append(note_a)

  if 'phrase_break' not in info: 
    phrase_info.append(phrase)
   
  #removes empty strings 
  phrase_info = [x for x in phrase_info if x != []] 
  # print(phrase_info)

  #compare notes relative to each other, broken up by phrase breaks 
  phrase_and_length_info = []
  phrase_notes = []

  #goes through and creates TextGrid-able lists 
  for phrase in phrase_info:
    
    phrase_start = phrase[0]
    if type(phrase_start) == list: 
      phrase_start = phrase_start[0]
   
    phrase_length = 0 
    phrase_notes = []

    if 'phrase_break' in phrase: 
      phrase_and_length_info.append(phrase)
    
    else: 
      for note in phrase: 
        
        phrase_length += note[1]
        note_val = str(note[2])
        phrase_notes.append(note_val)

      phrase_and_length_info.append([phrase_start, phrase_length, phrase_notes])
  
  
  return(phrase_and_length_info, phrase_info)
#--------------------------#
  # for x in phrase_info: 
  #  print(x)


  # for x in phrase_and_length_info: 
  #   print(x)
    # print(phrase_and_length_info)


 

#returns file info of type (float, int, str): (timestamp, length, notes in sequence)
                                             #(11.0,      30.0s,  '5 4 5 5 3') 
                                             #(11.0,      30.0s,  'F E F F D') 