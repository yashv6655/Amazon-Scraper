A Webscraper For [amazon.com](https://amazon.com).

## Get Started:

### Install Python

If Python isn't installed on your device, [click here](https://www.python.org/downloads/) to download the latest version. Check the `PATH` variable box. If you have Windows, install the executable installer in order to change the `PATH` variable.

### Install Chromedriver

Make sure to install the correct version of [chromedriver](https://chromedriver.chromium.org/downloads) for your Google Chrome. After installing, unzip the folder and move the `chromedriver.exe` file inside the project folder.

How to check current version of Chrome:
- Click the three dots in the top right corner.
- Hover over "Help"
- Click "About Google Chrome" and check the version.

### Install Project Dependencies in a Virtual Environment

After downloading the project, execute the following lines in the command line/terminal, inside the project folder, in the following order:
- `python -m venv venv`
- `source venv/Scripts/activate` (**Note**: If on a Mac/Linux machine, use `source venv/bin/activate`)
- `pip install -r requirements.txt`

### Run the Project

Run `python scraper.py` in the terminal.

### Change the Search Parameters

All the search parameters can be changed in the `amazon_config.py` file.

### Get Product Reports

After running `scraper.py`, the program creates a file in the `reports` directory. Copy and paste the code into an online JSON formatter for better readability. The first item in the file is the cheapest item available.
