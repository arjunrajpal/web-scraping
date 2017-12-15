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
    articleLink = soup.find_all('c-wiz',attrs={'class':'M1Uqc kWyHVd'})

    # print len(headlines)
    print len(articleLink)

    newsArticles = prettytable.PrettyTable(['SNo','Headlines','News Link'])

    for index in range(len(articleLink)):

        newsHeadlines = articleLink[index].find('a',attrs={'class':'nuEeue hzdq5d ME7ew'}).text
        newsLink = articleLink[index].find('a',attrs={'class':'nuEeue hzdq5d ME7ew'})['href']

        print "Article", index+1, ": ", newsHeadlines

        print "Article", index+1, ": ", newsLink

        article = [index+1, newsHeadlines, newsLink]
        newsArticles.add_row(article)

    print newsArticles

    return newsArticles

# Gets the topic from the user about which news has to be retrieved
topic = raw_input('Enter topic for news :')

# Invokes getNews to get the news articles
newsArticles = getNews(topic)
