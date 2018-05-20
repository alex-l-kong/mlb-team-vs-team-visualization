# MLB head to head record visualizations  
  
Plot the head to head history between two teams  

## How to  
  
* Run it using: ```python3 bballh2hviz.py [-ohap] TEAM1 TEAM2```  
* Refer to ```bballh2hcnst.py``` for team names and their respective nicknames  
* Data is scraped using BeautifulSoup  
* Visualizations are displayed using PyPlot  
* To additionally view year-by-year data in JSON format, uncomment line 7 and lines 194-195  
* A list of team nicknames and their associated teams:  
  
```json
{
	"ari": "Arizona Diamondbacks",
	"atl": "Atlanta Braves",
	"bal": "Baltimore Orioles",
	"bos": "Boston Red Sox",
	"chi": "Chicago Cubs",
	"wsx": "Chicago White Sox",
	"cin": "Cincinnati Reds",
	"cle": "Cleveland Indians",
	"col": "Colorado Rockies",
	"det": "Detroit Tigers",
	"hou": "Houston Astros",
	"kc": "Kansas City Royals",
	"laa": "Los Angeles Angels",
	"la": "Los Angeles Dodgers",
	"mia": "Miami Marlins",
	"mil": "Milwaukee Brewers",
	"min": "Minnesota Twins",
	"nym": "New York Mets",
	"nyy": "New York Yankees",
	"oak": "Oakland Athletics",
	"phi": "Philadelphia Phillies",
	"pit": "Pittsburgh Pirates",
	"sd": "San Diego Padres",
	"sf": "San Francisco Giants",
	"sea": "Seattle Mariners",
	"stl": "St. Louis Cardinals",
	"tb": "Tampa Bay Rays",
	"tex": "Texas Rangers",
	"tor": "Toronto Blue Jays",
	"wsh": "Washington Nationals"
}
```
  
* Flags:  
	* -o: overall win percentage
	* -h: home win percentage  
	* -a: away win percentage  
	* -p: playoff win percentage  
  
## Extra Notes
  
* Postseason games (including World Series matchups) are included in the visualizations  
* Games before the first WS in 1903 are included because they are officially tallied in the record books  
* For interleague series, the last valid year"s data points are displayed for gap years (a.k.a. years in which a game between those two teams was not played), but those data points do not count towards overall win percentage and other calculations because they are just filler points  

## Credit  
  
All data was gathered from mcubed.net  
  
## Next Update  
  
Coming soon  
