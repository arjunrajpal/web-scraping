from bs4 import BeautifulSoup
import mechanize
from prettytable import PrettyTable
import csv

def getData(rollno, password):
    absoluteUrl = "http://tnp.dtu.ac.in/rm_2016-17/login/"

    br = mechanize.Browser()
    br.set_handle_robots( False )
    br.addheaders = [('User-agent', 'Firefox')]
    br.open(absoluteUrl)
    br.select_form(nr=0)
    br.form['student_username_rollnumber'] = rollno
    br.form['student_password'] = password

    response = br.submit()

    soup = BeautifulSoup(response,'html.parser')

    ul = soup.find('ul',attrs={'class':'timeline'})

    count = 0
    absoluteUrl = "http://tnp.dtu.ac.in/rm_2016-17/login/index"
    while count >= 0:

        # print absoluteUrl
        li_time_label = ul.find_all('li',attrs={'class':'time-label'})

        if len(li_time_label) == 0:
            break

        div_timeline_item = ul.find_all('div',attrs={'class':'timeline-item'})

        for i in range(len(li_time_label)):

            print li_time_label[i].text.strip(' \t\n\r')

            time = div_timeline_item[i].span.text.strip(' \t\n\r')
            time = time.replace("&nbsp","")
            time = time.replace(";","")
            timelineHeader = div_timeline_item[i].find('h4',attrs={'class':'timeline-header'})

            # if timelineHeader:
            timelineBody = div_timeline_item[i].find('div',attrs={'class':'timeline-body'})
            timelineHeaderUp = div_timeline_item[i].find('h3',attrs={'class':'timeline-header up'})

            print time
            print timelineHeader.text.strip(' \t\n\r')
            # print timelineBody.text,"\n"

            p = timelineBody.find_all('p')
            for j in range(len(p)):
                print p[j].text
            print "\n-------------------"

            timelineHeader = ""
            timelineBody = ""

        print "-------End of Page ",count,"-------"


        links = br.links()

        if count == 0:
            # print links
            jobopenings = links[5]
            # print jobopenings
            # print links[len(links)-2]
            m = links[len(links)-2].url.replace("http://tnp.dtu.ac.in/rm_2016-17/student/index/","")
            m = int(m)

        url = links[len(links)-3]
        value = url.url.replace("http://tnp.dtu.ac.in/rm_2016-17/student/index/","")
        if int(value) >= m:
            url = links[len(links) - 2]

        absoluteUrl = url.url

        count += 50

        response = br.follow_link(url)
        soup = BeautifulSoup(response, 'html.parser')

        ul = soup.find('ul', attrs={'class': 'timeline'})

    # print jobopenings

    response = br.open("http://tnp.dtu.ac.in/rm_2016-17/student/search_job_openings/")
    soup = BeautifulSoup(response, 'html.parser')

    # table_jobopenings = soup.find('table',attrs={'id':'jobs_search'})

    table = PrettyTable(['Company Name', 'Branches', 'Application Deadline', 'B.Tech', 'M.Tech', 'MBA', 'DateofVisit'])

    # links = br.links()

    trs = soup.find_all('tr')

    companyDetails = []
    company = {}

    count = 1
    for i in range(1):

        for tr in trs:

            tds = tr.find_all('td')

            if len(tds) == 0:
                continue
            else:
                company = {}
                linkForCompany = tr['onclick']
                linkForCompany = linkForCompany.replace("void window.open(","")
                linkForCompany = linkForCompany.replace(")","")

                company = {'LinkForCompany':linkForCompany}

            temp = []
            for td in tds:
                i = td.find_all('i')
                if len(i) > 0:
                    degree = i[0]['class'][1]
                    temp.append(degree)
                else:
                    # print td.text
                    temp.append(td.text)

            company['Company Name'] = temp[0].replace(","," ")
            company['Branches'] = temp[1].replace(","," ")
            company['Application Deadline'] = temp[2]
            company['B.Tech'] = temp[3]
            company['M.Tech'] = temp[4]
            company['MBA'] = temp[5]
            company['DateofVisit'] = temp[6]

            companyDetails.append(company)

            if len(temp) == 7:
                table.add_row(temp)

    # print table

    # print companyDetails

    print "Companies ----------------------"

    with open('../../companies_placement.csv', 'wb') as csv_file:
        spamwriter = csv.writer(csv_file, delimiter=',',
                                quotechar='|', quoting=csv.QUOTE_MINIMAL)

        spamwriter.writerow(['Company Name', 'Branches', 'Application Deadline', 'B.Tech', 'M.Tech', 'MBA', 'DateofVisit', 'Link'])

        for company in companyDetails:
            spamwriter.writerow([company['Company Name'].encode("utf-8"), company['Branches'].encode("utf-8"), company['Application Deadline'].encode("utf-8"), company['B.Tech'].encode("utf-8"), company['M.Tech'].encode("utf-8"), company['MBA'].encode("utf-8"), company['DateofVisit'].encode("utf-8"), company['LinkForCompany'].encode("utf-8")])

    return companyDetails

# getData()

if __name__ == "__main__":

    rollno = raw_input("Enter roll no:")
    password = raw_input("Enter password:")
    getData(rollno,password)
