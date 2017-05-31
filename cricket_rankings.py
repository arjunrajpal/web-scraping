from bs4 import BeautifulSoup
import urllib2
import prettytable

# Gets the cricket team rankings for men on the basis of the format
def getRankings(format):

    url = "https://www.icc-cricket.com/rankings/mens/team-rankings/"+format

    file = urllib2.urlopen(url)
    rankings = file.read()
    file.close()

    soup = BeautifulSoup(rankings,'html.parser')

    positions = soup.findAll('td',attrs={'class':'table-body__cell table-body__cell--position'})
    teams = soup.findAll('td',attrs={'class':'table-body__cell rankings-table__team u-text-left'})
    matchesAndPoints = soup.findAll('td',attrs={'class':'table-body__cell'})
    ratings = soup.findAll('td',attrs={'class':'table-body__cell u-text-right rating'})

    indexForMatches = 2
    incrementForMatches = 5

    indexForPoints = 3
    incrementForPoints = 5

    teamDetails = prettytable.PrettyTable(['Position','Team','Matches','Points','Ratings'])

    for index in range(len(positions)):

        position = positions[index].text.strip(' \t\n\r')
        team = teams[index].text.strip(' \t\n\r')
        matches = matchesAndPoints[indexForMatches].text.strip(' \t\n\r')
        points = matchesAndPoints[indexForPoints].text.strip(' \t\n\r')
        rating = ratings[index].text.strip(' \t\n\r')

        # print position,team,' ',matches,' ',points,' ',rating

        team = [position, team, matches, points, rating]
        teamDetails.add_row(team)

        indexForMatches += incrementForMatches
        indexForPoints += incrementForPoints

    print teamDetails

    return teamDetails

# Gets the format from the user for which rankings have to be displayed
format = raw_input('Enter format :')

# Invokes getRankings to get the cricket ranking details
teamDetails = getRankings(format)
