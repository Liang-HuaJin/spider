# -*- coding: utf-8 -*-
"""
@author: KIM
@time: 2019/7/12
@dese: 使用requests爬取12366的热点问题，post方法
"""
import requests
import re


def get_html(url, form_data):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'
    }
    response = requests.post(url, data=form_data, headers=headers)
    return eval(response.text) if str(response.status_code).startswith('2') else None


def get_detail_url_list(url, form_data):
    response = get_html(url, form_data)
    # response = eval(response.content.decode('utf-8'))
    if not response:
        print('请求失败')
        return
    # 2.解析列表页，如果不是尾页，就修改form_data字典中的page，使其加1就是下一页需要的form data
    if response['cupage'] == response['pageCount']:
        next_url = None
    else:
        next_url = url
        form_data['page'] += 1
    # 3.获取请求问题url需要的form data，response['data]中的'BH'和'TSLX'
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
    title = response['bean']['ZLTITLE']
    answer = response['bean']['ZLNR']
    answer = answer.replace('&rdquo;', '')
    answer = answer.replace('&ldquo;', '')
    answer = answer.replace('&nbsp;', '')
    answer = answer.replace('<br/>', '')
    answer = answer.replace('<br />', '')
    print('*'*30)
    print(title)
    print(answer)


def spider():
    """
    启动爬虫函数
    :return:
    """
    next_url = 'https://12366.chinatax.gov.cn/sscx/rdzs'
    form_data = {'page': 636, 'pageSize': 10, 'bqtype': ''}
    detail_url = 'https://12366.chinatax.gov.cn/sscx/toDetail'
    detail_form_data = {'code': '', 'gjz': '', 'ip': ''}
    while next_url:
        next_url, form_data, detail_datas = get_detail_url_list(next_url, form_data)
        for data in detail_datas:
            detail_form_data['code'] = data
            parse_detail(detail_url, detail_form_data)


if __name__ == '__main__':
    spider()
