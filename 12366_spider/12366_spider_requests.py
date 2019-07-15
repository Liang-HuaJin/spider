# -*- coding: utf-8 -*-
"""
@author: KIM
@time: 2019/7/12
@dese: 使用requests爬取12366的热点问题，post方法
"""
import requests
import re


def get_html(url, form_data):
    """
    发起request请求，获取请求数据
    :param url:
    :param form_data:
    :return:
    """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'
    }
    response = requests.post(url, data=form_data, headers=headers)
    return eval(response.text) if str(response.status_code).startswith('2') else None


def get_detail_url_list(url, form_data):
    """
    解析列表页，获取下一页的form data及问题详情页的form data
    :param url:
    :param form_data:
    :return:
    """
    response = get_html(url, form_data)
    # response = eval(response.content.decode('utf-8'))
    if not response:
        print('请求失败')
        return
    # 1.解析列表页，如果不是尾页，就修改form_data字典中的page，使其加1就是下一页需要的form data
    if response['cupage'] == response['pageCount']:
        next_url = None
    else:
        next_url = url
        form_data['page'] += 1
    # 2.获取请求问题url需要的form data，即response['data]中的'BH'
    data = response['data']  # 列表,其中元素为字典
    detail_datas = []
    for i in data:
        detail_datas.append(i['BH'])
    return next_url, form_data, detail_datas


def parse_detail(url, form_data):
    """
    解析问题详情页，提取问题和答案
    :param url:
    :param form_data:
    :return:
    """
    response = get_html(url, form_data)
    if response['bean']:
        title = response['bean']['ZLTITLE']
        answer = response['bean']['ZLNR']
        answer = re.sub("[A-Za-z\&\%\<\>\;\/\[\]]", '', answer)
        print('*' * 30)
        print(title)
        print(answer)


def spider():
    """
    启动爬虫函数
    next_url: 问题列表的url
    form_data： psot请求问题列表需要的数据
    detail_url： 问题详情页面的url
    detail_form_data： psot请求问题详情页面需要的数据
    :return:
    """
    next_url = 'https://12366.chinatax.gov.cn/sscx/rdzs'
    form_data = {'page': 635, 'pageSize': 10, 'bqtype': ''}
    detail_url = 'https://12366.chinatax.gov.cn/sscx/toDetail'
    detail_form_data = {'code': '', 'gjz': '', 'ip': ''}
    while next_url:
        next_url, form_data, detail_datas = get_detail_url_list(next_url, form_data)
        for data in detail_datas:
            detail_form_data['code'] = data
            parse_detail(detail_url, detail_form_data)


if __name__ == '__main__':
    import time

    start_time = time.time()
    spider()
    print("sum_time = {}".format(time.time() - start_time))
