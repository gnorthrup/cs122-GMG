# cs122-GMG
Gabriel Levine, Maria Smith, and Graham Northrup's git repository for the CS122 project

Description
-----------
Little Bird is a tool that finds how Twitter users feel about particular topics. When a user provides a query, Little Bird selects recent tweets containing the query and runs a sentiment analysis program on each tweet to get a rating. An analysis of these tweet ratings are returned to the user.

Installation
-------------
git clone https://github.com/gnorthrup/cs122-GMG

In order for the program to run, the following packages need to be installed with sudo pip3 install:

bs4
csv
json
matplotlib.pyplot
nltk
? nltk.corpus
? nltk.sentiment.vader
numpy
pitchfork
PIL
random
re
requests
sqlite3
tweepy
twitter
wordcloud
? anything for Django?

Usage
-----
To launch the Django server, run:

python3 manage.py runserver --nothreading

from the DjangoThings/outer_bird directory. 

The Code
--------
The content of the code to run Little Bird is located in the DjangoThings/outer_bird/get_rating directory.

-urls.py : the url dispatcher for the app, works in tandem with views.py to deliver html files
-views.py : processes the url request and renders the appropriate html template
-tweets.py : contains the Tweets and Query classes and functions for streaming and seraching the Twitter API
-tweets_db.py : contains functions for setting up, updating, and querying tweet databases. NOTE: this functionality was not used in the final implementation
-sentiment.py : contains several functions for performing sentiment analysis on tweets
-plots.py : contains functions for creating plots and images related to sentiment analysis of tweets
-doesthething.py : contains the main function that incorporates all the components of querying Twitter and sentiment analysis

Other Directories
-----------------
The repository also have several other directories, some necessary for the implementation, others just to store things not in the final implementation

-DjangoThings/outer_bird/little_bird : just a Django wrapper with a url dispatcher that sends all urls to the get_rating app where the rest of the functional code is

-DjangoThings/outer_bird/get_rating/templates : directory that stores all of the html templates, used by the Django render function to produce the html file returned to the user

-DjangoThings/outer_bird/get_rating/static : stores the images called and the css file 





