from bs4 import BeautifulSoup
import urllib2
import prettytable
import json

headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'}

# Prints the result in tabular form
def printTable(allBooks):

    books = prettytable.PrettyTable(['SNo','Title','Author','Amazon Price', 'Book Depository Price', 'Reviews','Ratings','Stars','Summary','Amazon Link','Book Depository Link'])

    index = 0
    for book in allBooks:

        if 'AmazonPrice' in book:
            amazonPrice = book['AmazonPrice']
        else:
            amazonPrice = ''

        if 'BookDepositoryPrice' in book:
            bookDepositoryPrice = book['BookDepositoryPrice']
        else:
            bookDepositoryPrice = ''

        if 'Link' in book:
            amazonLink = book['Link']
        else:
            amazonLink = ''

        if 'BookDepositoryLink' in book:
            bookDepositoryLink = book['BookDepositoryLink']
        else:
            bookDepositoryLink = ''

        if 'Reviews' in book:
            reviews = book['Reviews']
        else:
            reviews = ''

        if 'Ratings' in book:
            ratings = book['Ratings']
        else:
            ratings = ''

        if 'Stars' in book:
            stars = book['Stars']
        else:
            stars = ''

        if 'Summary' in book:
            summary = book['Summary']
        else:
            summary = ''

        b = [index+1, book['Title'], book['Author'], amazonPrice, bookDepositoryPrice, reviews, ratings, stars, summary, amazonLink, bookDepositoryLink]
        index += 1

        books.add_row(b)

    # print books


# Gets the required book details along with prices from Amazon
def getFromAmazon(amazonUrl):
    request = urllib2.Request(amazonUrl, headers=headers)

    amazonFile = urllib2.urlopen(request)
    scrapedFromAmazon = amazonFile.read()
    amazonFile.close()

    soup = BeautifulSoup(scrapedFromAmazon, 'html.parser')

    allBooks = soup.find_all('li', attrs={'class': 's-result-item celwidget '})
    # print allBooks
    i = 0
    amazonBooks = []

    for book in allBooks:
        bookDetails = {}

        img = book.img['src']

        details = book.find('div', {'class': 'a-fixed-left-grid-col a-col-right'})

        link = details.find('a', {'class':'a-link-normal s-access-detail-page s-color-twister-title-link a-text-normal'})

        if hasattr(link,'href'):
            link = link['href']
        else:
            continue

        if details.h2.text:
            bookTitle = details.h2.text
        else:
            continue

        authors_names = details.find_all('span', {'class': 'a-size-small a-color-secondary'})

        authors = ""
        # print authors_names
        for i in range(2, len(authors_names)):

            if authors_names[i].text:
                # print "Author :",authors_names[i].text
                authors += authors_names[i].text
            else:
                break

        temp = details.find('span', {'class': 'a-size-base a-color-price s-price a-text-bold'})
        if temp:
            price = temp.text
        else:
            price = "Not available"

        bookDetails = {"Link": link, "img": img, "Title": bookTitle, "Author": authors, "AmazonPrice": price}

        # print bookDetails

        # print bookTitle,authors
        bookTitle= urllib2.quote(bookTitle.encode('utf-8')+authors.encode('utf-8'))

        bookdepositoryUrl = "https://www.bookdepository.com/search?searchTerm=" + bookTitle
        # print bookdepositoryUrl
        bookdepository = getFromBookDepository(bookdepositoryUrl)

        if bookdepository != 'None':
            bookDetails['BookDepositoryLink'] = bookdepository[0]
            bookDetails['BookDepositoryPrice'] = bookdepository[1]
            # print bookDetails

        goodreadsUrl = "https://www.goodreads.com/search?q=" + bookTitle
        # print goodreadsUrl
        goodreadsBooks = getFromGoodReads(goodreadsUrl)

        if goodreadsBooks != 'None':
            bookDetails['GoodReadsLink'] = goodreadsBooks[0]
            bookDetails['Stars'] = goodreadsBooks[1]
            bookDetails['Ratings'] = goodreadsBooks[2]
            bookDetails['Reviews'] = goodreadsBooks[3]
            bookDetails['Summary'] = goodreadsBooks[4]
            # print bookDetails

        amazonBooks.append(bookDetails)

        print bookDetails

    # print amazonBooks

    return amazonBooks


# Gets the required book details along with prices from Boom Depository
def getFromBookDepository(bookdepositoryUrl):

    # print bookdepositoryUrl

    bookdepositoryFile = urllib2.urlopen(bookdepositoryUrl)
    scrapedFromBookDepository = bookdepositoryFile.read()
    bookdepositoryFile.close()

    soup = BeautifulSoup(scrapedFromBookDepository, 'html.parser')

    books = soup.find_all('ol',attrs={'class' : 'breadcrumb'})

    if len(books)>0:
        link = bookdepositoryUrl
        price = soup.find('span',attrs={'class':'sale-price'})
        if price:
            price = price.text
        else:
            price = soup.find('p', attrs={'class': 'list-price'})
            if price:
                price = price.text
            else:
                price = "Not available"

        return [link, price]

    else:

        books = soup.find_all('div',attrs={'class' : 'book-item'})

        # bookdepositoryBooks = []

        # for book in books:

            # bookDetails = {}

            # link = "https://www.bookdepository.com"+book.a['href']
            # img = book.img['data-lazy']
            #
            # temp = book.find('h3',{'class':'title'})
            # bookTitle = temp.text.strip(' \t\n\r')
            #
            # temp = book.find('p',{'class':'author'})
            # author = temp.text.strip(' \t\n\r')
            #
            # temp = book.find('p',{'class':'published'})
            # date = temp.text.strip(' \t\n\r')

            # temp = book.find('p', {'class': 'price'})
            # price = temp.text.strip(' \t\n\r')
            #
            # temp = book.find('span', {'class': 'rrp'})
            # if temp:
            #     originalprice = temp.text.strip(' \t\n\r')
            #     price = price.replace(originalprice,"")

            # print link,img,bookTitle,author,date,price

            # bookDetails = {"Link": link, "img": img, "Title": bookTitle, "Author": author, "Price": price, "Date": date}

            # bookdepositoryBooks.append(bookDetails)

        # print bookdepositoryBooks

        # return bookdepositoryBooks

        if len(books)>0:
            link = "https://www.bookdepository.com"+books[0].a['href']

            temp = books[0].find('p', {'class': 'price'})
            if temp:
                price = temp.text.strip(' \t\n\r')
            else:
                price = ""

            temp = books[0].find('span', {'class': 'rrp'})
            if temp:
                # print temp
                originalprice = temp.text.strip(' \t\n\r')
                price = price.replace(originalprice, "")

            return [link,price]

        else:
            return "None"


# Gets the required book reviews and ratings from Good Reads
def getFromGoodReads(goodreadsUrl):

    goodreadsFile = urllib2.urlopen(goodreadsUrl)
    scrapedFromGoodReads = goodreadsFile.read()
    goodreadsFile.close()

    soup = BeautifulSoup(scrapedFromGoodReads, 'html.parser')
    trs = soup.find_all('tr')

    # goodreadsBooks = []
    #
    # for tr in trs:
    #
    #     bookDetails = {}
    #
    #     link = "http://www.goodreads.com"+tr.a['href']
    #
    #     temp = tr.find('a',attrs={'class':'bookTitle'})
    #     bookTitle = temp.text.strip(' \t\n\r')
    #
    #     temp = tr.find('a', attrs={'class': 'authorName'})
    #     author = temp.text
    #
    #     bookFile = urllib2.urlopen(link)
    #     scrapedFromBookFile = bookFile.read()
    #     bookFile.close()
    #
    #     soupForBook = BeautifulSoup(scrapedFromBookFile, 'html.parser')
    #     temp = soupForBook.find('div',attrs={'id':'description'})
    #     temp = temp.find_all('span')
    #     if len(temp)>=2:
    #         summary = temp[1].text
    #     else:
    #         summary = temp[0].text
    #
    #     temp = soupForBook.find('span', attrs={'class': 'value rating'})
    #     stars = temp.text
    #
    #     temp = soupForBook.find_all('a', attrs={'href': '#other_reviews'})
    #     ratings = temp[0].text.replace('Ratings','').strip(' \t\n\r')
    #
    #     reviews = temp[1].text.replace('Reviews\n','').strip(' \t\n\r')
    #     # print link," ",bookTitle," ",author," ",stars," ",ratings," ",reviews," ",summary
    #
    #     bookDetails = {"Link":link, "Title":bookTitle, "Author":author, "Stars":stars, "Ratings":ratings, "Reviews":reviews, "Summary":summary}
    #
    #     # print bookDetails
    #
    #     goodreadsBooks.append(bookDetails)
    #
    # print goodreadsBooks
    #
    # return goodreadsBooks

    if len(trs) > 0:

        link = "http://www.goodreads.com" + trs[0].a['href']

        bookFile = urllib2.urlopen(link)
        scrapedFromBookFile = bookFile.read()
        bookFile.close()

        soupForBook = BeautifulSoup(scrapedFromBookFile, 'html.parser')
        temp = soupForBook.find('div', attrs={'id': 'description'})

        if temp:
            temp = temp.find_all('span')
            if len(temp) >= 2:
                summary = temp[1].text
            else:
                summary = temp[0].text
        else:
            summary = ""

        temp = soupForBook.find('span', attrs={'class': 'value rating'})
        if temp:
            stars = temp.text
        else:
            stars = ""

        temp = soupForBook.find_all('a', attrs={'href': '#other_reviews'})
        if len(temp)>1:
            ratings = temp[0].text.replace('Ratings', '').strip(' \t\n\r')
            reviews = temp[1].text.replace('Reviews\n', '').strip(' \t\n\r')
        else:
            ratings = ""
            reviews = ""

        return [link,stars,ratings,reviews,summary]

    else:
        return "None"


# Matches the title and author of each book from Amazon and Book Depository and combines them to get prices from both the sites for each book
def getPrices(book):

    amazonUrl = "http://www.amazon.in/s/?url=search-alias%3Dstripbooks&field-keywords="+urllib2.quote(book)
    print amazonUrl
    amazonBooks = getFromAmazon(amazonUrl)

    return amazonBooks
    # bookdepositoryUrl = "https://www.bookdepository.com/search?searchTerm="+book
    #
    # bookdepositoryBooks = getFromBookDepository(bookdepositoryUrl,headers)

    # goodreadsUrl = "https://www.goodreads.com/search?q="+book
    #
    # goodreadsBooks = getFromGoodReads(goodreadsUrl,headers)

    # print amazonBooks

    # printTable(amazonBooks)

    amazonBooks = json.dumps(amazonBooks)

    # print amazonBooks

    # print bookdepositoryBooks
    #
    # print goodreadsBooks
    #
    # allBooks = []
    # for book1 in amazonBooks:
    #     for book2 in bookdepositoryBooks:
    #         for book3 in goodreadsBooks:
    #
    #             bookDetails = {flag: 0}
    #
    #             if book1['Title'] == book2['Title'] and book1['Title'] == book3['Title'] and book1['Author'] == book2['Author'] and book1['Author'] == book3['Author']:
    #                 bookDetails = {"Amazon Link": book1['Link'], "Book Depository Link:": book2['Link'], "Title": book1['Title'], "Author": book1['Author'], "Stars": book3['Stars'],
    #                                "Ratings": book3['Ratings'], "Reviews": book3['Reviews'], "Summary": book3['Summary'], "Amazon": book1['Price'], "Book Depository": book2['Price']}
    #                 # print bookDetails
    #
    #             elif book1['Title'] == book3['Title'] and book1['Author'] == book3['Author']:
    #                     bookDetails = {"Amazon Link": book1['Link'], "Title": book1['Title'], "Author": book1['Author'],
    #                                    "Stars": book3['Stars'],
    #                                    "Ratings": book3['Ratings'], "Reviews": book3['Reviews'],
    #                                    "Summary": book3['Summary'], "Amazon": book1['Price']}
    #
    #             elif book2['Title'] == book3['Title'] and book2['Author'] == book3['Author']:
    #                     bookDetails = {"Book Depository Link": book2['Link'], "Title": book2['Title'], "Author": book2['Author'],
    #                                    "Stars": book3['Stars'],
    #                                    "Ratings": book3['Ratings'], "Reviews": book3['Reviews'],
    #                                    "Summary": book3['Summary'], "Book Depository": book2['Price']}
    #
    #             if bookDetails != {}:
    #                 allBooks.append(bookDetails)
    #                 break
    #                 # print bookDetails
    #
    # print allBooks
    #
    # printTable(allBooks)
    #
    # return allBooks


# Gets the required keyword from the user on the basis of which the book has to be searched
keyword = raw_input("Enter book to be searched :")
print keyword
# Invokes getPrices to display prices of books matching the keyword

books = getPrices(keyword)
print books