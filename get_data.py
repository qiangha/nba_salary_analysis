import pickle
import requests
from bs4 import BeautifulSoup  
from bs4 import Comment
import pandas as pd

def data():

    '''This function creates the dataframe for my analysis'''
    
    with open ('player_dict', 'rb') as fr:
        player_stats = pickle.load(fr)  #player_dict contains players' names and their homepage urls

    dataframe=pd.DataFrame({'Player_name':[],'Years in League':[],'Minutes per Game':[],'Points per 36 minutes':[],'NBA ALL STAR':[],'Usage Rate':[],
                       'Offensive Win Share':[],'Defensive Win Share':[],'Obpm':[],'Dbpm':[],'Salary':[]})

    
    salary_cap={2014:63065000,2015:70000000,2016:94143000,2017:99093000,2018:101869000}   #salary cap by year 
    
    url_list = player_stats['url']
    for j in range(len(player_stats['url'])):
        player=player_stats['Player name'][j]
        #print (player)
        url=player_stats['url'][j]
        page=requests.get(url)
        #print(page.status_code)
        soup=BeautifulSoup(page.content,'html.parser')
        my_table=soup.find('table')
    
        #Construct features:
    
        #years in league up to 2018
        result=my_table.find_all('tr')[1].find('a').text
        years_in_league=2018-int(result.split('-')[0])
    
        if years_in_league>=2: #only selecting those who played in 2016, manually checked if they played in both 2016 and 2017
        
            #minutes per game
        
            rows=my_table.find_all('tr')[1:]
           
            for i in rows:
                if i.find('a'):
                    if i.find('a').text=='2016-17':
                        minutes_per_game=float(i.find_all('td')[6].text)
                        break
                    
        
        
            comments=soup.find_all(string=lambda text:isinstance(text,Comment))
            comment_list=[]
            for i in comments:
                a=BeautifulSoup(i, 'html.parser')
                if a.find('table'):
                    comment_list.append(a)
        
            #points per 36 minutes
            for i in comment_list:
                if i.find('caption').text=='Per 36 Minutes Table':
                    commentsoup=i
                    break
                
            table=commentsoup.find('table')
            rows=table.find_all('tr')[1:]
           
            for i in rows:
                if i.find('a'):
                    if i.find('a').text=='2016-17':
                        points_per_36_minutes=float(i.find_all('td')[27].text)
                        
                        break
                
          
            #nba all star
            nba_all_star=0
            for i in comment_list:
                if i.find('caption').text=='All-Star Games Table':
                    
                    nba_all_star=1   
                    break
        
        
        
        
            #usage rate and
            #offensive-win-shares and   defensive-win-shares
            #obpm and dbpm
            for i in comment_list:
                if i.find('caption').text=='Advanced Table':
                    commentsoup=i
                    break
        
        
            table=commentsoup.find('table')
            rows=table.find_all('tr')[1:]
        
        
            for i in rows:
                if i.find('a'):
                    if i.find('a').text=='2016-17':

                        usage_rate=float(i.find_all('td')[17].text)
                        offensive_win_share=float(i.find_all('td')[19].text)
                        defensive_win_share=float(i.find_all('td')[20].text)
                        obpm=float(i.find_all('td')[24].text)
                        dbpm=float(i.find_all('td')[25].text)

                        break
        
      
        
            #salary
            for i in comment_list:
                if i.find('caption').text=='Salaries Table':
                    commentsoup=i
                    break
        
        
            table=commentsoup.find('table')
            rows=table.find_all('tr')[1:]
        
           
            for i in rows:
                if i.find('th'):
                    if i.find('th').text=='2017-18':
                
                        salary=i.find_all('td')[2].text[1:]#the first charactwr is dollar sign
                        salary=int(salary.replace(',',''))
                        
                        break
                        
            
            #adjust salary according to salary cap
            
            
            #if the person changes team during 2014-2017, then the contract is signed when he last changes team
            #otherwise the contract is signed when the person joins nba or 2014 whichever is latest
            #normally contracts in nba last 4 years.
            
            #consturct the team by year lists
            for i in rows:
                if i.find('th'):
                    if i.find('a'):
                        team_list=[]
                        season_list=[]
                        season=i.find('th').text
                        season=int(season[:4])
                        if 2017>=season>=2014:
                            team_name=i.find('a').text
                            team_list.append(team_name)
                            season_list.append(season)
            season=2017
            if season_list[0]>=2014: #if joined after 2014, contract is signed on joining
                season=season_list[0]
            else:
                for i in range(3):
                    if team[i]!=team[i+1]:
                        season=season_list[i+1]
                        
            salary=(salary_cap[2018])*salary/(salary_cap[season])
                        
            #make adjustment to salary 
            #adjusting the contracts proportional to the difference in the current salary cap and 
            #the salary cap of the first year the contract is effective.
                    
            
            #add these to the dataframe
            dataframe= dataframe.append(pd.DataFrame({'Player_name':player,'Years in League':years_in_league,'Minutes per Game':minutes_per_game,'Points per 36 minutes':points_per_36_minutes,'NBA ALL STAR':nba_all_star,'Usage Rate': usage_rate, 'Offensive Win Share':offensive_win_share,'Defensive Win Share':defensive_win_share,'Obpm':obpm,'Dbpm':dbpm,'Salary':salary},index=[0]),ignore_index=True)


    return dataframe
        