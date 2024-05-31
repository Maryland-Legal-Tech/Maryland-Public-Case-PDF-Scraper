# Maryland-Public-Case-PDF-Scraper
 For Scraping the Public Case PDFs that the Court puts out daily.

## Overview
This scrapes the links for the PDFs located at https://www.mdcourts.gov/mdec/publiccases. Technically, the list itself is dynamically included to the page from https://www.mdcourts.gov/data/case/ which is the actualy url scraped in this program.

The program grabs the links and then compares it to a list of all the names of pdfs in my s3 bucket. If the file already exists in the s3 bucket then the program doesn't download it again. Otherwise the program downloads the pdf and saves it to the s3 bucket.

It is set to run once a day.

## TO Do
Set up some notifications to detect if the webpage is changed.

## Request File
If you want a copy of the PDFs please reach out. I have files starting from 5-26-24.
