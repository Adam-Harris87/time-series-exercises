import numpy as np
import pandas as pd
import requests

def get_sw_data(url):
    '''
    this function will return a dataFrame with all of the results from the passed url
    until the last page of results
    '''
    # create request.get for passed url
    page = requests.get(url)
    # create a dataframe withe the first page results
    df = pd.DataFrame(page.json()['results'])
    # loop through all pages of results for passed url
    while page.json()['next']:
        # set the page url to the next page url
        url = page.json()['next']
        page = requests.get(url)
        df = pd.concat([df, pd.DataFrame(page.json()['results'])], axis=0)
    # return the datframe
    return df.reset_index().drop(columns='index')

#----------------------------------------------------------------

def get_sw_people():
    '''
    this function will acquire a dataframe of star wars characters from the star wars api
    '''
    # set star wars api url
    people_url = 'https://swapi.dev/api/people'
    # retreive the data
    people = get_sw_data(people_url)
    # return the dataframe
    return people

#----------------------------------------------------------------

def get_sw_planets():
    '''
    this function will acquire a dataframe of star wars planets from the star wars api
    '''
    # set the url to the starwars api
    planets_url = 'https://swapi.dev/api/planets/'
    # create a dataframe of planets
    planets = get_sw_data(planets_url)
    # return the planets
    return planets

#----------------------------------------------------------------

def get_sw_starships():
    '''
    this function will acquire a dataframe of star wars planets from the star wars api
    '''
    # set the url to the starwars api
    starships_url = 'https://swapi.dev/api/starships/'
    # create the dataframe of starships
    starships = get_sw_data(starships_url)
    # return the dataframe
    return starships

#----------------------------------------------------------------

def send_sw_data_to_csv(people, planets, starships):
    '''
    this function will create csv files of the people, planets and starships dataframes
    '''
    people.to_csv('sw_people.csv')
    planets.to_csv('sw_planets.csv')
    starships.to_csv('sw_starships.csv')

#----------------------------------------------------------------

def combine_sw_dfs(people, planets, starships):
    '''
    this function will take in dataframes containing people, planets and starships.
    it will combine the 3 dataframes into one and return the combined df.
    '''
    # combine people and planets on homeworld
    people_planet = pd.merge(left=people, right=planets, how='left', 
                        left_on='homeworld', right_on='url',
                        suffixes=('_people', '_planet'))
    # explode out the lists of starships
    ships = people_planet.starships.explode()
    # combine the exploded list with people_planets
    people_planets_exploded = pd.merge(right=ships, 
                                       left=people_planet, how='left',
                                       left_on=people_planet.index, 
                                       right_on=ships.index)
    # combine people_planets with exploded starship lists with starships df
    combined = pd.merge(left=people_planets_exploded, 
                        right=starships, how='left', 
                        left_on='starships_y', right_on='url',
                        suffixes=('_people', '_starship'))
    # return the combined df
    return combined

#----------------------------------------------------------------

def get_germany():
    '''
    this function will get a dataset of Open Power Systems Data for Germany and return it 
    as a dataframe
    '''
    # get the germany data
    germany = pd.read_csv(
    'https://raw.githubusercontent.com/jenfly/opsd/master/opsd_germany_daily.csv')
    # return the dataframe
    return germany