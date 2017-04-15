## MARTA Parking page scraper

Scrapes: http://www.itsmarta.com/parking.aspx

To set up locally:

`$ npm init`

Then to run:

`$ node parking.js`

Project Goal: Create an AWS Lambda function that scrapes the page once per minute (via AWS Cloudwatch) and publishes to a static JSON file hosted on S3.

Next step: Publish that JSON object to S3.
