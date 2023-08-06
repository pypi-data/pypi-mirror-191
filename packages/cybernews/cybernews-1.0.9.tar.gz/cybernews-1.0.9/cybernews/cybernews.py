"""
    Main Class for Extracting News
"""
from utils.extractor import Extractor

class CyberNews:

    def __init__(self) -> None:
        self._extractor = Extractor()
        self._news_types = [
            {
                "general": [
                    {
                        "https://cio.economictimes.indiatimes.com/news/internet": {
                            "headlines": ".descBx h3 a",
                            "author": ".metaTx",
                            "fullNews": ".descBx p",
                            "newsImg": "figure.avtar a img",
                            "newsURL": ".descBx a",
                            "date": None,
                        }
                    }
                ]
            },
            {
                "dataBreach": [
                    {
                        "https://thehackernews.com/search/label/data+breach": {
                            "headlines": "h2.home-title",
                            "author": ".item-label span",
                            "fullNews": ".home-desc",
                            "newsImg": ".img-ratio img",
                            "newsURL": "a.story-link",
                            "date": ".item-label",
                        }
                    }
                ]
            },
            {
                "cyberAttack": [
                    {
                        "https://thehackernews.com/search/label/Cyber+Attack": {
                            "headlines": "h2.home-title",
                            "author": ".item-label span",
                            "fullNews": ".home-desc",
                            "newsImg": ".img-ratio img",
                            "newsURL": "a.story-link",
                            "date": ".item-label",
                        }
                    }
                ]
            },
            {
                "vulnerability": [
                    {
                        "https://thehackernews.com/search/label/Vulnerability": {
                            "headlines": "h2.home-title",
                            "author": ".item-label span",
                            "fullNews": ".home-desc",
                            "newsImg": ".img-ratio img",
                            "newsURL": "a.story-link",
                            "date": ".item-label",
                        }
                    }
                ]
            },
            {
                "malware": [
                    {
                        "https://thehackernews.com/search/label/Malware": {
                            "headlines": "h2.home-title",
                            "author": ".item-label span",
                            "fullNews": ".home-desc",
                            "newsImg": ".img-ratio img",
                            "newsURL": "a.story-link",
                            "date": ".item-label",
                        }
                    }
                ]
            },
            {
                "security": [
                    {
                        "https://telecom.economictimes.indiatimes.com/tag/hacking": {
                            "headlines": ".descBx h3 a",
                            "author": ".metaTx",
                            "fullNews": ".descBx p",
                            "newsImg": "figure.avtar a img",
                            "newsURL": ".descBx a",
                            "date": None,
                        }
                    },
                    {
                        "https://cio.economictimes.indiatimes.com/news/digital-security": {
                            "headlines": ".descBx h3 a",
                            "author": ".metaTx",
                            "fullNews": ".descBx p",
                            "newsImg": "figure.avtar a img",
                            "newsURL": ".descBx a",
                            "date": None,
                        }
                    },
                ]
            },
            {
                "cloud": [
                    {
                        "https://cio.economictimes.indiatimes.com/news/cloud-computing": {
                            "headlines": ".descBx h3 a",
                            "author": ".metaTx",
                            "fullNews": ".descBx p",
                            "newsImg": "figure.avtar a img",
                            "newsURL": ".descBx a",
                            "date": None,
                        }
                    }
                ]
            },
            {
                "tech": [
                    {
                        "https://telecom.economictimes.indiatimes.com/tag/digitalindia": {
                            "headlines": ".descBx h3 a",
                            "author": ".metaTx",
                            "fullNews": ".descBx p",
                            "newsImg": "figure.avtar a img",
                            "newsURL": ".descBx a",
                            "date": None,
                        }
                    },
                    {
                        "https://cio.economictimes.indiatimes.com/tag/next+gen+tech": {
                            "headlines": ".descBx h3 a",
                            "author": ".metaTx",
                            "fullNews": ".descBx p",
                            "newsImg": "figure.avtar a img",
                            "newsURL": ".descBx a",
                            "date": None,
                        }
                    },
                ]
            },
            {
                "iot": [
                    {
                        "https://cio.economictimes.indiatimes.com/news/internet-of-things": {
                            "headlines": ".descBx h3 a",
                            "author": ".metaTx",
                            "fullNews": ".descBx p",
                            "newsImg": "figure.avtar a img",
                            "newsURL": ".descBx a",
                            "date": None,
                        }
                    }
                ]
            },
            {
                "bigData": [
                    {
                        "https://cio.economictimes.indiatimes.com/news/big-data": {
                            "headlines": ".descBx h3 a",
                            "author": ".metaTx",
                            "fullNews": ".descBx p",
                            "newsImg": "figure.avtar a img",
                            "newsURL": ".descBx a",
                            "date": None,
                        }
                    },
                    {
                        "https://cio.economictimes.indiatimes.com/news/data-center": {
                            "headlines": ".descBx h3 a",
                            "author": ".metaTx",
                            "fullNews": ".descBx p",
                            "newsImg": "figure.avtar a img",
                            "newsURL": ".descBx a",
                            "date": None,
                        }
                    },
                ]
            },
            {
                "business": [
                    {
                        "https://cio.economictimes.indiatimes.com/news/business-analytics": {
                            "headlines": ".descBx h3 a",
                            "author": ".metaTx",
                            "fullNews": ".descBx p",
                            "newsImg": "figure.avtar a img",
                            "newsURL": ".descBx a",
                            "date": None,
                        }
                    }
                ]
            },
            {
                "mobility": [
                    {
                        "https://cio.economictimes.indiatimes.com/news/mobility": {
                            "headlines": ".descBx h3 a",
                            "author": ".metaTx",
                            "fullNews": ".descBx p",
                            "newsImg": "figure.avtar a img",
                            "newsURL": ".descBx a",
                            "date": None,
                        }
                    }
                ]
            },
            {
                "research": [
                    {
                        "https://cio.economictimes.indiatimes.com/tag/research": {
                            "headlines": ".descBx h3 a",
                            "author": ".metaTx",
                            "fullNews": ".descBx p",
                            "newsImg": "figure.avtar a img",
                            "newsURL": ".descBx a",
                            "date": None,
                        }
                    }
                ]
            },
            {
                "socialMedia": [
                    {
                        "https://cio.economictimes.indiatimes.com/news/social-media": {
                            "headlines": ".descBx h3 a",
                            "author": ".metaTx",
                            "fullNews": ".descBx p",
                            "newsImg": "figure.avtar a img",
                            "newsURL": ".descBx a",
                            "date": None,
                        }
                    }
                ]
            },
            {
                "corporate": [
                    {
                        "https://cio.economictimes.indiatimes.com/news/corporate-news": {
                            "headlines": ".descBx h3 a",
                            "author": ".metaTx",
                            "fullNews": ".descBx p",
                            "newsImg": "figure.avtar a img",
                            "newsURL": ".descBx a",
                            "date": None,
                        }
                    }
                ]
            },
        ]

    def get_news(self, news) -> list:
        for news_type in self._news_types:
            if news in news_type:
                try:
                    return self._extractor.data_extractor(news_type[news])
                except Exception as e:
                    raise Exception(
                        f"An error occurred while processing the news of type: '{news}': {str(e)}")
        raise ValueError(f"News type '{news}' not found")