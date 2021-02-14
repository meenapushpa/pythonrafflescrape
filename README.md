# pythonrafflescrape

Raffle Scrape repo is used to scrape or crawl a website protected with Cloudflare. This is fully written in python requests module with the help of BeautifulSoup and Clourscraper modules to process the requests. Expanding this repo with 2captcha key module to solve the captchas before we fully process the request.

# Installation & Dependencies
  - Python 3.x
  - Create a python virtual environment
  - Install dependencies from requirements.txt
  - Import the cloudflare root and intermediate SSL certificates into keystore to trust the connection

    `pip install -r requirements.txt` will install the Python dependencies automatically.

# Usage

Execute the command   `python rafflescript.py` and will ask for couple of inputs to proceed further, please answer them and click enter. There are few values are hardcoded as of 13th Feb,2021 and will be variablised once all testing is completed. Few things to note !

- The script will end if it finds any exception during the execution.
- If you encounter the following error, you may need to re run the script one or more time to see the actual results
  ```
  cloudscraper.exceptions.CloudflareChallengeError:
  Detected a Cloudflare version 2 challenge, This feature is not available in the opensource (free) version.
  ```
  This doesn't mean that will have to go for newer version as this is compromised for the current requirement using our script. It just needs multiple runs to come output

# Flow of execution

  1. Fetch the input from User
  2. Proxying the request
  3. Parsing the request
  4. Scraping require tokens
  5. Entering Raffle
  6. Solving Captcha
  7. Completing the Transaction.


# Inflight works

Step 6 and 7 is yet to be completed.
