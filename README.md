# Maryland-Public-Case-PDF-Scraper
 For Scraping the Public Case PDFs that the Court puts out daily.

> **⚠️ This scraper no longer works.** As of November 2026, the Court has added CAPTCHAs (bot protection) to https://www.mdcourts.gov/data/case/. All automated requests now receive a `403 Forbidden` response, so the program can no longer retrieve the list of PDFs.

## Overview
This scrapes the links for the PDFs located at https://www.mdcourts.gov/mdec/publiccases. Technically, the list itself is dynamically included to the page from https://www.mdcourts.gov/data/case/ which is the actualy url scraped in this program.

The program grabs the links and then compares it to a list of all the names of pdfs in my backblaze s3 bucket. If the file already exists in the bucket then the program doesn't download it again. Otherwise the program downloads the pdf and saves it to the bucket.

It is set to run once a day.

## TO Do
Set up some notifications to detect if the webpage is changed.
