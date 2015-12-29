This is the simplest scraper for the Food and Exercise diary offered by MyFitnessPal.com I could make. I'm throwing it up here so that others can use it to grab their stats from MFP if they'd like. 

requires scrapy: 

pip install scrapy

usage:

cd mfp_food_and_excercise

scrapy crawl -a username=[your username] -a password=[your password] -a target_date=[date in YYYY-MM-DD format] --nolog mfp

This will create two files in the current directory:

YYYY-MM-DD-excercise.dsv

YYYY-MM-DD-food.dsv



Columns in these tables are delimited with '|'s

This source is released to the Public Domain, do with it as you will (but please be nice to MFP in terms of rates). 
