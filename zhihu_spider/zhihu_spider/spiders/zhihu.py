# -*- coding: utf-8 -*-
"""
获取知乎所有用户的信息
实现方式为：
以一个关注者比较多的用户（知乎日报）开始，获取他所有的关注者，
然后获取关注者的关注者，依次推下去
"""
import scrapy
import json
import re


class ZhihuSpider(scrapy.Spider):
    name = 'zhihu'
    allowed_domains = ['zhihu.com']
    start_urls = [
        'https://www.zhihu.com/api/v4/members/zhi-hu-ri-bao-51-41/followers?include=data[*].answer_count%2Carticles_count%2Cgender%2Cfollower_count%2Cis_followed%2Cis_following%2Cbadge[%3F(type%3Dbest_answerer)].topics&offset=0&limit=20']

    def parse(self, response):
        # 1.获取当前页面的数据，粉丝的用户信息
        # 转换成json数据
        json_data = json.loads(response.text)
        # if json_data['paging']:
        #     print('is_start:', json_data['paging']['is_start'])
        if json_data['data']:
            for data in json_data['data']:
                # print(data)
                yield data  # 提交给管道文件处理 pipelines

                # 3.获取关注者的关注者，只需要更改url中‘members/zhi-hu-ri-bao-51-41/followers’
                # 中间的‘zhi-hu-ri-bao-51-41’(用户的url_token)就可改为关注者的url
                new_url_token = data['url_token']
                # 提取当前url的url_token，使用正则表达式的findall函数，结果为列表
                old_url_token = re.findall('members/(.*?)/followers', response.url)[0]
                # 替换成新的url
                new_url = re.sub(old_url_token, new_url_token, response.url)
                # 发出请求
                yield scrapy.Request(new_url, callback=self.parse)

        # 2.实现翻页
        if json_data['paging']:
            if not json_data['paging']['is_end']:  # 有下一页
                # 取出下一页网址，但不是完整的
                next_url = json_data['paging']['next']
                # 替换成完整的
                next_url = re.sub('members', 'api/v4/members', next_url)
                # 返回请求 发出请求 -> 得到的响应交给parse函数
                yield scrapy.Request(next_url, callback=self.parse)
