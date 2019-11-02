import re
import datetime
import requests
from bs4 import BeautifulSoup
import pandas as pd
import pickle as pkl
import os


def fetch_shuangseqiu_result(url):
	page = requests.get(url)
	assert page.status_code == 200

	page_content = page.content.decode('gbk')
	soup = BeautifulSoup(page_content, 'lxml')

	date = soup.find('span', attrs={'class': 'span_right'}).text[:18]
	year, month, day = re.findall('[0-9]+', date)
	date = datetime.date(int(year), int(month), int(day))

	red_balls = [int(e.text.strip()) for e in soup.find_all('li', class_='ball_red')]
	blue_ball = int(soup.find('li', class_='ball_blue').text.strip())

	sales, pool_size = re.findall('[0-9,]+元', page_content)
	sales = float(sales[:-1].replace(',', ''))
	pool_size = float(pool_size[:-1].replace(',', ''))

	price = soup.find_all('table', class_='kj_tablelist02')[1]
	# read_html doesn't work with bs4.Tag
	price: pd.DataFrame = pd.read_html(str(price))[0]

	price_money, price_count = {}, {}
	for _, row in price.iterrows():
		if row[0].endswith('等奖'):
			price_count[row[0]] = 0 if '--' in row[1] else float(row[1])
			price_money[row[0]] = 5000000 if '--' in row[2] else float(row[2])

	return {'date': date, 'red_balls': red_balls, 'blue_ball': blue_ball, 'pool_size': pool_size,
			'price_count': price_count, 'price_money': price_money}



def download_shuangseqiu(save_dir=None):
	try:
		from tqdm import tqdm
	except:
		def tqdm(obj):
			return obj

	save_dir = save_dir or './data/'
	save_path = os.path.join(save_dir, 'shuangseqiu.pkl')
	try:
		os.mkdir(save_dir)
	except:
		pass

	url = 'http://kaijiang.500.com/shtml/ssq/19002.shtml'
	page = requests.get(url)
	assert page.status_code == 200
	page_content = page.content.decode('gbk')
	soup = BeautifulSoup(page_content, 'lxml')

	all_urls = [i.get('href') for i in soup.find_all('a') if i.get('href', '').startswith('http://kaijiang.500.com/shtml/ssq/')]

	res = []
	for url in tqdm(all_urls):
		res.append(fetch_shuangseqiu_result(url))

	with open(save_path, 'wb') as f:
		pkl.dump(res, f)

	print('Data download complete. Number of records: {}'.format(len(res)))



if __name__ == '__main__':
	import argparse

	parser = argparse.ArgumentParser()
	parser.add_argument('which', help='Which game data to download.')
	args = parser.parse_args()

	if args.which.lower() == 'shuangseqiu':
		download_shuangseqiu()
