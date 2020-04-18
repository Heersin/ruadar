# Struct

```
1. Parser -- For different RSS Format

2. Webui -- Todo, act with Web

3. Contents -- Store the rss list and other contents
        |
        |----Support Group

4. Main Directory
    |
    |---- main.py
    |
    |---- rss_config.py -> some configs
    |
    |---- fetch_rss.py -> The net spider part 
    |
    |---- content_provider.py -> parse the rss

```


# Step
1. fetch_rss.py --> Read List and Fetch the data
2. content_provider --> parse the data and output
3. main.py --> show the data


# Ref
1. 比较atom与rss2：http://www.intertwingly.net/wiki/pie/Rss20AndAtom10Compared

2. 二者比较的表格：https://www.imooc.com/article/28992

3. rss2的规范 <a href=https://www.cnblogs.com/bugsharp/articles/350392.html>中文 </a> <a href=http://blogs.law.harvard.edu/tech/rss> English</a>
