# -*- coding: utf-8 -*-
import scrapy
import re


class QuestionSpiderSpider(scrapy.Spider):
    name = 'question_spider'
    allowed_domains = ['12366.chinatax.gov.cn']
    start_urls = ['https://12366.chinatax.gov.cn/sscx/rdzs']
    form_data = {'page': '635', 'pageSize': '10', 'bqtype': ''}
    detail_url = 'https://12366.chinatax.gov.cn/sscx/toDetail'
    detail_form_data = {'code': '', 'gjz': '', 'ip': ''}

    def start_requests(self):
        """
        重写Spider类的start_requests函数，使程序一开始就发送post请求
        :return:
        """
        yield scrapy.FormRequest(
            url=self.start_urls[0],
            formdata=self.form_data,
            callback=self.parse
        )

    def parse(self, response):
        # 1.解析页面，获取请求问题url需要的form data，即response.text['data]中的'BH'
        response = eval(response.text)
        datas = response['data']
        for data in datas:
            self.detail_form_data['code'] = data['BH']
            yield scrapy.FormRequest(
                url=self.detail_url,
                formdata=self.detail_form_data,
                callback=self.parse_detail
            )

        # 2.解析列表页，如果不是尾页，就修改form_data字典中的page，使其加1就是下一页需要的form data
        if response['cupage'] != response['pageCount']:
            self.form_data['page'] += str(1)
            yield scrapy.FormRequest(
                url=self.start_urls[0],
                formdata=self.form_data,
                callback=self.parse
            )

    def parse_detail(self, response):
        response = eval(response.text)
        if response['bean']:
            data = {}
            data['title'] = response['bean']['ZLTITLE']
            answer = response['bean']['ZLNR']
            data['answer'] = re.sub("[A-Za-z\&\%\<\>\;\/\[\]]", '', answer)
            yield data
