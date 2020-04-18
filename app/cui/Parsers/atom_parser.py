from bs4 import BeautifulSoup
from .base_parser import BaseParser

class AtomParser(BaseParser):

    def getAuthor(self, author_tag):
        # May have more than 1 author.
        author_list = []
        AUTHOR_NOT_FOUND = False

        for author in author_tag:
            author_info = {}
            try:
                author_info['name'] = str(author.find('name').string.encode('utf-8'), encoding='utf-8')
            except:
                print('[-]Warning:Maybe A Broken seed')
                author_info['name'] = None
                AUTHOR_NOT_FOUND = True

            mail_addr = author.email
            if mail_addr == None:
                author_info['mail'] = None
            else:
                author_info['mail'] = str(mail_addr.string.encode('utf-8'), encoding='utf-8')
            
            author_list.append(author_info)
        
        # If More than one author or cannot find author tag,
        # we chose title as author later
        if (len(author_list) > 1) or AUTHOR_NOT_FOUND:
            author_info['name'] = None
            author_info['mail'] = author_list[0]['mail']
        
        else:
            author_info = author_list[0]

        return author_info
    
    def getSummary(self, tag):
        if tag == None:
            return None
        return str(tag.string.encode('utf-8'), encoding='utf-8')

    def getLink(self, tag):
        if tag == None:
            return None
        return tag['href']

    
    # Func: Get Title of this page, Use as Author
    # Output: Title String
    # PS : None When Nothing
    def getTitle(self, title_tag):
        if title_tag == None:
            return None
        return str(title_tag.string.encode('utf-8'), encoding='utf-8')   

    # Func: Get the last update Time of this web page
    # Output: Update Time
    # PS : None When Nothing
    def getUpdate(self, tag):
        if tag == None:
            return None
        return str(tag.string.encode('utf-8'), encoding='utf-8')

    
    # Func: Get Article Item
    # Output : A Dict For Article Item
    #           |
    #           |-------> {
    #                       'title' : 'xxx',
    #                       'update' : 'xxx',
    #                       'summary' : 'xxx',
    #                       'link' : 'xxx',
    # }
    # PS : None When Nothing
    def getArticle(self, entry):
        if entry is None:
            return None

        entry_item = {}
        
        try:
            entry_item['title'] = self.getTitle(entry.title)
            entry_item['update'] = self.getUpdate(entry.updated)
        except:
            print('[-]Error : May be A broken seed')
            entry_item['title'] = None
            entry_item['update'] = None

        entry_item['summary'] = self.getSummary(entry.summary)
        entry_item['link'] = self.getLink(entry.link)
        return entry_item

    
    # Func: Article List
    # Output : A List of Article
    def getArticleList(self, entry_tags):
        articles = []

        for entry in entry_tags:
            entry_item = self.getArticle(entry)
            articles.append(entry_item)
        
        return articles

    
    # Func: Pack All Required Elements
    # Output: A Dict About this site, The following Elements is required!
    #               |
    #               |
    #               |----> { 'title': 'xxx',
    #                        'author' : {},
    #                        'update' : 'xxx',
    #                        'articles' : [{},{},{}...]
    # }
    def getAll(self, rss_record):
        website_rec = {}
        status = rss_record['status']
        soup = rss_record['xml_soup']


        if status != 200:
            print("Bad Status Code")
            return None
        
        # ======== Site Required ===============
        # ==> Title
        # ==> Update
        try:
            website_rec['title'] = str(soup.title.string.encode('utf-8'),encoding='utf-8')
            website_rec['update'] = str(soup.updated.string.encode('utf-8'), encoding='utf-8')
        except:
            print("[-]Error : This Site Feed Has Been Broken")


        # ======== Recommend  ===============
        # ==> Author
        author_tag = soup.find_all('author')
        author = self.getAuthor(author_tag)
        if author['name'] is None:
            author['name'] = website_rec['title']
        website_rec['author'] = author


        # ======== Optional Here =============
        # ==> Articles(Remember check None in DataProvider)
        entry_tags = soup.find_all('entry')
        articles = self.getArticleList(entry_tags)
        website_rec['articles'] = articles

        return website_rec
        