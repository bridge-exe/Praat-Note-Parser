#Name of the file you'd like to read in praat_data folder
  #MAKE SURE IT IS SPELLED RIGHT, EXACTLY AS IT IS WRITTEN IN PRAAT_DATA
file_name = "2019-08-7.txt"

#Name of the instrument in the video
#You may enter "My Balafon", "EmileBalafon1", "EmileBalafon2", "StearnsLargeBalafon", "SiamouBalafonDieri", DianBalafon", "JulaBalafon", or "BwabaBalafon"
instrument = "EmileBalafon2"

#What would you like the outputted Elan TextGrid file to be named? (outputted in textgrid_data file)
ELAN_name = "2019-08-7"

#Output Settings
#set one of these to True to get one of the following: 
#0. Does all of the below
do_all = True

#1. An Elan file of frequencies outputed as one annotation per phrase (eg '550hz 400hz 550hz 550hz 550hz)
freq_phrases = False

#2. An Elan file of individual notes (eg. 'F', 'C', 'F', 'F', 'F')
individual_notes = False

#3. An Elan file of notes outputted as one annotation per phrase (eg. 'F C F F F')
note_phrases = False

#4. An elan file of individual relative notes (eg. '5', '4', '5', '5', '5' '5a')
relative_notes = False

#5. An Elan file of relative notes in a phrase (eg.'5 4 5 5 5 5a')
relative_phrases = False

#---------------------------------------------------------#
import freq_to_notes as ftn
import auto_segmenter as autoseg
import relative_notes as rn
import phrase_parser as pp 
import relative_phrases as rp
import do_all as dl 
#using text file from Praat, gets file name, makes a dict with time:freq lines as a list, then removes header, creates empty dictionary

#do_all, individual_notes, note_phrases, freq_phrases, relative_notes, relative_phrases

def make_dict(file_name):
  #creates name of file
  # if '.txt' in file_name: 
  #   text_file = open('praat_data/' + file_name)
  # else: 
  #   text_file = open('praat_data/' + file_name + ".txt")

  text_file = open('praat_data/' + file_name)

  #reads info into text_file_lines
  text_file_lines = text_file.readlines()
  text_file_lines.remove(text_file_lines[0])
  text_file_lines.append('0.0000   --undefined--')

  #creates dictionary of times and hz
  text_file_dictionary = {}
  for line in text_file_lines:
      text_file_dictionary[line.split()[0]] = line.split()[1]
  
  #adding end marker to text_file_dictionary, so that it can be parsed later 
  text_file_dictionary['end'] = 'here'
  return text_file_dictionary


def chunk_data(dictionary):  
  #goes through dict, sorts data into chunk_list, which is a list of lists-- 'chunks' of information, notes or rests. At the same time, it stores the time stamps of the relevant markers and then zips the data together to be returned. 
  undef_list = []
  freq_list = []
  chunk_list = []
  sound_starts = []

  for item in dictionary.items():
    curr_freq = item[1]
    curr_time = item[0]
    sound_starts.append(curr_time)
    
#if val is undefined, adds freq_list to chunk_list, clears freq_list and adds 'undefined' to undef_list 
    if 'undefined' in curr_freq: 
      chunk_list.append(freq_list)
      freq_list = []
      undef_list.append(curr_freq)
    
    #checks if it is the last val in the list, if so, adds either freq_list or undef_list to chunk_list, depending on which was cleared last
    elif 'end' in curr_freq: 
      chunk_list.append(freq_list)
      chunk_list.append(undef_list)

    #if val is not undefined (ie. a float), adds undef_list to chunk_list, clears undef_list and adds the float to freq_list 
    else: 
      chunk_list.append(undef_list)
      undef_list = []
      freq_list.append(curr_freq)

  #removes empty strings
  new_list = [x for x in chunk_list if x != []]

 

  #goes through the chunk list to see if there are any areas of notes that haave a large jump between them. This will mean that there is a flam or octave being played, and so should count as two notes within the chunk 

  chunk_list = []

  for chunk in new_list:  
    variance = 9 
    found_notes = []

    if '--undefined--' in chunk: 
      chunk_list.append(chunk)
    #an undefined chunk describes a period of silence, and so should not be observed for flams 

    elif '--undefined--' not in chunk: 
      # prev_freq = float(chunk[0])
      #goes through the frequencies in the list chunk
      partial_chunk = []
      for i in range(len(chunk)-1):
        note_freq = float(chunk[i])
        next_freq = float(chunk[i+1])
        note_range = range(round(note_freq) - variance, round(note_freq) + variance)

        partial_chunk.append(chunk[i])
    
        if round(next_freq) not in note_range: 
          chunk_list.append(partial_chunk)
          partial_chunk = []

      partial_chunk.append(chunk[-1])
      chunk_list.append(partial_chunk)
        

#creates list stamp_list of time stamps for beginnings of each new beat 
  start_stamp = 0 
  stamp_list = [sound_starts[0]]
  
  for beat in chunk_list: 
    stamp_list.append(sound_starts[start_stamp + len(beat)])
    start_stamp = start_stamp + len(beat)

  chunk_list = list(zip(chunk_list, stamp_list))

  return chunk_list
      
def freq_parser(chunk_list): 
  #Goes through each list(beat) in chunk_list and describes their average freq and length. A 'beat' can either mean a note or a rest. 
  count = 0 
  freq_and_lengths = {}
  file_info = [] #######

  curr_time = chunk_list[0]
  
  #goes through each beat
  for chunk in chunk_list: 
    count += 1
    curr_time = chunk[1]
    curr_beat = chunk[0]
    sound_start = str(round(float(curr_time),4))
    beat_len = str(len(curr_beat)*10)

    #if beat is 'undef' it is a rest. counts how long the rest is, and adds this to freq_and_lengths dictionary
    if '--undefined--' in curr_beat: 
      freq_and_lengths['beat ' + str(count)] = 'rest for ' + beat_len + 'ms from ' + sound_start + 's'

      file_info.append([float(sound_start), int(beat_len), 'undefined'])

    #if beat is not 'undef' it is a note. else: calculates its average freqency in hertz, rounds it to 4 sig figs, and adds this frequency to freq_and_lengths with its duration
    else: 
      total_freq = 0 
      avg_freq = 0 

      for num in curr_beat: 
        total_freq = float(num) + total_freq
      avg_freq = round(total_freq/len(curr_beat), 3)

      freq_and_lengths['beat ' + str(count)] = str(avg_freq) + 'hz for ' + beat_len + 'ms' + ' at ' + sound_start + 's'

      file_info.append([float(sound_start), int(beat_len), avg_freq])
    
  return file_info


def directive():
  file_notes = freq_parser(chunk_data(make_dict(file_name)))
  # pp.phrase_parser(ftn.freq_to_notes(file_notes, False, instrument)

  if do_all: 
    individ_notes = autoseg.auto_segmenter(ftn.freq_to_notes(file_notes, False, True,instrument), ELAN_name + '_individual_notes_file', do_all) 

    note_phrase = autoseg.auto_segmenter(pp.phrase_parser(ftn.freq_to_notes(file_notes, False, True, instrument)), ELAN_name + '_note_phrases_file', do_all)
  
    frequencies = autoseg.auto_segmenter(pp.phrase_parser(file_notes), ELAN_name + '_frequency_file', do_all)

    relative_note = autoseg.auto_segmenter(rn.relative_notes(pp.phrase_parser(ftn.freq_to_notes(file_notes, True, True, instrument))), ELAN_name + '_relative_notes_file', do_all)

    relative_phrase = autoseg.auto_segmenter(rp.relative_phrases(pp.phrase_parser(ftn.freq_to_notes(file_notes, True, True, instrument))), ELAN_name +'_relative_phrases_file', do_all)

    dl.do_all(ELAN_name, individ_notes, note_phrase, frequencies, relative_note, relative_phrase)


  else: 
    if individual_notes:
      autoseg.auto_segmenter(ftn.freq_to_notes(file_notes, False, True, instrument), ELAN_name, do_all, '_individual_notes') 

    elif note_phrases:
      autoseg.auto_segmenter(pp.phrase_parser(ftn.freq_to_notes(file_notes, False, True, instrument)), ELAN_name, do_all, '_note_phrases')
          
    elif freq_phrases:
      autoseg.auto_segmenter(pp.phrase_parser(file_notes), ELAN_name, do_all, '_frequency_phrases')

    elif relative_notes: 
      autoseg.auto_segmenter(rn.relative_notes(pp.phrase_parser(ftn.freq_to_notes(file_notes, True, True, instrument))), ELAN_name, do_all, '_relative_notes')

    elif relative_phrases: 
      autoseg.auto_segmenter(rp.relative_phrases(pp.phrase_parser(ftn.freq_to_notes(file_notes, True, True, instrument))), ELAN_name, do_all, '_relative_phrases')

#runs it all
directive()