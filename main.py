from bs4 import BeautifulSoup
import requests

TEAM_SITE_1 = "https://us.movember.com/team/1997277"
TEAM_SITE_2 = "https://us.movember.com/team/1997277/mp/2"








def gen_team_mates(soup):
	mates = soup.find_all('div', class_='member-row')
	for m in mates:
		href = m.find('a').get('href')
		name = m.a.string
		mate = {}
		mate['href'] = href
		mate['name'] = name.ljust(23)
		yield mate

def parse_member_page(member):
	req = requests.get(member['href'])
	soup = BeautifulSoup(req.text, 'html.parser')
	move_count_soup = soup.find(id="key-statistic-value--moves-counter")
	move_count = move_count_soup.get_text().strip()
	stats = soup.find_all('div', class_='key-statistic-value')
	funds_raised = stats[4].get_text().strip()
	member['moves'] = move_count.ljust(5)
	if 'Funds Raised' in funds_raised:
		member['funds'] = funds_raised.split('Funds Raised')[0].strip().ljust(10)
	elif 'My target' in funds_raised:
		member['funds'] = funds_raised.split('My target')[0].strip().ljust(10)
	return member


def main(site):
	req = requests.get(site)
	main_site_html = req.text
	soup = BeautifulSoup(main_site_html, 'html.parser')
	members = [parse_member_page(mate) for mate in gen_team_mates(soup)]
	#return members[0]
	for m in members:
		print("%s MOVEs: %s FUNDs: %s" % (m['name'], m['moves'], m['funds']))

	

if __name__ == '__main__':
	x = main(TEAM_SITE_1)
	main(TEAM_SITE_2)