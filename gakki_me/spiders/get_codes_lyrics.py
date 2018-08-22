# -*- coding: utf-8 -*-
import scrapy
from gakki_me.items import SongPages
from gakki_me.items import CodesLyrics


class GetCodesLyricsSpider(scrapy.Spider):
    name = 'get_codes_lyrics'
    allowed_domains = ['gakufu.gakki.me']
    #start_urls = ['http://http://gakufu.gakki.me/']
    handle_httpstatus_list = [404] 


    def __init__(self, init_url=None, *args, **kwargs):
        super(GetCodesLyricsSpider, self).__init__(*args, **kwargs)
        
        if init_url != None:
            self.start_urls  = [init_url]
            self.artist_name = init_url.split(':')[-1]
            self.all_pages  = []
            self.songs      = SongPages() # store urls of single song pages
            self.songs["song_urls"] = []
            self.page_num   = 0
            self.header = 'http://gakufu.gakki.me/search/'
            self.song_page_head = 'http://gakufu.gakki.me/'
            # get all urls of songs in this page

            self.song_page_list = []
            self.song_page_num = 0

            self.codes_lyrics = CodesLyrics()
            self.codes_lyrics['titles'] = []
            self.codes_lyrics['codes']  = []
            self.codes_lyrics['lyrics'] = []

            self.lyrics_dump = []
            self.codes_dump  = []

        else:
            print("Error: initial url need to be speficied.")
            

    def parse(self, response):

        # initial url will be specify the artist page. 
        print("initial page")
        # get all pages from pagenation info.
        # * this page is the first page. Urls listed starts from second page.
        all_pages_pre = response.xpath('//*[@class="s_pagination"]//@href').extract()
        num_other_pages = len(all_pages_pre)
        newheader = "index.asp?mode=list&lid=&sort=&word=AT:" + self.artist_name
        self.all_pages = [newheader + "&page={}".format(x+2) for x in range(num_other_pages)]

        # get all urls of songs in this page
        all_songs_in_this_page = response.xpath('//*[@id="ranking_list"]//div[@class="detail"]//p[@class="name"]//@href').extract()
        self.songs["song_urls"].extend(all_songs_in_this_page)
        
        next_url = self.header + self.all_pages[self.page_num]
        
        #print(self.songs["song_urls"])

        # go to next page
        req_next = scrapy.Request(next_url, callback=self.next_parse)
        yield req_next

    def next_parse(self, response):
        # get all urls of songs in this page
        print("{}-th page".format(self.page_num))
        all_songs_in_this_page = response.xpath('//*[@id="ranking_list"]//p[@class="name"]//@href').extract()
        self.songs["song_urls"].extend(all_songs_in_this_page)
        #print(self.songs["song_urls"])

        self.page_num += 1
        try:
            next_url = self.header + self.all_pages[self.page_num]
            # go to next page
            req_next = scrapy.Request(next_url, callback=self.next_parse, dont_filter = True)
            yield req_next
        except:
            # final pagenation
            #yield self.songs

            # make a list of each song page
            self.song_page_list = [self.song_page_head + x for x in self.songs["song_urls"]]
            next_url = self.song_page_list[self.song_page_num]
            self.song_page_num += 1
            req_next = scrapy.Request(next_url, callback=self.song_page_parse, dont_filter = True)
            yield req_next

    def song_page_parse(self, response):
        if response.status == 404:
            next_url = self.song_page_list[self.song_page_num]
            self.song_page_num += 1
            req_next = scrapy.Request(next_url, callback=self.song_page_parse, dont_filter = True)

            yield req_next

        
        
        from lxml import etree
            
        # get song title
        song_title = response.xpath('//*[@class="tit"]/text()').extract()[0]
        self.codes_lyrics['titles'].append(song_title)
 
        # get all codes and lyrics info
        c_and_l = response.xpath('//*[@class="score_02"]//div[@id="code_area"]//p').extract()

        lyrs = [] # lyrics, if no lyrics -> "nnann" will be put in
        cods = [] # codes

        # functions for extraction of necessary info
        find_code = etree.XPath('//u/text()')
        find_lyrs = etree.XPath('//p/text()')

        num_codes_one_line_before = 0
        if_before_code = False
        for one_line in c_and_l:
            # try codes or lyrics from this line

            # make lxml obj 
            xline = etree.fromstring(one_line)

            # get code info
            code = find_code(xline)
            # if this line is not for code but lyrics
            if len(code) == 0:
                # get lyric info
                try:
                    lyric = find_lyrs(xline)[0]#.split('\xa0').split('\u3000')
                    if_before_code = False
                except:
                    #print(etree.tostring(xline))
                    pass
            elif if_before_code == False: # if code line comes more than twice,
                if_before_code = True
            elif if_before_code == True:
                # insert nan in the lyrics
                lyric = ['nan' for x in range(num_codes_one_line_before)]

            num_codes_one_line_before = len(code)

            # append to items
           
            if len(code) != 0:
                # append code
                cods.append(code)
                #self.codes_lyrics['codes'].extend(code)
            try:
                if len(lyric) != 0: # and len(code) == 0:
                    # append lyric by splitting with \xa0
                    lyrs.append(lyric)
                    lyric = []
                    #self.codes_lyrics['lyrics'].extend(lyric)
            except:
                pass

        self.codes_dump.append(cods)
        self.lyrics_dump.append(lyrs)
        
        # go to the next song page if exists
        if self.song_page_num == len(self.song_page_list):
            self.codes_lyrics['codes'].append(self.codes_dump)
            self.codes_lyrics['lyrics'].append(self.lyrics_dump)
            
            yield self.codes_lyrics

        else:
            next_url = self.song_page_list[self.song_page_num]
            self.song_page_num += 1
            req_next = scrapy.Request(next_url, callback=self.song_page_parse, dont_filter = True)

            yield req_next







        

