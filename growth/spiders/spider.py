import scrapy

class ProdutoSpider(scrapy.Spider):
    name = 'spider'
    allowed_domains = ['www.gsuplementos.com.br']
    start_urls = [
        'https://www.gsuplementos.com.br/aminoacidos', 
        'https://www.gsuplementos.com.br/proteina',
        'https://www.gsuplementos.com.br/vegetariano',
        'https://www.gsuplementos.com.br/vegano',
        'https://www.gsuplementos.com.br/carboidratos',
        'https://www.gsuplementos.com.br/fitoterapicos',
        'https://www.gsuplementos.com.br/vitaminas',
        'https://www.gsuplementos.com.br/roupas-de-treino',
        'https://www.gsuplementos.com.br/termogenico',
        'https://www.gsuplementos.com.br/acessorios']

#    def start_requests(self):
#
#        for url in self.start_urls:
#            yield scrapy.Request(url=url, headers=self.headers, callback = self.parse)

    def parse(self, response):
        #print(response.url)

        produtos = response.xpath('//div[@class="flex-container flex-dir-column vitrine-prod flex-child-auto"]')
        
        for produto in produtos:
            produto_url = produto.xpath('.//div/div/a/@href').extract_first()
            # print(produto_url)
            yield scrapy.Request(produto_url, callback = self.parse_produto)
        
        proxima_pagina_url = response.xpath('//button[@class="proxima "]/@onclick').extract_first()

        if proxima_pagina_url is not None:
            proxima_pagina_url = proxima_pagina_url.split('=', 2)
            proxima_pagina_url = proxima_pagina_url[1]
            yield scrapy.Request(proxima_pagina_url, callback=self.parse)
            
        

    def parse_produto(self, response):
        nome = response.xpath('//div/h1/text()').extract_first()
        preco = response.xpath('//gs-custom/text()').extract_first()
        imagem  = response.xpath('//section[3]/div/div[2]/img/@src').extract_first()
                  

        yield {
            'nome': nome,
            'preco': preco,
            'imagem': imagem
        }



    



    