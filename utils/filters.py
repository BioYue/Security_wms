from datetime import datetime
import re


def strftime(date):
    # 格式化日期和时间保留 23年 12月05日 22:23
    return date.strftime('%y年 %m月%d日 %H:%M')


def strftime_comment(date):
    # 格式化评论区的时间
    return date.strftime('%m月%d日 %H:%M')


def address(data):
    # 国家|区域|省份|城市|ISP
    list_ = data.split('|')
    return list_[2] + list_[3]


def remove_html_tags(text):
    # 去除文章内容的html标签
    clean = re.compile('<.*?>')
    return re.sub(clean, '', text)


FILTERS = {
    'strftime': strftime,
    'strftime_comment': strftime_comment,
    'address': address,
    'remove_html_tags': remove_html_tags
}
