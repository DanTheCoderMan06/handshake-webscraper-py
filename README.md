# Handshake Webscraper

## Description
Just a simple webscraper I used to get a bunch of jobs from handshake into a csv.

## Features
- Scrapes job titles, company names, images, and links.
- Supports pagination 
- Outputs the data to a CSV file with formatted columns for easy reading.
- Working as of 11/13/2024

## Table of Contents
- [Installation](#installation)
- [Environment Variables](#environment-variables)
- [Usage](#usage)
- [License](#license)

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/DanTheCoderMan06/handshake-webscraper-py.git
   cd src

2. **Install required packages**:
   ```bash
   pip install -r requirements. txt

3. **Make sure firefox is installed**:

## Environment Variables
   ```bash
   LOGIN_URL=the login page for your universitys handshake
   JOBS_URL=The link to the page with all the filters applied
   BASE_URL=The base url of handshake
   OUTPUT_CSV=The name of the genreated csv file.

## Usage
  Run the file and log into your handshake in the new window.
  Press enter when log in is successful
  Run the program for as long as you like, and press enter to start the csv writing process.

## License
This project is licensed under the MIT License.
