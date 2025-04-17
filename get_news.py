import feedparser
import time

# Simple in-memory cache
_cache = {
    'timestamp': 0,
    'data': None
}

# Cache timeout in seconds (e.g., 10 minutes = 600 seconds)
CACHE_TIMEOUT = 86400  

def get_current_financial_news():
    current_time = time.time()
    
    # Check if cache is still valid
    if _cache['data'] is not None and (current_time - _cache['timestamp'] < CACHE_TIMEOUT):
        print("Using cached financial news...\n")
        return _cache['data']

    print("Fetching fresh financial news...\n")

    # Define RSS feed URLs for financial news
    rss_feeds = {
        'CNBC': 'https://www.cnbc.com/id/100003114/device/rss/rss.html',
        'Reuters Business': 'http://feeds.reuters.com/reuters/businessNews',
        'Moneycontrol': 'https://www.moneycontrol.com/rss/MCtopnews.xml',
        'Economic Times': 'https://economictimes.indiatimes.com/rssfeedsdefault.cms',
        'Bloomberg': 'https://www.bloomberg.com/feed/podcast/etf-report.xml'
    }

    # Collect and store news items
    news_entries = []

    for source, url in rss_feeds.items():
        feed = feedparser.parse(url)
        for entry in feed.entries:
            news_entries.append({
                'title': entry.title,
                'link': entry.link,
                'summary': entry.summary if 'summary' in entry else 'No summary available.',
                'published': entry.published if 'published' in entry else 'No date available.',
                'source': source
            })

    # Sort by latest date if possible
    news_entries.sort(key=lambda x: x['published'], reverse=True)

    # Limit to top 25
    top_news = news_entries[:25]

    # Prepare single string of all news items
    news_summary_string = ""
    for i, entry in enumerate(top_news, start=1):
        news_summary_string += (
            f"{i}. {entry['title']}\n"
            f"Source: {entry['source']}\n"
            f"Published: {entry['published']}\n"
            f"Summary: {entry['summary']}\n"
            f"Link: {entry['link']}\n\n"
        )

    # Update the cache
    _cache['timestamp'] = current_time
    _cache['data'] = news_summary_string

    return news_summary_string
