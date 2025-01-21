# Ticker
Receive crypto coins data for free and get notified for specific price changes. save informations for later
analysis and reduction of bandwidth and customize the program the way you want it

## How it works
First you need to initialize the data you need so run __main.py__ with __init__ command and wait a few seconds

Second, you need to see the list of coins you have initialized so far. do that with __coins__ command

And finally - set a __TICK__ with __listen__ command and passing options like `--tick` and so on

### Options

simply run the __main.py__ program form commandline for it

```bash
	python3 . -h
```

here's a quick shot at the help:

```bash
sage: ticker [-h] [-v] [-n] [-t [TICK]] {init,coins,listen} [parameters ...]

get custom crypto coins prices from CoinLore (free 100%)

positional arguments:
  {init,coins,listen}
  parameters

options:
  -h, --help            show this help message and exit
  -v, --verbose
  -n, --notification    enable notification sound when a new response arrives (only effective when "listen"ing)
  -t [TICK], --tick [TICK]
                        how long before fetching prices again (minutes)

By https://github.com/AmirHBahrami95
```

### TODO
- [ ] save each response in another sqlite3 file for later analysis
- [ ] if program is interrupted, continue where you left off

### Contribution
This program uses [Coinlore](https://www.coinlore.com) , so go check it out it's completely free to use their api's (and their website's
insights ftm)

