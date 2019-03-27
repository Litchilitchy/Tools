#coding=utf-8
import spider.spiders.prep as prep
import scrapy
import re
import os

from spider.items import SpiderItem
class GovSpider(scrapy.Spider):
    name = 'spider'
    allowed_domains = ["com"]

    start_urls = prep.get_start_url()

    '''start_urls = [
        "http://www.dmoz.org/Computers/Programming/Languages/Python/Books/",
        "http://www.dmoz.org/Computers/Programming/Languages/Python/Resources/"
    ]
    '''
    def __init__(self, OP=None, ED=None, SD=None):
        super(GovSpider, self).__init__()
        self.b_time = OP
        self.e_time = ED
        if SD != None:
            self.out_dir = SD

        self.DICT = prep.PatternDict()

    def parse(self, response):
        #ilename = response.url.split("/")[-2]
        #f = open(filename, 'wb')


        print("is dynamic page>>>>>>>")
        '''with open(filename, 'wb') as f:
            c = response.body
            f.write(c)      
        '''

        '''
        for sel in response.xpath('//ul/li'):
            title = sel.xpath('a/text()').extract()
            link = sel.xpath('a/@href').extract()
            desc = sel.xpath('text()').extract()
            print(title, link, desc)
        '''

        url_list = []
        # parent page

        # next_pattern = r'<a[^a]*?htm">下一页</a>'
        #f.write(response.body)
        # next_obj = re.search(next_pattern, response.body.decode('utf-8'))


        '''
        if next_obj:

            next_url = next_obj.group(0)
            print(next_url)
            next_pattern = r'".*?\.htm"'
            next_obj = re.search(next_pattern, next_url)
            if next_obj:
                next_url = next_obj.group(0).strip('\"')

            domain_url = None
            if 'domain' in response.meta:
                next_url = response.meta['domain'] + next_url
                domain_url = response.meta['domain']
            else:
                next_url = response.urljoin(next_url)
                domain_url = response.url
            print ("next_url>>>>>>>>>>>>>>>>>>>>")
            print (next_url)
            #os.system("pause")
            request = scrapy.Request(next_url,
                    meta={'domain': domain_url}, dont_filter=True)
            # request.meta['PhantomJS'] = True
            yield request
        '''



        # content page
        content_len = len(response.xpath('//div[@id="content"]').extract())
        domain_obj = re.search(r"(?<=www\.)[^\.]*", response.url)
        assert domain_obj
        domain_name = domain_obj.group(0)


        if content_len == 0:
            # parent page
            # print (content_len)
            # print ("no content")
            print("this url >>>>>", response.url)
            next_pattern = self.DICT.get_pattern(domain_name, 6)

            request = None
            # get pattern 7-page total
            if 'domain' in response.meta:
                page_num = int(response.meta['page']) + 1
                next_url = response.meta['domain'] + next_pattern + str(page_num) + r'.htm'
                print(next_url)
                #os.system("pause")
                page_total = self.DICT.get_pattern(domain_name, 7)
                if page_num <= int(page_total):
                    request = scrapy.Request(next_url,
                                         meta={'domain': response.meta['domain'], 'page': page_num}, dont_filter=True)

            else:
                next_url = response.url + next_pattern + r'1.htm'
                print(next_url)
                #os.system("pause")
                request = scrapy.Request(next_url,
                                         meta={'domain': response.url, 'page': '1'}, dont_filter=True)
            yield request

            for sel in response.xpath('//tr[@class="tr1"]').extract():
                #print(">>>>>><<<<<><><><><><>>>" + str(sel))
                link_re = re.compile('window.open\(\'' + '(.*)' + '\'\)')
                link = str(link_re.findall(sel)).replace('[', '').replace(']', '').strip("\'")

                url = response.urljoin(link)
                # print ("ready to go to next page")
                yield scrapy.Request(url, dont_filter=True)
                # print (url)
                None
            None


        else:
            # print ("content coming >>>>>")
            # print (response.xpath('//div[@id="content"]').extract())
            item = SpiderItem()

            print (response.url)
            #os.system("pause")



            # 0 - position, 1 - title, 2 - time, 3 - source, 4 - content, 5 - aff, 6 - next_url
            time_pattern = self.DICT.get_pattern(domain_name, 2)
            print ("time pattern>>>", time_pattern)
            #os.system("pause")

            time_obj = response.xpath(time_pattern).extract_first()
            time_str = re.search(r'[0-9-]+', time_obj).group(0)

            title_pattern = self.DICT.get_pattern(domain_name, 1)
            content_pattern = self.DICT.get_pattern(domain_name, 4)
            aff_pattern = self.DICT.get_pattern(domain_name, 5)

            if prep.valid_time(time_str=time_str): # time in range
                item['time'] = time_str
                item['title'] = response.xpath(title_pattern).xpath('string(.)').extract_first()
                item['position'] = self.DICT.get_pattern(domain_name, 0)
                item['source'] = self.DICT.get_pattern(domain_name, 3)
                item['url'] = response.url
                item['aff'] = response.xpath(aff_pattern).extract_first()
                item['content'] = response.xpath(content_pattern).xpath('string(.)').extract_first()
                #os.system("pause")
                yield item

            '''
            item['title'] = response.xpath('//div[@class="v_title"]/h1').extract_first()
            time_pattern = r"<span>时间.*?</span>"
            aff_pattern = r"附件："

            #time_pattern = time_pattern.decode('utf-8')
            aff_obj = re.findall(aff_pattern, response.body.decode('utf-8'))
            time_obj = re.search(time_pattern, response.body.decode('utf-8'))

            item['position'] = None
            item['source'] = None
            item['url'] = response.url
            # item['content'] = response.xpath('//div[@id="content"]').extract_first()
            item['content'] = None
            item['aff'] = len(aff_obj)


            if time_obj:
                time_str = time_obj.group(0)[9:19]
                item['time'] = time_str
                year = time_str[0:4]
                month = time_str[5:7]
                day = time_str[8:10]
                print (year, month, day)
                if hasattr(self, 'OP'):
                    if prep.valid_time(self.OP, self.ED, year, month, day):
                        yield item
                else:
                    yield item

            else:
                print ("no time object")
                yield item
            # 检测时间在这里
            '''


            None

