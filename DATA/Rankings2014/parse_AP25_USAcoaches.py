import urllib2, csv

#tables = ['AP Top 25', 'USA Today Coaches Poll']
headers = [['Rank', 'Team', 'Record', 'Points']]
rankings_url = 'http://espn.go.com/mens-college-basketball/rankings'

def getRankings(rankings_url=rankings_url):
    webpage = urllib2.urlopen(rankings_url).read()

    file_AP25 = open('APtop25.csv', 'w')
    file_USAcoaches = open('USAtodayCoaches.csv', 'w')

    idx = 0

    # Get AP top 25 poll first
    for file in [file_AP25, file_USAcoaches]:
        idx += webpage[idx:].find('stathead')
        ti = idx
        
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
            record, points = '', 0
            for k in xrange(2):
                ti += webpage[end:].find('center')
                ti += webpage[ti:].find('>')
                end = ti + webpage[ti:].find('<')
                attr = webpage[ti+1:end]
                if attr.find('-') != -1:
                    # Get record e.g. 20-0
                    record = attr
                elif attr.find(',') != -1:
                    # Get points e.g. 1653
                    points = int(attr.replace(',', ''))
                    break
            
            # One team's info found
            teams.append([rank, team_name, record, points])


        print teams

        writer = csv.writer(file)
        writer.writerows(headers)
        writer.writerows(teams)

        file.close()

if __name__ == '__main__':
    getRankings()
    exit('Finished getting rankings!')
