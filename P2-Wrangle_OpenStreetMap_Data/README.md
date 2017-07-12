# P2 - Wrangle OpenStreetMap Data

## Build Requirement
Python 3
MongoDB

## Python Code Structure
There are three code files included in this project submission.
1.	data.py – reading data from xml file and store a json, no data processing is done in this file except converting the xml into json
2.	cleaning_queries.py – cleaning queries to address the problems raised in part 2 of this report.
3.	explore_queries.py – queries to explore the data set for part 3 and 4

## Getting Started
1. Install MongoDB on the machine
2. Put the data file `hong-kong_china.osm` under this folder. If you want to use a different file name, you may change it in `data.py` file
3. Run the xml to json code by `python data.py`
4. Import the data into MongoDB, example import shell script:
`mongoimport --db openstreetmap --collection hk --drop --file ./hong-kong_china.json`
5. To clean up the data in MongoDB as described in the report:
`python cleaning_queries.py`
6. To explore the data in MongoDB as described in the report:
`python explore_queries.py`
