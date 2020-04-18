from app import get_logger, get_config
import math
from flask import render_template, redirect, url_for, flash, request
from flask_login import login_required
from . import admin
import os
from app import cui

logger = get_logger(__name__)
cfg = get_config()


# 根目录跳转
@admin.route('/', methods=['GET'])
def root():
    return redirect(url_for('main.index'))


# 首页
@admin.route('/index', methods=['GET'])
def index():
    feed_dict = cui.get_group_info_for_nav()
    articles = cui.get_all_articles()
    return render_template('admin/index.html', feed_dict=feed_dict, articles=articles)

# feeds
@admin.route('/feed/<feed_name>', methods=['GET'])
def view_feed(feed_name):
    feed_dict = cui.get_group_info_for_nav()
    articles = cui.get_article_by_feed_name(feed_name)
    if articles is None:
        articles = []
    
    return render_template('admin/feed.html', articles=articles, feed_dict=feed_dict)

# show feedlist of <group_name>
@admin.route('/feedlist/<group_name>', methods=['GET'])
def list_feed(group_name):
    feed_list = cui.get_feed_list(group_name)
    feed_dict = cui.get_group_info_for_nav()
    if feed_list is None:
        feed_list = []

    return render_template('admin/feedlist.html', feeds=feed_list, feed_dict=feed_dict)

# show articles in a group
@admin.route('/group/<group_name>', methods=['GET'])
def view_group(group_name):
    feed_dict = cui.get_group_info_for_nav()
    articles = cui.get_article_by_group(group_name)
    if articles is None:
        articles = []
    
    return render_template('admin/group.html', articles=articles, feed_dict=feed_dict)


@admin.route('/grouplist', methods=['GET'])
def list_group():
    groups = cui.get_group_list()
    feed_dict = cui.get_group_info_for_nav()
    if groups == None:
        groups = []
    return render_template('admin/grouplist.html', groups=groups, feed_dict=feed_dict)



