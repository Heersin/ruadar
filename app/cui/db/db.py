from peewee import *

usr_db = SqliteDatabase('./feed.db')

class BaseModel(Model):
    class Meta:
        database = usr_db

class Feed(BaseModel):
    feed_name = CharField()
    feed_link = CharField()
    #avoid conflict
    update_ = CharField(default="Unknown", column_name='update')
    group_ = CharField(default="All", column_name='group')

class Article(BaseModel):
    title = CharField()
    update_ = CharField(column_name='update')
    summary = CharField()
    link = CharField(null=True)
    feed_name = CharField()

def init_db(rss_filename=None):
    usr_db.connect()
    usr_db.create_tables([Feed, Article])

    if rss_filename == None:
        return usr_db
 
    with open(rss_filename, encoding='utf-8') as f:
        raw_records = f.readlines()
    
    appear_name = []
    cur_feeds = Feed.select(Feed.feed_name).distinct()
    for feed in cur_feeds:
        appear_name.append(feed.feed_name)


    for index in range(len(raw_records)):
        record = raw_records[index]
        pairs = record.split('|%|')
        rss_name = pairs[0]
        rss_link = pairs[1]
        rss_group = pairs[2]

        '''
        # To avoid corruption
        if rss_name in appear_name:
            rss_name = rss_name + str(index)
        appear_name.append(rss_name)
        '''
        if rss_name in appear_name:
            continue

        feed_rec = Feed(feed_name=rss_name, feed_link=rss_link, group_=rss_group)
        feed_rec.save()
    
    usr_db.close()
    return usr_db