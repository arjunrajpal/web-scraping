import mechanize
from bs4 import BeautifulSoup
from prettytable import PrettyTable
import csv
import resume_manager


def login():

    absoluteUrl = "http://tnp.dtu.ac.in/rm_2016-17/intern/intern_login"

    br = mechanize.Browser()
    br.set_handle_robots(False)
    br.addheaders = [('User-agent', 'Firefox')]
    br.open(absoluteUrl)
    br.select_form(nr=0)
    br.form['intern_student_username_rollnumber'] = "2k14/se/021"
    br.form['intern_student_password'] = "Tintinrajpal@11"

    response = br.submit()

    return br


def getHeadings(br, company):

    response = br.open(company[7].strip('\''))

    soup = BeautifulSoup(response, 'html.parser')

    headings = soup.find_all('div', attrs={'class': 'box-header with-border'})

    for i in range(len(headings)):
        headings[i] = headings[i].text.strip(' \t\n\r')

    return headings


def getCompanyData(br, company):

    response = br.open(company[7].strip('\''))

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

    with open('../../../Desktop/companies.csv','r') as companyFile:
        companies = csv.reader(companyFile)
        companies = list(companies)

    br = login()

    companyProfiles = []

    length = len(companies)

    counter = 0
    for company in companies:

        counter += 1

        print company[0] # company name

        if company[7] == "Link":
            continue

        if flag == 0:
            headings = getHeadings(br, company)
            flag = 1

        content = getCompanyData(br, company)

        companyProfiles.append(content)

        # if company[0] == "Faircent":
        #     break

    # print companyProfiles

    with open('../../company_profiles_internship.csv', 'wb') as csv_file:
        spamwriter = csv.writer(csv_file, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)

        spamwriter.writerow(["Company Name", headings[0], headings[1], headings[2], headings[3], headings[4], headings[5], headings[6]])

        for i in range(len(companyProfiles)):

            if len(companyProfiles[i]) == 7:
                spamwriter.writerow([companyProfiles[i][6], companyProfiles[i][0], companyProfiles[i][1], "",companyProfiles[i][2], companyProfiles[i][3], companyProfiles[i][4], companyProfiles[i][5]])
            else:
                spamwriter.writerow([companyProfiles[i][7], companyProfiles[i][0], companyProfiles[i][1], companyProfiles[i][2], companyProfiles[i][3], companyProfiles[i][4], companyProfiles[i][5], companyProfiles[i][6]])
