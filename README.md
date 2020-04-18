# Ruadar
## Description
Web-based Rss Reader, Set in server and access from terminal devices.

## Features
- easy setup
- access from everywhere by web
- group feeds

The Demo Page as follows<br>
![example](https://github.com/Heersin/ruadar/blob/master/log/example.png)

## Install
A virtual environment is recommended, I choose virtualenv.
```
mkdir venv
virtualenv venv
source venv/bin/activate
``` 
In this virtual environment, install the third-party libs
```
pip install -r requirements.txt
```

## Usage
Modify your rss_list.txt in cui/content/, the format of every record is :
```
[rss name]|%|[rss link]|%|[group]
example : xxx|%|htttp://xxx.com/rss.xml|%|Group1
```

start your virtual environment, use the following command to start server
```
python manage.py runserver (start server in 0.0.0.0:5000)
or 
python run_app_dev.py (start server in 127.0.0.1:5000)
```

For keeping running in server, you can use start.sh
```
sh start.sh
```
But I recommend using Screen
```
Screen -S ruadar
source venv/bin/activate
python manage.py runserver
```

use Ctrl-D to leave it back, Screen -R rudar to resotre.

## How it works?
Well, it's quite simple and straightfoward. The backend program read rss feed list and init database when you run this project in the first time. And Then it will fetch these rss feeds, and detect the protocol of this rss feed. after all those things,  it's time to parse the rss.<br>
I create a class named ContentProvider to pack the data, and use some methods to read and write from database, and provide data to our web ui.<br>
To write a new parser and apply, inherit the base_parser and modify 2 places:
1. rss_content : __check_rss_type() (modify method) & __check_[typename]()  (add this method)

2. your parser file in app/cui/Parsers

## Contribute
If you have a better parser to parse different types of RSS file, you can write code and tell me or open an issue for new features~
