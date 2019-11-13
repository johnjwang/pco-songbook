# pco-songbook

One Paragraph of project description goes here

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

## Running It

### Resources Songbook Mode

```
python songbook/__main__.py --csv input.csv output.pdf
```

The `input.csv` can be retrieved from the "Export CSV" feature on PCO's web interface.

### Band Mode
```
python songbook/__main__.py --band output.pdf
```

Notable differences from the resources songbook mode:

- Prints by letter so that we can use this with tab dividers (skips pages until a new letter can begin on a new odd-numbered page)
- Retrieves only non-archived songs from PCO API with song codes in the format: "A000 - Title"

## Road Map
- [x] Retrieve chords, lyrics, metadata from API
- [x] Parse chordpro format
	- [x] Clean up lyrics
	- [x] Extract chords, song structure, lyrics
- [X] Table of Contents
- [x] Layout chords and lyrics into two line format
- [X] Layout song and fine tune sizes
	- [X] Adjust width based on ratio of longest song line to the max width given to the song
	- [X] Adjust height to fit space
	- [X] Have a minimum font size that cannot be breached. If needs to be passed, display song on two quarters
	- [X] Add headers/footers to songs and pages
- [X] Output to PDF


## Meta Tasks

- [ ] Edit songs in PCO to make the output pretty
- [ ] Choose a font
- [x] Select which songs get exported
- [ ] How user-friendly does it need to be?
- [ ] Hide the API key somehow
- [x] Get publishing company for each song somehow
- [x] Clarify input method (e.g. .csv, commandline, etc.)


## Transformation Ideology
- WYSIWYG (mostly...)
- Part labels with no non-empty lines following are printed out
	- If it has lines, it's not printed out
