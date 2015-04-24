'''
Created on Apr 18, 2015

@author: Mike

pulls data out from weather underground and converts it into a dictionary structure

Inputs: (location information, features)
    Location information:
        City/State:
            If you want to get the WU data based on the the city name and the sate/country
            three inputs are requred city (string),state (string),features (string or list)
            example: a = WuAPI('canton', 'ma', 'forecast')
        Zipcode:
            If you want to get the WU data based on the cities zipcode only two inputs are
            required, zipcode (string), features (string or list)
            example: a = WuAPI('02021', 'forecast')
    Features (string or list):
        This is the list of features that you want to pull from WU data and be either a 
        string for a single feature or a list of many features.
        List of features and their responses can be found in following link:
        http://www.wunderground.com/weather/api/d/docs?d=data/index 
        
Output:
    self.parsed_json is the results from the query request in a dictionary
'''
from urllib.request import urlopen

import json


class WuAPI(object):

    API_KEY = '603255bdafa80256'

    def __init__(self, *args):
        if len(args) == 3:
            self.CityStateQuery(args[0], args[1], args[2])
        elif len(args) == 2:
            self.ZipcodeQuery(args[0], args[1])
        self.exicuteWUAPI(self.queryStr)
                
    
    def CityStateQuery (self,city, state, feature):
        self.BuildFeatureStr(feature)
        self.queryStr = 'http://api.wunderground.com/api/' +self.API_KEY+ '/' + self.featureStr + '/q/' + state+ '/' +city+ '.json'
        

    def ZipcodeQuery(self, zipcode, feature):   
        feature = self.BuildFeatureStr(feature)
        self.queryStr = 'http://api.wunderground.com/api/' +self.API_KEY+ '/' + self.featureStr + '/q/' +zipcode+ '.json'
        
    def exicuteWUAPI(self, queryStr):
        results = urlopen(queryStr)

        json_string = results.read().decode('utf-8')
        results.close()
        self.parsed_json = json.loads(json_string)


    def BuildFeatureStr(self, featureLst):
        if isinstance(featureLst, list):
            self.featureStr = ''
            for i in range(len(featureLst)):
                self.featureStr += featureLst[i]
                if i != len(featureLst)-1:
                    self.featureStr += '/'
        else:
            self.featureStr = featureLst
        
if __name__=="__main__":
    a = WuAPI("canton", "ma", ['geolookup' ,'conditions'])
    print("Current temperature in %s is: %s" % (a.parsed_json['location']['city'], a.parsed_json['current_observation']['temp_f']))
    b = WuAPI('02090', ['geolookup' ,'conditions'])
    print("Current temperature in %s is: %s" % (b.parsed_json['location']['city'], b.parsed_json['current_observation']['temp_f']))