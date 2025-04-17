import feedparser

def get_current_financial_news():

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

    # Limit to top 15
    top_news = news_entries[:25]

    # Print nicely
    print("Top 15 Financial News Headlines:\n")
    for i, entry in enumerate(top_news, start=1):
        print(f"{i}. {entry['title']}")
        print(f"   Source: {entry['source']}")
        print(f"   Published: {entry['published']}")
        print(f"   Summary: {entry['summary']}")
        print(f"   Link: {entry['link']}\n")

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

    # Optional: print or return the full string
    print("Combined News Summary String:\n")
    return(news_summary_string)

# You can also return this string from a function or save to file
