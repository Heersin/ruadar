# Command Line Reader
from .rss_content import ContentProvider
from . import rss_config
from . import rss_fetch
from .db import db
from .db.db import Article,Feed
import os

def should_I_update_site(db_site, update):
    if db_site.update_ == update:
        return False
    else:
        return True

def try_get_article(title, feed_name):
    db_article = Article.select().where((Article.title == title) & (Article.feed_name == feed_name)) 
    if db_article.count() == 0:
        return None
    else:
        return db_article.get()

def get_article_by_feed_name(feed_name):
    db_article = Article.select().where((Article.feed_name == feed_name)) 
    if db_article.count() == 0:
        return None
    else:
        return db_article

def get_feed_list(group_name):
    db_feeds = Feed.select().where((Feed.group_ == group_name))
    print('[group name] {} '.format(group_name))
    if db_feeds.count() == 0:
        print("no group")
        return None
    else:
        return db_feeds


def get_article_by_group(group_name):
    feed_list = get_feed_list(group_name)
    if feed_list.count() == 0:
        print("no such group")
        return None
    
    result = []
    for feed in feed_list:
        articles = get_article_by_feed_name(feed.feed_name)
        for article in articles:
            result.append(article)

    return result


def get_group_list():
    db_groups = Feed.select(Feed.group_).distinct()
    groups = []
    for group in db_groups:
        print('[group_list] : ')
        print(group.group_)
        groups.append(group.group_)
    return groups

def get_group_info_for_nav():
    groups = get_group_list()
    result = {}
    for group in groups:
        result[group] = get_feed_list(group)
    return result

def get_all_articles():
    db_articles = Article.select()
    return db_articles

def should_I_update_article(db_article, update):
    if db_article.update_ == update:
        return False
    return True


def store_original(db_article, original):
    store_dir = rss_config.store_dir
    feed_name = db_article.feed_name
    cur_feed = Feed.get(Feed.feed_name == feed_name)

    # Decode original
    original = original.decode('utf-8')

    if cur_feed.group_ == 'All':
        mid_dir = ''
    else:
        mid_dir = cur_feed.group_
    path = store_dir + '/' + mid_dir + '/' + feed_name + '##' + db_article.title + '.html'

    if original is None:
        print("[*]Not Store For None")
        return None
    with open(path, 'w', encoding='utf-8') as f:
        f.write(original)
    
    print("[*]Log: Store 1 File")

def grab_notnone_articles(feed_name, not_none_articles):
    for i in range(len(not_none_articles)):
        print("==============%dth==================" %i)
        article = not_none_articles[i]

        title = article['title']
        update_time = article['update']
        link = article['link']
        summary = article['summary']

        print("Title => %s " %title)
        print("Update Time => %s" %update_time)
        print("Origin Link => %s" %link)
        print("Summary => %s" %summary)

        # If This Article is not in our database
        # ---> feed_name & title
        db_article = try_get_article(feed_name, title)

        if db_article is None:
            art_rec = Article(title=title, update_=update_time, summary=summary,link=link, feed_name=feed_name)
            art_rec.save()
            #original = rss_fetch.fetch_original(link)
            #store_original(art_rec, original)
        elif should_I_update_article(db_article, update_time) is True:
            db_article.update_ = update_time
            db_article.save()
            #original = rss_fetch.fetch_original(link)
            #store_original(db_article, original)
        else:
            continue

def run_reader_session():
    rss_file = rss_config.rss_file_path
    usr_db = db.init_db(rss_file)
    usr_db.connect()
    
    provider = ContentProvider()
    success = provider.success
    fail = provider.fail
    resrc = provider.resrc
    
    for feed_name in resrc:
        print("=====================================")
        print(feed_name)
        print("=====================================")
        site_data = provider.getSiteData(feed_name)
        site_status = provider.getSiteStatus(feed_name)
        
        if(site_data == None):
            print("[*]Main.py: Broken , Status {}".format(site_status))
            continue
            
        title = site_data['title']
        update = site_data['update']
        author_name = site_data['author']['name']
        author_mail = site_data['author']['mail']
        
        # Only One Record Will Return
        db_site = Feed.get(Feed.feed_name == feed_name)
        
        # Check If We should Update This Site
        if should_I_update_site(db_site, update) is False:
            print("[*]Log: Ignore Site {}".format(feed_name))
            continue
        else:
            print("[*]Log: Should Update Site {}".format(feed_name))
            db_site.update_ = update
            db_site.save()
            
        print("title => " + title)
        print("Update => " + update)
        print("Author => " + author_name)
        
        # Wash None Articles
        articles = site_data['articles']
        not_none_articles = []
        for article in articles:
            if article is None:
                continue
            else:
                not_none_articles.append(article)
                
        # Show Article and Store
        grab_notnone_articles(feed_name, not_none_articles)

    # close db
    usr_db.close()
    return success, fail


if __name__ == "__main__":
    success, fail = run_reader_session()