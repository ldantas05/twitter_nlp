# twitter_nlp
Captures tweets from governors of all the US states and shows sentiment towards the Covid Pandemic during the selected time, displays average sentiment during that time in map as well as average sentiment each day on a lineplot.

# required installs
pip install pandas plotly char_studio numpy matplotlib tkcalendar requests TwitterAPI

# required licences
need google cloud sdk key called key in the main folder as well as twitter API premium sandbox bearer key and app environment name

For the program to work replace credentials_template.py data with required keys and rename to credentials.py

Run program by running: python stateanalyzer.py

Depending on the type of license you might need to adjest the dev field in credential to either "30day" or "fullarchive", full archive has less pull requests but it grants access to historical data meanwhile 30 is limited to the previous 30 days but you get many more requests. Program might not run to completion since TwitterAPI limits the amount of requests per minute. Graphs are displayed in browser using plotly and are interactive.


