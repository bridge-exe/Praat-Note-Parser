import os
import os.path
from praatio import tgio
from os.path import join

#praat textgrid creator that auto annotates freq/notes and duration

#('tier_name', [(start, stop, 'annotation'), (start, stop, 'annotation'), ...])

# takes in file_info = (float, int, str): (timestamp, length in ms, freq/undef)

#create a for loop for the objs in file info, and add those tuples to list, use list to make a textGrid interval tier, use tier to make textgrid file 

def auto_segmenter(file_info, ELAN_name):
  # for x in file_info:
  #   print(x)
  beat_info = []
  rest_info = []
  file_length = 0 

  if len(file_info) == 2: 
    file_info = file_info[0]


  #each beat in file info should look like [start, length, name]
  for beat in file_info: 
    #creates vals for start, stop, and beat label
    
    beat_start = float(beat[0])
    beat_length = int(beat[1])/1000
    
    beat_end = round((beat_length + beat_start), 2)
    beat_label = beat[2]

    if 'undefined' in beat: 
      rest_info.append([beat_start, beat_end, 'rest'])
      continue
    
    elif 'phrase_break' in beat: 
      beat_info.append([beat_start, beat_end, ''])
      continue 

    if type(beat_label) == list:
      beat_label = [x for x in beat_label if x != 'undefined'] 
      beat_label = ' '.join(beat_label)

    # else: 
    #adds these vals to a list
    beat_info.append([beat_start, beat_end, beat_label])
    
  #creates tier desired beat info 

  beat_tier = tgio.IntervalTier('Balafon', beat_info)

  #nothing is left blank  
  nothing = [[0, 1, '']]  
  #creates tiers 
  karim_tier = tgio.IntervalTier('Karim', nothing)
  ktrans_tier = tgio.IntervalTier('Karim Translation', nothing) 
  ant_tier = tgio.IntervalTier('Anthony', nothing)
  atrans_tier = tgio.IntervalTier('Anthony Translation', nothing)
  emile_tier = tgio.IntervalTier('Emile', nothing)
  etrans_tier = tgio.IntervalTier('Emile Translation', nothing)

#creates the textgrid and adds in the filled beat tier, and blank tiers for further annotation
  file_textgrid = tgio.Textgrid()
  
  file_textgrid.addTier(beat_tier)
  file_textgrid.addTier(karim_tier)
  file_textgrid.addTier(ktrans_tier)
  file_textgrid.addTier(ant_tier)
  file_textgrid.addTier(atrans_tier)
  file_textgrid.addTier(emile_tier)
  file_textgrid.addTier(etrans_tier)

  

#makes textgrid of beats of given file_info

  file_textgrid.save('textgrid_data/' + ELAN_name + '.TextGrid')  

  # file_textgrid.save('C:\Users\Bridg\Praat Proj' + ELAN_name + '.TextGrid')
  
  #figure out saving to computer  
  return beat_info

  