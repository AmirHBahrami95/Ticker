from coinlore.client import Client
from db.CoinTable import CoinTable
import initializer.utils as utils
import json
import os
import time

"""
	this section helps initialize the names of coins so that we have all the fucking id's ffs
	and is supposed to run before you start using actual program - so fetch the data

	DO NOT use this script with a loop without at least sleep(3), as it will overrun the 
	api system and you will be marked by them as an asshole (attacker)
"""

def updateLastRead(lastRead):
	with open("{}/lastRead.json".format(os.environ['TICKER_DATA_DIR']),'w+') as fout:
		json.dump({'read':lastRead},fout)

def getLastRead():
	lastRead=0
	try:
		with open("{}/lastRead.json".format(os.environ['TICKER_DATA_DIR']),'r') as readF:
			lastRead=json.load(readF)['read']
	except:
		print('lastRead.json did not exist, initializing...')
		pass
	return lastRead

def __getAndSaveCoins(client,lastRead,verbose=True):
	coins=client.getcoins(start=str(lastRead),limit=str(100))['data']
	coinRecords=utils.getCoinRecords(coins)
	with CoinTable("{}/coins.sql".format(os.environ['TICKER_DATA_DIR'])) as db:
		db.insertN(coinRecords)
		if verbose:
			print('wrote to {}/coins.sql'.format(os.environ['TICKER_DATA_DIR']))

def readIds(verbose=True):
	lastRead=getLastRead()
	client = Client();
	if verbose:
		print('reading 1000 coins, it\'ll take 30 seconds (to avoid being marked as brute forcer)')
	for i in range(10):
		if verbose:
			print("reading coins from {} to {}...".format(lastRead,lastRead+100))
		__getAndSaveCoins(client,lastRead,verbose)
		lastRead+=100
		updateLastRead(lastRead+100)
		time.sleep(3)
