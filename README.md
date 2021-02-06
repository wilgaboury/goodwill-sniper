# Sniper for Goodwill Online Shopping

This is a command line tool for sniping auctions on the goodwill website (https://www.shopgoodwill.com/)

## Usage

Using the command line go to the location that this code was downloaded and type 'python sniper.py [args]' in order to use

## Explination of config.json

Make a copy of config-example.json named config.json in order for program to run.

* username ~ your username for the shop goodwill website
* password ~ your password for the shop goodwill website
* bid_before_seconds ~ the amount of time to for the process to start sniping before the bid ends
* port ~ the sniping process works in a background thread. In order to communate with it the command line tool needs to send data over a port. Choese a port that is generally unused (somthing above 10,000 but not more than 50,000, use https://www.random.org/integers/?num=1&min=5001&max=49151&col=5&base=10&format=html&rnd=new to generate)