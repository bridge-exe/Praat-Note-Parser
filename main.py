#Name of the file you'd like to read
file_name = "info"
#Name of the instrument in the video
instrument = "EmileBalafon2"

#What would you like the outputted Elan TextGrid file to be named? (outputted in textgrid_data file)
ELAN_name = 'example'

#Set to True to get one of the following: 

#0. Does all of the below
do_all = False

#1. An Elan file of individual notes 
individual_notes = False

#2. An Elan file of notes outputted as one annotation per phrase 
note_phrases = True

#3 An Elan file of frequencies outputed as one annotation per phrase 
freq_phrases = False

#4. An elan file of individual relative notes (eg. '5', '4', '5', '5', '5')**
relative_notes = False 

#5. An Elan file of relative notes in a phrase (eg.'5 4 5 5 5')** 
relative_phrases = False

#---------------------------------------------------------#
import freq_to_notes as ftn
import auto_segmenter as autoseg
import relative_notes as rn
import phrase_parser as pp 
import relative_phrases as rp
import do_all as dl 

# using text file from Praat, gets file name, makes a dict with time:freq lines as a list, then removes header, creates empty dictionary

#do_all, individual_notes, note_phrases, freq_phrases, relative_notes, relative_phrases

def make_dict(file_name):
  ######-----SELECT WHETHER YOU WANT TO TYPE THE NAME OR INPUT IT---####
  text_file = open('praat_data/' + file_name + ".txt")
  # text_file = open('praat_data/' + input() + ".txt")

  text_file_lines = text_file.readlines()
  text_file_lines.remove(text_file_lines[0])

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
  chunk_list = [x for x in chunk_list if x != []]

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

      file_info.append([float(sound_start), int(beat_len), avg_freq]) #######
    
# prints and returns
  # for x in freq_and_lengths.items(): 
  #   print(x)

  # for x in file_info:
  #   print(x)

  # print(file_name)
  return file_info


def directive():
  file_notes = freq_parser(chunk_data(make_dict(file_name)))
  # pp.phrase_parser(ftn.freq_to_notes(file_notes, False, instrument)

  if do_all: 
    individ_notes = autoseg.auto_segmenter(ftn.freq_to_notes(file_notes, False, instrument), ELAN_name + '_individual_notes_file') 

    note_phrase = autoseg.auto_segmenter(pp.phrase_parser(ftn.freq_to_notes(file_notes, False, instrument)), ELAN_name + '_note_phrases_file')
  
    frequencies = autoseg.auto_segmenter(pp.phrase_parser(file_notes), ELAN_name + '_frequency_file')

    relative_note = autoseg.auto_segmenter(rn.relative_notes(pp.phrase_parser(ftn.freq_to_notes(file_notes, True, instrument))), ELAN_name + '_relative_notes_file')

    relative_phrase = autoseg.auto_segmenter(rp.relative_phrases(pp.phrase_parser(ftn.freq_to_notes(file_notes, True, instrument))), ELAN_name +'_relative_phrases_file')

    dl.do_all(ELAN_name, individ_notes, note_phrase, frequencies, relative_note, relative_phrase)


  else: 
    if individual_notes:
      autoseg.auto_segmenter(ftn.freq_to_notes(file_notes, False, instrument), ELAN_name) 

    elif note_phrases:
      autoseg.auto_segmenter(pp.phrase_parser(ftn.freq_to_notes(file_notes, False, instrument)), ELAN_name)
          
    elif freq_phrases:
      autoseg.auto_segmenter(pp.phrase_parser(file_notes), ELAN_name)

    elif relative_notes: 
      autoseg.auto_segmenter(rn.relative_notes(pp.phrase_parser(ftn.freq_to_notes(file_notes, True, instrument))), ELAN_name)

    elif relative_phrases: 
      autoseg.auto_segmenter(rp.relative_phrases(pp.phrase_parser(ftn.freq_to_notes(file_notes, True, instrument))), ELAN_name)


#runs it all
directive()