from bs4 import BeautifulSoup
from . import rss_fetch
from .Parsers.atom_parser import AtomParser


class ContentProvider:
    success = None
    fail = None
    resrc = None


    def __check_atom(self, soup):
        if soup.feed is None:
            return False
        else:
            return True
    
    def __check_rss2(self, soup):
        return False

    # Check rss type
    def __check_rss_type(self, soup):
        if self.__check_atom(soup):
            return AtomParser()
        elif self.__check_rss2(soup):
            return 'rss2_parser'
        else:
            print('[*]Not Support')
            return None

    def __parse_user_rss(self):
        content = []
        success = 0
        fail = 0
        none_rec = {}
        none_rec['status'] = None
        none_rec['web_data'] = None

        # Parse FeedName and Link
        # And Fetch The Xml
        # Output : feedname | data
        rss_recs = rss_fetch.fetch_user_rss()
        new_rss_recs = {}
        
        for feed_name in rss_recs:
            old_rec = rss_recs[feed_name]
            # Hndle None Error
            if old_rec == None:
                new_rss_recs[feed_name] = none_rec
                continue

            xml_soup = old_rec['xml_soup']
            # Handle None Error
            if xml_soup is None:
                print("[*]{} feed failed".format(feed_name))
                new_rss_recs[feed_name] = none_rec
                continue
            
            # chose parser
            parser = self.__check_rss_type(xml_soup)

            # pack and pass to parser
            tmp_rec = {}
            tmp_rec['status'] = old_rec['status']
            tmp_rec['xml_soup'] = xml_soup

            # Parse Content and pack
            new_rec = {}
            new_rec['status'] = old_rec['status']
            new_rec['web_data'] = parser.getAll(tmp_rec)
            new_rss_recs[feed_name] = new_rec
            
        # statistics info
        # TODO:Report Failed
        for feed_name in new_rss_recs:
            rec = new_rss_recs[feed_name]
            if rec['web_data'] is None:
                fail += 1
            else:
                success += 1

        
        content.append(success)
        content.append(fail)
        content.append(new_rss_recs)
        
        return content

    def getSiteData(self, feed_name):
        if self.resrc is None:
            print("[*]Error No Resrc")
            return None
        
        if feed_name in self.resrc:
            return self.resrc[feed_name]['web_data']
        
        else:
            print("[-]No Feed Name {}".format(feed_name))
            return None

    def getSiteStatus(self, feed_name):
        if self.resrc is None:
            print("[*]Error No Resrc")
            return None
        
        if feed_name in self.resrc:
            return self.resrc[feed_name]['status']
        
        else:
            print("[-]No Feed Name {}".format(feed_name))
            return None


    def __init__(self):
        result = self.__parse_user_rss()
        self.success = result[0]
        self.fail = result[1]
        self.resrc = result[2]