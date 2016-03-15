# This code allows the user to set up a database in order to store the 
# collected tweets. It was not ultimately used as a part of LittleBird,
# however it was included because it may be useful if this project is 
# expanded. 


import sqlite3
import re
import get_rating.tweets

def create_db(db_name, table_schemas):
    '''
    Creates a sqlite database 

    Inputs:
        db_name: name of the new database
        table_schemas: a dictionary where keys are names of
            the tables in the database and values are lists 
            of the column names for each table.
    '''
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    for table in table_schemas:
        cols = ', '.join(table_schemas[table])
        c.execute('CREATE TABLE {} ({})'.format(table, cols)) 
    conn.commit()
    conn.close()
    return 

def update_tweets_table(db, table, columns, tweet):
    '''
    Updates a database with information about tweets. The database must
    have a table for storing tweet information with a column for the tweet 
    text, a column for the tweet data, and a column for the tweet id
    Inputs:
        db: the name of the database to store tweet text and dates into
        table: the name of the table in the database to store tweet text
            and dates into
        columns: a list of the column names of the table 
        tweet: a Tweet object 
    '''
    conn = sqlite3.connect(db)
    c = conn.cursor()
    cols = ','.join(columns)
    command = 'INSERT INTO {} ({}) VALUES '.format(table, cols)
    values = '''("{}", "{}", "{}")'''.format(tweet.id, tweet.text, tweet.date)
    c.execute(command + values)
    conn.commit()
    conn.close()
    return

def is_match(search, text):
    '''
    Identifies if a search term is located in text

    Inputs:
        search: a string of the term you a searching for
        text: the text you are looking for the search term
            in
    Returns: boolean
    '''
    match = re.findall(search, text)
    if match == []:
        return False
    return True

def search_db(db, table, col, query):
    '''
    Searches a tweets database for entries matching
    a specified query. When a tweet is found to contain 
    the query term, the tweet is added to the tweets attribute
    of the query 

    Inputs:
        db: name of the database
        table: name of the table in the database
        col: the name of the column in the table containing
            tweet text
        query: a Query object 
    '''
    search = 'SELECT {} FROM {} WHERE is_match("{}", {})'.format(col, table, query.term, col)
    conn = sqlite3.connect(db)
    conn.create_function("is_match", 2, is_match)
    c = conn.cursor()
    r = c.execute(search)
    results = r.fetchall()
    for result in results:
        tweet = tweets.Tweet(result[0])
        query.add_tweet(tweet)
    return




