import sys
import os
import re
import importlib
import matplotlib.pyplot as plt
import matplotlib.ticker
# import json
from bs4 import BeautifulSoup
from urllib.request import urlopen
from datetime import datetime
from bballh2hcnst import *

# Use BeautifulSoup to scrape respective web page
def grab_url(fav, opp):
	url = 'http://mcubed.net/mlb/%s/%s.shtml' % (fav, opp)
	page = urlopen(url)
	return BeautifulSoup(page, 'lxml')

# Check if two teams exist and are not equal
def validate_teams(fav, opp):
	keys = [*full_names]
	if fav not in full_names or opp not in full_names:
		print('ERROR: one or both of the eams you specified is invalid. Please consult README for acceptable abbreviations')
		sys.exit(1)

	if fav == opp:
		print('ERROR: You cannot specify the same team twice')
		sys.exit(1)

# For years in which there wasn't a game in a matchup played
# Fill the gap years in between with data from the last valid year
# But make sure that data will not factor into the computation of
# win percentages
def update_to_today(year, stats):
	keys = [*stats]

	if len(keys) > 0:
		# this is the odd case of interleague matchups
		# there often exist big gaps in head-to-head history in these cases
		# basically we want to display that there was no change between years
		# where there weren't games played
		# but we also want to make sure that games don't 

		last_year = keys[len(keys) - 1]

		if year - last_year > 1:
			for gap_year in range(last_year + 1, year):
				stats[gap_year] = stats[last_year].copy()
				stats[gap_year]['gap_year'] = True

	return stats

# Make a running tally of a team's head-to-head records over the years
def tally_data(stats, data, playoff):
	year = int(data[1])

	# technically, you could have home playoff wins and home playoff losses as well
	# but the sample size is already so small just for playoff wins and losses already
	# playoff wins and playoff losses categories are really only meant for highly technical people
	# who argue that head to head records should only include regular season games
	# or that regular season and postseason head to head records should be disjoint
	
	if year not in stats:
		stats = update_to_today(year, stats)

		stats[year] = {'wins': 0,
					   'losses': 0,
					   'home_wins': 0,
					   'home_losses': 0,
					   'away_wins': 0,
					   'away_losses': 0,
					   'playoff_wins': 0,
					   'playoff_losses': 0,
					   'gap_year': False}

	if data[2] == "W":
		stats[year]['wins'] += 1

		if playoff is not None:
			stats[year]['playoff_wins'] += 1

		if data[0] == "H":
			stats[year]['home_wins'] += 1
		else:
			stats[year]['away_wins'] += 1
	elif data[2] == "L":
		stats[year]['losses'] += 1

		if playoff is not None:
			stats[year]['playoff_losses'] += 1

		if data[0] == "H":
			stats[year]['home_losses'] += 1
		else:
			stats[year]['away_losses'] += 1

	return stats

	# do nothing in a tie game because it doesn't count towards a win or a loss

# Use season-by-season head to head records to compute
# Overall head-to-head record statistics
def cum_win_percs(stats):
	win_percs = {}

	total_wins = 0
	total_losses = 0
	total_home_wins = 0
	total_home_losses = 0
	total_away_wins = 0
	total_away_losses = 0
	total_playoff_wins = 0
	total_playoff_losses = 0
	
	for key in stats:
		# if it is not a gap year then update the corresponding information
		# otherwise, just copy the data from previous year's entry
		if stats[key]['gap_year'] == False:
			total_wins += stats[key]['wins']
			total_losses += stats[key]['losses']
			total_home_wins += stats[key]['home_wins']
			total_home_losses += stats[key]['home_losses']
			total_away_wins += stats[key]['away_wins']
			total_away_losses += stats[key]['away_losses']
			total_playoff_wins += stats[key]['playoff_wins']
			total_playoff_losses += stats[key]['playoff_losses']

			# a special case because teams don't see each other every year
			# so many records will be 0-0, and we don't want to divide by 0
			overall_win_percentage = total_wins / (total_wins + total_losses) * 100 # this one will never be 0-0 though
			home_win_percentage = 0 if (total_home_wins == 0 and total_home_losses == 0) else (total_home_wins / (total_home_wins + total_home_losses) * 100)
			away_win_percentage = 0 if (total_away_wins == 0 and total_away_losses == 0) else (total_away_wins / (total_away_wins + total_away_losses) * 100)
			playoff_win_percentage = 0 if (total_playoff_wins == 0 and total_playoff_losses == 0) else (total_playoff_wins / (total_playoff_wins + total_playoff_losses) * 100)

			win_percs[key] = {'overall_win_percentage': overall_win_percentage,
					 	 	  'home_win_percentage': home_win_percentage,
					 	 	  'away_win_percentage': away_win_percentage,
					 	 	  'playoff_win_percentage': playoff_win_percentage}
		else:
			win_percs[key] = win_percs[key - 1]

	return win_percs

# Display visualization results in graphical format
def viz(cum_win_percs, fav, opp):
	x = [*cum_win_percs]

	y_overall = [cum_win_percs[val]['overall_win_percentage'] for val in [*cum_win_percs]]
	y_home = [cum_win_percs[val]['home_win_percentage'] for val in [*cum_win_percs]]
	y_away = [cum_win_percs[val]['away_win_percentage'] for val in [*cum_win_percs]]
	y_playoff = [cum_win_percs[val]['playoff_win_percentage'] for val in [*cum_win_percs]]

	plt.plot(x, y_overall, 'ro', label='Overall winning percentage')
	plt.plot(x, y_home, 'go', label='Home winning percentage')
	plt.plot(x, y_away, 'bo', label='Away winning percentage')
	plt.plot(x, y_playoff, 'mo', label='Playoff winning percentage')

	plt.title('%s vs %s' % (full_names[fav], full_names[opp]))

	plt.xlabel('Year')
	plt.ylabel('Win percentage')

	plt.legend(loc='upper right')

	plt.axis([min(x) - 1, max(x) + 1, 0, 100.0])

	locator_x = matplotlib.ticker.MultipleLocator(1)
	plt.gca().xaxis.set_major_locator(locator_x)

	locator_y = matplotlib.ticker.MultipleLocator(10)
	plt.gca().yaxis.set_major_locator(locator_y)

	plt.show()

# Pull the specified head to head record and process it
def search_data(fav, opp):
	h2h_data = grab_url(fav, opp)
	table = h2h_data.findAll('span', {'class': 'hovl'})
	stats = {}
	
	for index, elem in reversed(list(enumerate(table))):
		data = re.findall(r' (H|A) (\d\d\d\d)/\d\d/\d\d[\w\s\-\.()]* (W|L|T)', elem.text)
		
		if len(data) != 0:
			stats = tally_data(stats, data[0], re.search(r'!', elem.text))
		else:
			break

	# Because of interleague games, in some head to head records
	# the last game between two teams might have been played up to 3 years ago
	stats = update_to_today(datetime.now().year, stats)

	results = cum_win_percs(stats)

	# use the following lines to write data to a file confirming the data is accurate
	# with open('out.json', 'w') as outfile:
	# 	outfile.write(json.dumps(results, indent=4))

	viz(results, fav, opp)


def main():
	if len(sys.argv) != 3:
		print('USAGE: python3 bballh2hviz.py [TEAM1 TEAM2]')
		sys.exit(1)

	validate_teams(sys.argv[1], sys.argv[2])
	search_data(sys.argv[1], sys.argv[2])

if __name__ == '__main__':
	main()