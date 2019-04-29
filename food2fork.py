from urllib.request import Request, urlopen
import urllib.parse
import json

class Food2ForkClient():
    """
    Castom imlementation of Food2Fork API for recipes retrival.

    Use case:
                from food2fork import Food2ForkClient
                f2fClient = Food2ForkClient('Your Api Key')

                recipes = f2fClient.search('noodles', 'pork')

                # Next page
                moreRecipes = f2fClient.search('noodles', 'pork', 2)
    """

    def __init__(self, apiKey, debug=False):
        self.apiKey = apiKey
        self.debugMode = debug

        self.SEARCH = 'http://food2fork.com/api/search'
        self.VIEW = 'http://food2fork.com/api/get'

    def search(self, query, page=1):
        try:
            url = self.urlHelper(self.SEARCH, q=query, page=page)

            contents = self.getUrlContents(url)

            data = json.loads(contents)

            if self.debugMode:
                print(contents)

            return data

        except Exception as instance:
            if self.debugMode:
                print(instance)

            return None

    def urlHelper(self, endpoint, **kwargs):
        """
        Build Url for POST request
        :param endpoint:
        :param kwargs:
        :return:
        """
        data = {'key': self.apiKey}

        for key, value in kwargs.items():
            data[key] = value

        if self.debugMode:
            print('Url: ', endpoint + '?' + urllib.parse.urlencode(data))

        return endpoint + '?' + urllib.parse.urlencode(data)

    def getUrlContents(self, url):
        """
        Decypher url contents
        :param url:
        :return:
        """
        try:
            req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            contents = urlopen(req).read()
            return contents

        except Exception as instance:
            if self.debugMode:
                print(instance)

            return None