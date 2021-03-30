from praatio import tgio

def do_all(ELAN_name, individual_notes, note_phrases, frequencies, relative_notes, relative_phrases): 
  
  
  #creates tiers of import
  individual_notes_tier = tgio.IntervalTier('Individual Notes', individual_notes)
  note_phrases_tier = tgio.IntervalTier('Note Phrases', note_phrases)
  frequencies_tier = tgio.IntervalTier('Frequencies', frequencies)
  relative_notes_tier = tgio.IntervalTier('Relative Notes', relative_notes)
  relative_phrases_tier = tgio.IntervalTier('Relative Phrases', relative_phrases)

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
  
  file_textgrid.addTier(individual_notes_tier)
  file_textgrid.addTier(note_phrases_tier)
  file_textgrid.addTier(frequencies_tier)
  file_textgrid.addTier(relative_notes_tier)
  file_textgrid.addTier(relative_phrases_tier)
  
  # file_textgrid.addTier(beat_tier
  file_textgrid.addTier(karim_tier)
  file_textgrid.addTier(ktrans_tier)
  file_textgrid.addTier(ant_tier)
  file_textgrid.addTier(atrans_tier)
  file_textgrid.addTier(emile_tier)
  file_textgrid.addTier(etrans_tier)

  file_textgrid.save('textgrid_data/' + ELAN_name + '_combined.TextGrid') 
  