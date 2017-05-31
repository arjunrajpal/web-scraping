from bs4 import BeautifulSoup
import urllib2
import prettytable

# Gets the news headlines and article link on the basis of the keyword(topic)
def getNews(topic):

    url = "https://news.google.co.in/news/section?q="+topic

    newsFile = urllib2.urlopen(url)
    news = newsFile.read()
    newsFile.close()

    soup = BeautifulSoup(news,'html.parser')

    # headlines = soup.find_all('span',attrs={'class':'titletext'})
    articleLink = soup.find_all('h2',attrs={'class':'esc-lead-article-title'})

    # print len(headlines)
    # print len(articleLink)

    newsArticles = prettytable.PrettyTable(['SNo','Headlines','News Link'])

    for index in range(len(articleLink)):

        newsHeadlines = articleLink[index].find('span',attrs={'class':'titletext'}).text
        newsLink = articleLink[index].a['href']

        # print "Article", index+1, ": ", headlines[index].text

        # print "Article", index+1, ": ", newsHeadlines
        # print newsLink

        article = [index+1, newsHeadlines, newsLink]
        newsArticles.add_row(article)

    print newsArticles

    return newsArticles

# Gets the topic from the user about which news has to be retrieved
topic = raw_input('Enter topic for news :')

# Invokes getNews to get the news articles
newsArticles = getNews(topic)
