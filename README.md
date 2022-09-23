## New Holiday Webhook
A Python script that scrapes data about state holidays around the world and processes it into Discord announcements for a specific server.

### How to use
First, you need API keys for the site used - abstractapi.com. Those keys (recommended number - 10) and a Discord webhook token should be put in environmental variables called **APIKEYLIST** and **TOKENKEY** respectively.
You will also need to fill the .json file yourself - the supplied role IDs are for the server I made the script for.

### Dependencies
The only module not included in the standard Python installation that is used is the httpx module. It can be installed with the **pip install httpx** command.
