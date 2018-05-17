# MLB head to head record visualizations  
  
Plot the head to head history between two teams  

## How to  
  
* Run it using: ```python3 bballh2hviz.py [TEAM1 TEAM2]```  
* Refer to ```bballh2hcnst.py``` for team names and their respective nicknames  
* Data is scraped using BeautifulSoup  
* Visualizations are displayed using PyPlot  
* To additionally view year-by-year data in JSON format, uncomment line 7 and lines 194-195  
  
## Extra Notes
  
* Postseason games (including World Series matchups) are included in the visualizations  
* Games before the first WS in 1903 are included because they are officially tallied in the record books  
* For interleague series, the last valid year's data points are displayed for gap years (a.k.a. years in which a game between those two teams was not played), but those data points do not count towards overall win percentage and other calculations because they are just filler points  

## Credit  
  
All data was gathered from mcubed.net  
  
## Next Update  
  
Add feature allowing users to specify which records (overall, home, away, playoff) they want to view  