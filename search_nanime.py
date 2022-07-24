import scrapy
from scrapy.crawler import CrawlerProcess
import os
import webbrowser

class Nanime(scrapy.Spider):
    # Your spider definition
    name = "nanime"
    chrome_path = '/usr/bin/google-chrome %s'

    def start_requests(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        nama_anime = input('Cari Anime : ')
        urls = 'https://nanimex.org/?s={}'.format(nama_anime)
        yield scrapy.Request(url=urls, callback=self.CariAnime)
        #yield scrapy.Request(url=urls, callback=self.DownloadAnime)

    def CariAnime(self, response):
        judul = response.xpath("//div[@class='col-sm-3 content-item']//h3/text()").getall()
        link_anime = response.xpath("//div[@class='col-sm-3 content-item']//a[@title]//@href").getall()
        tahun_release = response.xpath("//div[@class='col-sm-3 content-item']//div[@class='status']//a/text()").getall()

        os.system('cls' if os.name == 'nt' else 'clear')
        for (jdl, tahun, i) in zip(judul, tahun_release, range(len(judul))) :
            print(f"[{i}].Anime : {jdl}")
            print(f"Tahun Release : {tahun}")
        
        pilih = int(input('Pilih yang mana : '))
        judul_anime = link_anime[pilih]

        if judul_anime is not None :
            judul_anime = response.urljoin(judul_anime)
            yield scrapy.Request(url=judul_anime, callback=self.LinkAnime)

    def LinkAnime(self, response) :
        nama_episode = response.xpath("//div[@class='box-body episode_list']//a/text()").getall()
        link_episode = response.xpath("//div[@class='box-body episode_list']//a/@href").getall()

        os.system('cls' if os.name == 'nt' else 'clear')
        for (nama,i) in zip((nama_episode),range(1,len(nama_episode)+1)) :
            print(f'[{i}]-{nama}')

        pilih_ep = int(input('Pilih Episode : ')) - 1
        episode = link_episode[pilih_ep]
        enter = input('Tekan Enter / b untuk buka link :')
        if enter == 'b' :
            webbrowser.get(Nanime.chrome_path).open(episode)

        if episode is not None :
            episode = response.urljoin(episode)
            yield scrapy.Request(url=episode, callback=self.DownloadAnime)

    def DownloadAnime(self, response) :
        link_downloads = response.xpath("//div[@class='box-title pull-left form-inline']//option/@value").getall()
        server = response.xpath("//div[@class='box-title pull-left form-inline']//option/text()").getall()

        if len(link_downloads) == 0 :
            print('link kosong')
            input('tekan enter')

        os.system('cls' if os.name == 'nt' else 'clear')
        for (k,i) in zip(server, range(len(server))) :
            print(f"[{i}]-{k}")

        pilih_k = int(input('Pilih Kualitas : '))
        kualitas_pilihan = link_downloads[pilih_k]
        os.system('cls' if os.name == 'nt' else 'clear')
        #download = requests.get(kualitas_pilihan).content
        #pilih_download = input('Download Y/n : ')
        #if pilih_download.lower() == 'y':
        #    with open(f'/anime_cli_indo/Downloads/{kualitas_pilihan[-7]}','wb') as handler :
        #        print('Sedang Mendownload')
        #        handler.write(download)
        #        print('Selesai Mendownload')
        #else :
        #    print('Tidak Mendownload')
        print(kualitas_pilihan)
        webbrowser.get(Nanime.chrome_path).open(kualitas_pilihan)
        pilih = input('Tekan Enter Untuk Keluar')

process = CrawlerProcess({
    'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
})

process.crawl(Nanime)
process.start() # the script will block here until the crawling is finished