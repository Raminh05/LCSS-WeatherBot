LCSS-WeatherBot
It's a weather bot, that runs in a Discord server! Gathers data from Environment Canada.

Planned Features:
- ~~Status (rich presence) for the bot (it will show: "playing with the weather")~~ (Done)
- ~~Auto update a certain channel title (maybe a vc or text) in the discord server to display temperature data (e.g. "Temperature: 8 degrees")~~ (Done as of 03.12.2021)
- Auto-update data every 1hr 30minutes. @tasks.loop maybe?
- ~~For weather data sent to text from bot commands, a proper graphical interface to display data is "planned" (embeds)~~ (Done as of 03.12.2021)
- ~~Conditional weather icons (time and weather condition). For example, a clear weather icon that can either have a moon or sun depending on time of day.~~ (Done as of 03.18.2021)
- Fix the UX (optimization, make country and city args OPTIONAL)
- Print local time for specified location (instead of just doing EST/EDT)
- For London, show weather alert in the embed if there is an alert.


Prerequisities:
- Requests
- BeautifulSoup
- Discord.py
- Datetime
- Json
