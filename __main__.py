from initializer.id_reader import readIds
from datetime import datetime
from db.CoinTable import CoinTable
from coinlore.client import Client
import simpleaudio as sa
import argparse
import time
import sys
import os

os.environ['TICKER_DATA_DIR']="{}/data".format(os.getcwd()) # DO THIS BEFORE ANYTHING

parser = argparse.ArgumentParser(
	prog='ticker',
	description='get custom crypto coins prices from CoinLore (free 100%)',
	epilog='By https://github.com/AmirHBahrami95'
)

parser.add_argument('command',nargs=1,choices=['init','coins','listen'])
parser.add_argument('parameters',nargs='*')
parser.add_argument('-v', '--verbose', action='store_true')
parser.add_argument('-n', '--notification', action='store_true',help='enable notification sound when a new arrives (only effective when "listen"ing)')
parser.add_argument('-t', '--tick', nargs='?',type=int, help='how long before fetching prices again (minutes)',default=1)

# TODO add functionality to pick up where you left off last time in 
# case the program is accidentally closed, so the tick is not reset
# this is to make sure the timestamps don't get wrecked for later 
# analysis -- also : if the leftOff timestamp is 16:00 and right now
# it's 16:07 (less than 10 minutes) wait until leftOff + `10

args = parser.parse_args()

command=args.command[0]
if command == 'init':
	readIds(args.verbose)

elif command == 'coins':
	with CoinTable("{}/coins.sql".format(os.environ['TICKER_DATA_DIR'])) as db:
		if len(args.parameters)==0:
			db.printCoins(db.getAll())
		else :
			for p in args.parameters:
				try:
					db.printCoins(db.getBySymbol(p))
				except:
					print("found nothing for {}".format(p))
					sys.exit()
		

# TODO add support for multiple coins (later...maybe) OR just start another ticker process!
elif command == 'listen':
	if len(args.parameters)==0:
		print('please provide a coin symbol')
	else:
		client=Client()
		coinId=None
		with CoinTable("{}/coins.sql".format(os.environ['TICKER_DATA_DIR'])) as db:
			try:
				coinId=db.getBySymbol(args.parameters[0])[0][0];
			except:
				print("invalid symbol {}".format(args.parameters[0]))
				sys.exit()

		# listening loop
		while True:
			currentInfo=client.getcoin(coinId)
			rightNow=datetime.now()
			# TODO save the rightNow's full datetime and currentInfo's prices in a separate
			# sql file for later analysis (if u cannot find candle data out there) then
			# pass --tick as 1, so it'll get all 1 minute candles
			# ALSO - save these changes in regard to later anaylsis for a full day ==> save 
			# day column separate than time, so u'll get less fucked when using them later
			print("[{}:{}]\t{} ${}".format(
				rightNow.hour
				,rightNow.minute
				,currentInfo['symbol']
				,currentInfo['price_usd']
			))
			if args.notification:
				wave=sa.WaveObject.from_wave_file("{}/notif.wav".format(os.environ['TICKER_DATA_DIR']))
				play=wave.play()
				play.wait_done()
			time.sleep((args.tick*60) +5) # in minutes. +5 is to make sure a minute sure passes before catching next candle

