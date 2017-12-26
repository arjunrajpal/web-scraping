import mechanize
from bs4 import BeautifulSoup
from prettytable import PrettyTable
import csv
import resume_manager
import urllib2


def login(rollno, password):

    absoluteUrl = "http://tnp.dtu.ac.in/rm_2016-17/login/"

    br = mechanize.Browser()
    br.set_handle_robots(False)
    br.addheaders = [('User-agent', 'Firefox')]
    br.open(absoluteUrl)
    br.select_form(nr=0)
    br.form['student_username_rollnumber'] = rollno
    br.form['student_password'] = password

    response = br.submit()

    return br


def getHeadings(br, company):

    url = company[7].strip('\'')

    companyPart = url.replace("http://tnp.dtu.ac.in/rm_2016-17/student/recruiter_profile/","")

    companyPart = urllib2.quote(companyPart)

    response = br.open("http://tnp.dtu.ac.in/rm_2016-17/student/recruiter_profile/"+companyPart)

    soup = BeautifulSoup(response, 'html.parser')

    headings = soup.find_all('div', attrs={'class': 'box-header with-border'})

    for i in range(len(headings)):
        headings[i] = headings[i].text.strip(' \t\n\r')

    return headings


def getCompanyData(br, company):

    url = company[7].strip('\'')

    companyPart = url.replace("http://tnp.dtu.ac.in/rm_2016-17/student/recruiter_profile/", "")

    companyPart = urllib2.quote(companyPart)

    response = br.open("http://tnp.dtu.ac.in/rm_2016-17/student/recruiter_profile/" + companyPart)

    soup = BeautifulSoup(response,'html.parser')

    content = soup.find_all('div',attrs={'class':'box-body'})

    # content[0] = company[0]

    for i in range(len(content)):
        content[i] = content[i].text.encode('utf-8')

        if content[i] != "":
            content[i] = content[i].replace("\n","")
            content[i] = content[i].replace("\r", "")
            content[i] = content[i].replace(",", "")

        else:
            content[i] = ""

    content.append(company[0]) # for company name

    return content

if __name__ == "__main__":

    # resume_manager.getData()

    flag = 0

    with open('../../companies_placement.csv','r') as companyFile:
        companies = csv.reader(companyFile)
        companies = list(companies)

    rollno = raw_input("Enter roll no:")
    password = raw_input("Enter password:")

    br = login(rollno, password)

    companyProfiles = []

    length = len(companies)

    counter = 0
    for company in companies:

        counter = counter+1

        print company[0] # company name

        if company[7] == "Link":
            continue

        if flag == 0:
            headings = getHeadings(br, company)
            flag = 1

        # if counter <= 324:
        #     continue

        content = getCompanyData(br, company)

        companyProfiles.append(content)

    # print companyProfiles

    with open('../../company_placement_profiles.csv', 'wb') as csv_file:
        spamwriter = csv.writer(csv_file, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)

        spamwriter.writerow(["Company Name", headings[0], headings[1], headings[2], headings[3], headings[4], headings[5], headings[6]])

        for i in range(len(companyProfiles)):

            if len(companyProfiles[i]) < 7:
                print companyProfiles[i]
                continue

            if len(companyProfiles[i]) == 7:
                spamwriter.writerow([companyProfiles[i][6], companyProfiles[i][0], companyProfiles[i][1], "",companyProfiles[i][2], companyProfiles[i][3], companyProfiles[i][4], companyProfiles[i][5]])
            else:
                spamwriter.writerow([companyProfiles[i][7], companyProfiles[i][0], companyProfiles[i][1], companyProfiles[i][2], companyProfiles[i][3], companyProfiles[i][4], companyProfiles[i][5], companyProfiles[i][6]])
