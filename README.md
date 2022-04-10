# `#startingDataEngineeringFromScratch`

# Project Topic: Webscrape Companies Information Listed on Y-combinator and Perform analysis
<br>
</br>

# Project Objective - (Last updated: March, 2022)
The goal of the project is to demonstrate an end-to-end data engineering skill by performing ETL task and analysis on y-combinator listed company (https://ycombinator.com/companies).

</br>

# Information to scrape
The image below indicates the information to be scraped for analysis.
1. `company_name` (company's summary and tags)
1. `short_description` (company's summary and tags)
1. `tags` (company's summary and tags)
1. `link` (company's link)
1. `company_socials` (company's info)
1. `founded` (company's info)
1. `team_size` (company's info)
1. `location` (company's info)
1. `active_founders` (Founder's decription)
1. `about_founder` (Founder's info)
1. `description` (Company's description)

</br>


<img width="1353" alt="Screenshot 2022-04-03 at 7 29 58 PM" src="https://user-images.githubusercontent.com/55639062/162624402-ed21f6f2-ab55-46e4-aa4a-58b91b093ed6.png">

</br>


### Important Notice
If the code breaks, the closest fix is to verify if the HTML tag in the code is still valid. If not, change the HTML tags.

</br>

# Output data sample

| company_name  | link  | short_description | tags | company_socials | founded | team_size | location | active_founders | about_founders | description 
| ------------- | ----- | ----------------- | ---- | --------------- | ------- |---------- | -------- |---------------- | -------------- | ---------- |
| Airbnb | http://airbnb.com | Book accommodations around the world. | "['W09', 'Public', 'Marketplace', 'Travel']" | "['https://www.linkedin.com/company/airbnb/', 'https://twitter.com/Airbnb', 'https://www.facebook.com/airbnb/', 'https://www.crunchbase.com/organization/airbnb']" | 2008 | 5000 | San Francisco | "['Nathan Blecharczyk', 'Brian Chesky', 'Joe Gebbia']" | "[{'name': 'Joe Gebbia, CPO', 'role': 'CPO', 'social_media_links': ['https://twitter.com/jgebbia']}, {'name': 'Joe Gebbia, CPO', 'role': 'CPO', 'social_media_links': ['https://twitter.com/jgebbia']}, {'name': 'Joe Gebbia, CPO', 'role': 'CPO', 'social_media_links': ['https://twitter.com/jgebbia']}]" | "Founded in August of 2008 and based in San Francisco, California, Airbnb is a .."  \n

</br>

# Tools
- Selenium - (handled dynamic scraping)
- BeautifulSoup - (for static scraping)
- Pandas - (for data cleaning)
- Matplotlib
- Seaborn
- GitLab
- S3