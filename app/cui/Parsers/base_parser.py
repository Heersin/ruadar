from bs4 import BeautifulSoup
from abc import ABCMeta, abstractmethod

class BaseParser:
    # ============== Required ==================================
    # Func: Extract Info About Author
    # Output: A Dict For Author Info | Dict
    #               |
    #               |-----> {'name':'xxx',
    #                        'mail':'xxx'}
    # PS: None When No Author tag detect,later use title as author
    @abstractmethod
    def getAuthor(self, tag):
        pass

    # Func: Get Title of this page, Use as Author
    # Output: Title String
    # PS : None When Nothing
    @abstractmethod
    def getTitle(self, tag):
        pass

    # Func: Get the last update Time of this web page
    # Output: Update Time
    # PS : None When Nothing
    @abstractmethod
    def getUpdate(self, tag):
        pass

    
    # Func: Get Article Item
    # Output : A Dict For Article Item
    #           |
    #           |-------> {
    #                       'title' : 'xxx',
    #                       'summary' : 'xxx',
    #                       'link' : 'xxx',
    #                       'update' : 'xxx',
    # }
    # PS : None When Nothing
    @abstractmethod
    def getArticle(self, tag):
        pass
    
    # Func: Article List
    # Output : A List of Article
    @abstractmethod
    def getArticleList(self, tag):
        pass

    
    # Func: Pack All Required Elements
    # Output: A Dict About this site, The following Elements is required!
    #               |
    #               |
    #               |----> { 'title': 'xxx',
    #                        'author' : {},
    #                        'update' : 'xxx',
    #                        'articles' : [{},{},{}...]
    # }
    @abstractmethod
    def getAll(self, tag):
        pass


