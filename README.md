# theaconf-nlp

This repository is a collection different ways to analyse the the text (mostly abstracts) from the website of the 2022 Gesellschaft für Theaterwissenschaft congress "Matters Of Urgency": https://matters-of-urgency.de/

## Data

The first step before being able to work with the data is aquiring the -- in this case -- complete website as html files. One of the most straight forward ways to do this is using the commandline tool wget: https://www.gnu.org/software/wget/ or (german): https://wiki.ubuntuusers.de/wget/

In this case the complete command was: `wget -r -k -E -l 8 https://matters-of-urgency.de/`

This dumps the webite as funktional html pages directly into the working folder.

## Parsing the HTML


