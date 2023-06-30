# Data Pipeline - PGA Tour Data

This project was intended to be set up to continuously track PGA Tour stats week to week. 

## Instructions

The data pipeline was built with a particular order in mind. The goal was to first provide some tournament information, then gather the strokes gained data for that week and enter into database.

### To Update database

1. First manually populate the `tournaments` table with the information about where a particular event is played.
2. Next, the `scrape.py` script needs to be run to collect the data from the internet
   * There are few constants that need to be updated to successfully scrape webpage
3. Then, `load.py` needs to be run to transform and enter rest of data into database.

## Data Model

![1688073004450](https://file+.vscode-resource.vscode-cdn.net/Users/andrejacobs/Desktop/pga-tour-database/image/readme/1688073004450.png)
