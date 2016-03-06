import sqlite3
import re
import get_rating.tweets

def create_db(db_name, table_schemas):
    '''
    Inputs:
        db_name: name of the new database
        table_schemas: dictionary. Keys are names of
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

def update_tweets_table(db, table, columns, tweet_text, tweet_date):
    '''
    Write a function that will add on new tweet text and new
    tweet ids to the tweets table. Think about the issue of 
    how to make this function stop eventually.
    '''
    conn = sqlite3.connect(db)
    c = conn.cursor()
    cols = ','.join(columns)
    command = 'INSERT INTO {} ({}) VALUES '.format(table, cols)
    values = '''("{}", "{}")'''.format(tweet_text, tweet_date)
    c.execute(command + values)
    conn.commit()
    conn.close()
    return

def is_match(search, text):
    match = re.findall(search, text)
    if match == []:
        return False
    return True

def search_db(db, table, col, query):
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




