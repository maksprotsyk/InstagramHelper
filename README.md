# Instagram Helper Bot
<img src="images/logo.png" width="250"/>

## Table of contents
* [Description](#description)
* [Installation](#installation)
* [Usage](#usage)
* [Screenshots](#screenshots)
* [Credits](#credits)
* [License](#license)


## Description:
Telegram bot that will help you effectively use your Instagram profile.
Its main functions include:
* Getting a list of recommended Profiles
* Viewing posts of the given profiles
* Visiting this accounts by link

## Installation:
```bash
pip install -r requirements.txt
```
(If you get unexpected errors from the igramscrapper,
 clone the [repository](https://github.com/realsirjoe/instagram-scraper)
 and put igramscraper folder in the project folder)

 ## Usage
 The project consists of 4 module packages and one main module: [bot.py](bot.py)
 ### Package [Instagram](modules/instagram)
 #### Contains two modules:
 * [parser.py](modules/instagram/parser.py)
 * [user_interaction.py](modules/instagram/user_interaction.py)
 
 parser.py allows user to access instagram profiles with requests and BeautifulSoup
 
 
 ## Screenshots
 
### Bot meets you with a greeting message

<img src="images/Screenshot1.png" width="450"/>

### Bot sends some recommendations

<img src="images/Screenshot2.png" width="450"/>



## Credits:
* Diana Kmet
* Maksym Protsyk

## License
[MIT](https://choosealicense.com/licenses/mit/)
