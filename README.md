# pco-songbook

One Paragraph of project description goes here

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

## Road Map
- [x] Retrieve chords, lyrics, metadata from API
- [x] Parse chordpro format
	- [x] Clean up lyrics
	- [x] Extract chords, song structure, lyrics
- [x] Layout chords and lyrics into two line format
- [ ] Layout song and fine tune sizes
	- [ ] Adjust width based on ratio of longest song line to the max width given to the song
	- [ ] Adjust height to fit space
	- [ ] Have a minimum font size that cannot be breached. If needs to be passed, display song on two quarters
	- [ ] Add headers/footers to songs and pages
- [ ] Output to PDF


## Meta Tasks

- [ ] Edit songs in PCO to make the output pretty
- [ ] Choose a font
- [ ] Select which songs get exported
- [ ] How user-friendly does it need to be?
- [ ] Hide the API key somehow
- [ ] Get publishing company for each song somehow
- [ ] Clarify input method (e.g. .csv, commandline, etc.)

## Formatting Issues
- One line of lyrics is too long (shrink font or overflow)
- Too many lyrics (overflow or shrink font)
- Unrecognized characters create strange output 
