from bs4 import BeautifulSoup
import mechanize
from prettytable import PrettyTable
import csv

def getData(rollno, password):
    absoluteUrl = "http://tnp.dtu.ac.in/rm_2016-17/intern/intern_login"

    br = mechanize.Browser()
    br.set_handle_robots( False )
    br.addheaders = [('User-agent', 'Firefox')]
    br.open(absoluteUrl)
    br.select_form(nr=0)
    br.form['intern_student_username_rollnumber'] = rollno
    br.form['intern_student_password'] = password

    response = br.submit()

    soup = BeautifulSoup(response,'html.parser')

    ul = soup.find('ul',attrs={'class':'timeline'})

    count = 0
    absoluteUrl = "http://tnp.dtu.ac.in/rm_2016-17/intern/intern_student/index"
    while count >= 0:

        print absoluteUrl
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
            jobopenings = links[4]
            print jobopenings
            m = links[len(links)-2].url.replace("http://tnp.dtu.ac.in/rm_2016-17/intern/intern_student/index/","")
            m = int(m)

        url = links[len(links)-3]
        value = url.url.replace("http://tnp.dtu.ac.in/rm_2016-17/intern/intern_student/index/","")
        if int(value) >= m:
            url = links[len(links) - 2]

        absoluteUrl = url.url

        count += 50

        response = br.follow_link(url)
        soup = BeautifulSoup(response, 'html.parser')

        ul = soup.find('ul', attrs={'class': 'timeline'})

    # print jobopenings

    response = br.follow_link(jobopenings)
    soup = BeautifulSoup(response, 'html.parser')

    table_jobopenings = soup.find('table',attrs={'id':'jobs_search'})

    table = PrettyTable(['Company Name', 'Branches', 'Application Deadline', 'B.Tech', 'M.Tech', 'MBA', 'DateofVisit'])

    links = br.links()

    trs = table_jobopenings.find_all('tr')

    companyDetails = []
    company = {}

    count = 1
    for link in links:

        partOfLink = link.url.find("http://tnp.dtu.ac.in/rm_2016-17/intern/intern_student/job_openings/")

        if partOfLink == -1:
            continue
        elif count != 1:
            response = br.follow_link(link)
            soup = BeautifulSoup(response, 'html.parser')

            table_jobopenings = soup.find('table', attrs={'id': 'jobs_search'})
            trs = table_jobopenings.find_all('tr')
        else:
            count += 1

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

            company['Company Name'] = temp[0]
            company['Branches'] = temp[1].replace(","," ")
            company['Application Deadline'] = temp[2]
            company['B.Tech'] = temp[3]
            company['M.Tech'] = temp[4]
            company['MBA'] = temp[5]
            company['DateofVisit'] = temp[6]

            companyDetails.append(company)

            if len(temp) == 7:
                table.add_row(temp)

        partOfLink = link.url.find("http://tnp.dtu.ac.in/rm_2016-17/intern/intern_student/job_openings/")

        # if partOfLink != -1:
        #     print link
        #     response = br.follow_link(link)
        #     soup = BeautifulSoup(response, 'html.parser')
        #
        #     table_jobopenings = soup.find('table', attrs={'id': 'jobs_search'})
        #     trs = table_jobopenings.find_all('tr')
        # else:
        #     continue

    # print table

    # print companyDetails
    print "Companies ----------------------"

    # for company in companyDetails:
    #     response = br.click_link(predicate='window.open()')
    #     # response = br.follow_link(company['linkForCompany'])
    #     soup = BeautifulSoup(response, 'html.parser')
    #     html = soup.find('html')
    #     print html.text
    #     break

    with open('../../companies_internship.csv', 'wb') as csv_file:
        spamwriter = csv.writer(csv_file, delimiter=',',
                                quotechar='|', quoting=csv.QUOTE_MINIMAL)

        spamwriter.writerow(['Company Name', 'Branches', 'Application Deadline', 'B.Tech', 'M.Tech', 'MBA', 'DateofVisit', 'Link'])

        for company in companyDetails:
            spamwriter.writerow([company['Company Name'], company['Branches'], company['Application Deadline'], company['B.Tech'], company['M.Tech'], company['MBA'], company['DateofVisit'], company['LinkForCompany']])

    return companyDetails

# getData()

if __name__ == "__main__":

    rollno = raw_input("Enter roll no:")
    password = raw_input("Enter password:")
    getData(rollno, password)
