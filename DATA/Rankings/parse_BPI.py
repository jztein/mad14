# ESPN's BPI Basketball Power Index
# ranks 351 teams, trying to predict which 68 teams make that NCAA tournament

import urllib2, csv

headers = [['Rank', 'Team', 'Conf', 'BPI', 'PVA', 'Conf_rk', 'Record', 'RAW', 'RAW_rk','SOS', 'SOS_rk', 'Var', 'Var_rk']]

rankings_url = 'http://espn.go.com/mens-college-basketball/bpi'

def getRankings(rankings_url=rankings_url, year='2014'):
    webpage = urllib2.urlopen(rankings_url).read()

    file_BPI = open('BPI_%s.csv' % year, 'w')
    #file_AP25 = open('a.test', 'w')

    idx = 0

    # Get AP top 25 poll first
    idx += webpage[idx:].find('VAR RK')
    ti = idx
    
    # 100 is arbitrary
    idx += 100
    
    teams = []

    rank = 0
    while True:
        pva, conf_rk, w_l, raw, raw_rk,sos, sos_rk, var, var_rk =\
        '', '', '', '', '', '', '', '', ''

        # BPI
        rank += 1
        
        # Get team name e.g. Arizona
        tId = webpage[ti:].find('/teamId/')
        if tId == -1:
            # finished finding all teams
            break
        ti += tId
        ti += webpage[ti:].find('>')
        end = ti + webpage[ti:].find('<')
        team_name = webpage[ti+1:end]

        # Conf
        ti = end + len('</a></td><td>')
        end = ti + webpage[ti:].find('<')
        conf = webpage[ti:end]

        # BPI
        ti = end + webpage[end:].find('sortcell')
        ti += len('sortcell">')
        end = ti + webpage[ti:].find('<')
        bpi = webpage[ti:end]

        other_headers = [pva, conf_rk, w_l, raw, raw_rk, 
                         sos, sos_rk, var, var_rk]
        for i in xrange(len(other_headers)):
            ti = end + webpage[end:].find('right')
            ti += len('right">')
            end = ti + webpage[ti:].find('<')
            other_headers[i] = webpage[ti:end]
                
        # One team's info found
        teams.append([rank, team_name, conf, bpi] + other_headers)

    #print teams

    writer = csv.writer(file_BPI)
    writer.writerows(headers)
    writer.writerows(teams)

    file_BPI.close()

if __name__ == '__main__':
    # get rankings from 2012 through 2013
    for year in xrange(2012, 2014):
        y = str(year)
        url = 'http://espn.go.com/mens-college-basketball/bpi/_/season/%s' % y
        getRankings(url, y)

    # get 2014 rankings
    getRankings()

    exit('Finished getting rankings!')
