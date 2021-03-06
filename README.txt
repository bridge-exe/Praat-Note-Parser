Introduction:
This is a utility code used to parse the frequencies, notes, and relative musical positions of the Toussian Musical Surrogate Language. It outputs a TextGrid file, which may be exported into ELAN for automatic annotation. 

Instructions: 
1. Select audio and video files.
2. Import audio file into Praat
  2a. Select View & Edit
  2b. On the new file window, select View -> Show Analyses 
  2c. Set Longest Analysis to a large value, depending on length of the file, then hit OK.
  2d. Select (highlight) range to analyze (e.g. full length of the audio file, etc.)
  2e. Go to Pitch -> Pitch Listing. Praat will tell you if the Longest Analysis from #2c needs to be longer. (NOTE: you can adjust the "Advanced pitch settings" here to try and get more accurate frequencies, but the default is usually fine.)
  2f. Save the resulting text file.
3. Upload the new text file into the repl under praat_data.
4. Go to main.py and follow the prompts
5. After filling in the prompts (file name, name of the instrument, final TextGrid file name, true/false settings), hit Run.

To export the .TextGrid file:
6. In the repl, click the three dots in the top left of the repl -> "Download as zip"
  6a. Extract the files to your computer, namely the new .TextGrid file.
  6b. OPTIONALLY you may choose to copy-paste the output into a notepad app on your computer, then save that as a .TextGrid file. 
You now have the final .TextGrid file.

To upload the .TextGrid file into ELAN:
7. In ELAN: File -> Import -> Praat TextGrid File, and select the desired TextGrid file. 
  7a. Click the box for "Skip empty intervals," then hit Finish. 
