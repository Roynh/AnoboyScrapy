import scrapy
from scrapy.crawler import CrawlerProcess
import os
import webbrowser

class Anoboy(scrapy.Spider):
    # Your spider definition
    name = "anoboy"
    chrome_path = '/usr/bin/google-chrome %s'

    def start_requests(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        anime = input('Cari Anime : ')
        urls = 'https://62.182.83.93/?s={}'.format(anime)
        yield scrapy.Request(url=urls, callback=self.SearchEp)
        #yield scrapy.Request(url=urls, callback=self.DownloadAnime)

    def SearchEp(self, response):
        title = response.xpath("//div[@class='column-content']//a[@rel='bookmark']//@title").getall()
        anime_link =  response.xpath("//div[@class='column-content']//a[@rel='bookmark']//@href").getall() 
        page_link = response.xpath("//div[@class='wp-pagenavi']//a[@class='page larger']//@href").get() 
        page_now = response.xpath("//div[@class='wp-pagenavi']//span[@class='pages']//text()").get() 
        
        os.system('cls' if os.name == 'nt' else 'clear')
        print('Perhatian : Jangan Memilih yang bertuliskan [Streaming] atau [Download]')
        for (jdl, i) in zip(title, range(len(title))) :
            print(f"[{i}].Anime : {jdl}")
        print(page_now)
        print("Ketik 'next' untuk berpindah halaman")
        sel = (input('Pilih yang mana : '))
        if 'next' in sel.lower() :
            if page_link is not None :
                page_link = response.urljoin(page_link)
                yield scrapy.Request(url=page_link, callback=self.SearchEp)
        else :
            anime_ep = anime_link[int(sel)]
            title = title[int(sel)]
            if anime_ep is not None and 'Episode' in title:
                anime_ep = response.urljoin(anime_ep)
                yield scrapy.Request(url=anime_ep, callback=self.WatchAnime)
            elif anime_ep is not None : 
                anime_ep = response.urljoin(anime_ep)
                yield scrapy.Request(url=anime_ep, callback=self.SelEpisode)

    def WatchAnime(self, response) :
        servers = response.xpath("//div[@class='vmiror']//a//@data-video").getall()

        servers.pop(0)
        first =  servers[0]
        servers.pop(0)
        new_server = []
        for server in servers :
            link = 'https://62.182.83.93' + server
            new_server.append(link)
            link = ''
        new_server.insert(0,first)

        os.system('cls' if os.name == 'nt' else 'clear')
        print('Server B-Tube : ')
        print('0] 720p')
        print('Server AC : ')
        print('1] 240p')
        print('2] 360p')
        print('3] 340p')
        print('4] 720p')
        print('Server FastStream : ')
        print('5] 240-720p')
        print('server YUP')
        print('6] 240-720p')
        
        sel = input('Pilih Server : ')
        sel_server = new_server[int(sel)]
        webbrowser.get(Nanime.chrome_path).open(sel_server)
    
    def SelEpisode(self, response) :
        ep_anime = response.xpath("//div[@class='singlelink']//li//text()").getall()
        ep_link = response.xpath("//div[@class='singlelink']//li//@href").getall()

        os.system('cls' if os.name == 'nt' else 'clear')
        for (jdl, i) in zip(ep_anime, range(len(ep_anime))) :
            print(f"[{i}].Anime : {jdl}")
        sel = (input('Pilih yang mana : '))

        sel_ep = ep_link[int(sel)]
        if sel_ep is not None :
            sel_ep = response.urljoin(sel_ep)
            yield scrapy.Request(url=sel_ep, callback=self.WatchAnime)

process = CrawlerProcess({
    'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
})

process.crawl(Anoboy)
process.start() # the script will block here until the crawling is finished
