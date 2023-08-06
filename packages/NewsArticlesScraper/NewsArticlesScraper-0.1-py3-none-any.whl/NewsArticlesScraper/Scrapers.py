import scrapy
import datetime
import ciso8601
import time
import re
import logging


class CNBCSpider(scrapy.Spider):
    """Spider to scrape CNBC articles.

    """
    name = 'CNBC'

    allowed_domains = ["api.queryly.com", "cnbc.com"]
    start_urls = []
    custom_settings = {
        'LOG_LEVEL': 'WARN',
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 '
                      'Safari/537.1',
        'ROBOTSTXT_OBEY': False,
        'DOWNLOAD_DELAY': 0.5,
        # 'JOBDIR': './News/CNBCJobs',
        'REQUEST_FINGERPRINTER_IMPLEMENTATION': '2.7',
    }

    def __init__(self, from_time, until_time, **kwargs):
        self.url_stream = "https://api.queryly.com/cnbc/json.aspx?queryly_key=31a35d40a9a64ab3&query=cnbc&endindex={" \
                          "}&batchsize=100&timezoneoffset=-60&sort=date"
        self.from_time = from_time
        self.until_time = until_time
        self.start_page = None
        self.end_page = None
        super().__init__(**kwargs)

    def start_requests(self):
        yield scrapy.Request(self.url_stream.format(0), callback=self.get_total_pages)

    def get_total_pages(self, response):
        data = response.json()
        metadata = data["metadata"]
        total_pages = metadata["totalpage"]
        self.start_page = total_pages
        self.end_page = 1
        middle = round(total_pages/2)
        yield scrapy.Request(self.url_stream.format((middle-1)*100), callback=self.locate_start_page)

    def locate_start_page(self, response):
        data = response.json()
        current_page = data["metadata"]["pagerequested"]
        if current_page != 1:
            newest_date = time.mktime(ciso8601.parse_datetime(data["results"][0]["datePublished"]).timetuple())
            oldest_date = time.mktime(ciso8601.parse_datetime(data["results"][-1]["datePublished"]).timetuple())
            if newest_date <= self.from_time:  # from = 3000 newest = 3050 oldest = 2950
                middle = round((current_page+self.end_page)/2)
                self.start_page = current_page
                yield scrapy.Request(self.url_stream.format((middle-1)*100) + "&x=1", callback=self.locate_start_page)
            if newest_date > self.from_time:
                if oldest_date < self.from_time:
                    logging.info(f"Found start page: {current_page}")
                    yield scrapy.Request(response.url + "&x=1", callback=self.parse)
                    # + "&x=1" is needed because scrapy won't request same page twice
                else:
                    middle = round((current_page+self.start_page)/2)
                    self.end_page = current_page
                    yield scrapy.Request(self.url_stream.format((middle - 1) * 100) + "&x=1",
                                         callback=self.locate_start_page)

    def parse(self, response, **kwargs):
        data = response.json()
        metadata = data["metadata"]
        current_page = metadata["pagerequested"]
        logging.info(f"Requested page {current_page}")

        if current_page:
            if current_page > 1:
                page = (current_page-2) * 100
                yield scrapy.Request(
                    url=self.url_stream.format(page),
                    callback=self.parse)
        else:
            logging.error(f"Current page not found when requesting {response.url}.")

        for result in data["results"]:
            t = time.mktime(ciso8601.parse_datetime(result["datePublished"]).timetuple())
            if self.from_time < t < self.until_time:
                premium = False
                if "cn:contentClassification" in result:
                    clasf = result["cn:contentClassification"]
                    if "premium" in clasf:
                        premium = True
                if not premium:
                    if result["cn:branding"] == "cnbc":
                        if result["cn:type"] not in ["cnbcvideo", "live_story"]:
                            yield scrapy.Request(result["cn:liveURL"], callback=self.parse_article, meta={"time": t})

    @staticmethod
    def parse_article(response):
        content = "".join(response.css(".ArticleBody-subtitle , .group p").css("::text").getall())
        title = response.css(".ArticleHeader-headline ::text").get()
        if title is None:
            title = response.css(".twoCol .title ::text").get()
        author = response.css(".Author-authorName ::text").get()
        if author is None:
            author = response.css(".source > a ::text").get()
        yield {
            "title": title,
            "author_name": author,
            "body": content,
            "time": response.meta["time"],
            "url": response.url,
            "origin": "c",
        }


class NYTSpider(scrapy.Spider):
    """Spider to scrape NYT articles.

    """
    name = 'NYT'
    allowed_domains = ['api.nytimes.com', 'nytimes.com']
    custom_settings = {
        'LOG_LEVEL': 'WARN',
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 '
                      'Safari/537.1',
        'ROBOTSTXT_OBEY': False,
        'DOWNLOAD_DELAY': 6,
        # 'JOBDIR': './News/NYTJobs',
        'REQUEST_FINGERPRINTER_IMPLEMENTATION': '2.7',
        'DOWNLOAD_TIMEOUT': 300,
    }

    def __init__(self, from_time, until_time, api_key, **kwargs):
        self.api_key = api_key
        self.from_time = from_time
        self.until_time = until_time
        if time.time() - self.until_time <= 86400:
            self.recent = True
        else:
            self.recent = False
        super().__init__(**kwargs)

    def start_requests(self):
        url_api_historic = "https://api.nytimes.com/svc/archive/v1/{}/{}.json?api-key=" + self.api_key
        year_min = int(datetime.datetime.fromtimestamp(self.from_time).strftime('%Y'))
        date_max = datetime.datetime.fromtimestamp(self.until_time)
        year_max = int(date_max.strftime('%Y'))
        month_max = int(date_max.strftime('%m'))

        for year in range(year_min, year_max):
            for month in range(1, 13):
                yield scrapy.Request(url_api_historic.format(year, month),
                                     callback=self.parse, meta={"api_point": "historic"})
        for _month in range(1, month_max + 1):
            yield scrapy.Request(url_api_historic.format(year_max, _month),
                                 callback=self.parse, meta={"api_point": "historic"})
        if self.recent:
            url_api_recent = f"https://api.nytimes.com/svc/news/v3/content/all/world.json?api-key={self.api_key}&limit=500"
            yield scrapy.Request(url_api_recent, callback=self.parse, meta={"api_point": "recent"})

    def parse(self, response, **kwargs):
        data = response.json()
        api_point = response.meta["api_point"]
        if api_point == "historic":
            articles = data["response"]["docs"]
        else:
            articles = data["results"]
        for article in articles:
            if api_point == "historic":
                pub_date = article["pub_date"]
            else:
                pub_date = article["published_date"]
            pub_date = time.mktime(ciso8601.parse_datetime(pub_date).timetuple())
            if pub_date < self.from_time:
                break
            if pub_date > self.until_time:
                break
            if api_point == "historic":
                url = article["web_url"]
            else:
                try:
                    url = article["related_urls"][0]["url"]
                except (TypeError, IndexError):
                    url = article["url"]
            yield scrapy.Request(url=url, callback=self.parse_article, meta={"time": pub_date})

    @staticmethod
    def parse_article(response):
        content = "".join(response.css(".StoryBodyCompanionColumn > div > p ::text").getall())
        author_name = response.css(".last-byline ::text").get()
        if author_name is not None:
            author_name = re.sub("[Bb]y.", "", author_name)
        yield {
            "title": response.css("div h1 ::text").get(),
            "author_name": author_name,
            "body": content,
            "time": response.meta["time"],
            "url": response.url,
            "origin": "n",
        }
