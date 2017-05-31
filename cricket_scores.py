from bs4 import BeautifulSoup
import urllib2
import prettytable

# Gets the cricket scores for a particular date
def scrapeData(date):

    url = "http://www.espncricinfo.com/ci/engine/match/index.html"

    if date != "":
        url+="?date="+date

    file = urllib2.urlopen(url)
    scrapedData = file.read()
    file.close()

    soup = BeautifulSoup(scrapedData,'html.parser')
    tournaments = soup.find_all('div',attrs={'class':'match-section-head'})
    matchesUnderTournament = soup.find_all('section',attrs={'class': 'matches-day-block'})

    index = 0

    cricketScores = prettytable.PrettyTable(['Tournament','Match Info','Team 1','Team2','Match Status'])

    for tournament in tournaments:

        tournamentName = tournament.h2.text
        # print "\n",tournamentName

        matches = matchesUnderTournament[index].find_all('section', attrs={'class': 'default-match-block'})

        for match in matches:
            matchInfo = match.find_all('div')

            match_info = matchInfo[0].span.text
            team1 = matchInfo[1].text
            team2 = matchInfo[2].text
            match_status = matchInfo[3].text

            # print "Match Info :",match_info
            # print "Team 1 :",team1
            # print "Team 2 :",team2
            # print "Match Status :",match_status

            info = [tournamentName, match_info, team1, team2, match_status]
            cricketScores.add_row(info)

        index+=1

    print cricketScores

    return cricketScores

# Gets the date from the user for which the cricket scores have to be displayed
date = raw_input("Enter date in format (yyyy-mm-dd) or Now :")

# Displays the score on the current date if 'Now' is entered by the user otherwise scores of a particular date
if date=='Now':
    scrapeData(date="")
else:
    scrapeData(date)

