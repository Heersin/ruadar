import urllib.request
from bs4 import BeautifulSoup
from .db.db import Feed

'''
Get resource from the given rss_url
Arg: rss_url
Return: a rss resource record(rssRR)
rssRR:
	status -- the request server status
	headers -- the response headers
	xml -- the XML content
'''
# Need Rewrite to deal the 404
def fetch_single_rss(rss_url):
	rss_result = {}
	try:
		rss_response = urllib.request.urlopen(rss_url)
		rss_result['status']  = rss_response.status
		rss_result['headers'] = rss_response.getheaders()
		xml = rss_response.read()
	except:
		print("[*]Fetch Single Rss Faild {}".format(rss_url))
		rss_result['status'] = '404'
		rss_result['headers'] = None
		rss_result['xml_soup'] = None
		xml = None

	if xml is None:
		return None

	xml_soup = BeautifulSoup(xml, 'xml')
	rss_result['xml_soup'] = xml_soup
	
	return rss_result


# Read From db
def fetch_user_rss():
	resrc_dict = {}
	query = Feed.select()
	for feed in query:
		result = fetch_single_rss(feed.feed_link)
		resrc_dict[feed.feed_name] = result
		
	return resrc_dict


def fetch_original(link):
	original_result = {}
	try:
		response = urllib.request.urlopen(link)
	except:
		print("[Response Error]")
		return None
	
	original_result['status'] = response.status
	original_result['header'] = response.getheaders()
	html = response.read()

	return html
