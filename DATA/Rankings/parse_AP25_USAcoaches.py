import urllib2, csv

#tables = ['AP Top 25', 'USA Today Coaches Poll']
headers = [['Rank', 'Team', 'Record', 'Points']]

rankings_url = 'http://espn.go.com/mens-college-basketball/rankings'

def getRankings(rankings_url=rankings_url, year='2014'):
    webpage = urllib2.urlopen(rankings_url).read()

    file_AP25 = open('APtop25_%s.csv' % year, 'w')
    file_USAcoaches = open('USAtodayCoaches_%s.csv' % year, 'w')
    #file_AP25 = open('a.test', 'w')
    #file_USAcoaches = open('b.test', 'w')

    idx = 0

    # Get AP top 25 poll first
    for file in [file_AP25, file_USAcoaches]:
        idx += webpage[idx:].find('stathead')
        ti = idx

        # 100 is arbitrary
        idx += 100
        
        teams = []
        
        for j in xrange(25):
            # Rank will be
            rank = j + 1
            
            # Get team name e.g. Arizona
            ti += webpage[ti:].find('basketball/team/')
            ti += webpage[ti:].find('>')
            end = ti + webpage[ti:].find('<')
            team_name = webpage[ti+1:end]

            # Get record and points
            record, points, count = '', 0, 0
            while count < 2:
                ti += webpage[end:].find('center')
                ti += webpage[ti:].find('>')
                end = ti + webpage[ti:].find('<')
                attr = webpage[ti+1:end]
                #print (count, attr)
                if attr.find('-') != -1:
                    # Get record e.g. 20-0
                    record = attr
                    count += 1
                elif attr == '':
                    continue
                else:
                    # Get points e.g. 1653
                    count += 1
                    points = int(attr.replace(',', ''))

            # One team's info found
            teams.append([rank, team_name, record, points])

        print teams

        writer = csv.writer(file)
        writer.writerows(headers)
        writer.writerows(teams)

        file.close()

if __name__ == '__main__':
    # get rankings from 2003 through 2013
    for y in xrange(2003, 2014):
        year = str(y)
        url = 'http://espn.go.com/mens-college-basketball/rankings/_/year/%s/week/14/seasontype/2' % year
        getRankings(url, year)

    # get 2014 rankings
    getRankings()
    exit('Finished getting rankings!')
