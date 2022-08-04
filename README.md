# `#startingDataEngineeringFromScratch`

# Project Topic: Webscrape Companies-Information Listed on Y-combinator and Perform analysis
<br>
</br>

# Project Objective - (Last updated: August 2022)
The project aims to demonstrate an end-to-end data engineering skill by performing ETL tasks and analyses on the y-combinator listed companies (https://ycombinator.com/companies). The project's core concept is to help beginners optimize data pipelines.
In the project doc, three different approaches were used
- An approach that made the extraction process run for `3 hours`
- An approach that ran for `12 mins`
- An approach that ran for 	1.06 mins	


# Analysis Result
[click here for full analysis details](EDA.ipynb)

From the analyzed data, here are the insights
- The top 5 countries under y-combinator are 
    - USA
    - India
    - Canada
    - UK
    - Nigeria
- Companies from `USA` take **65.3%** of y-combinator start-up
- `Nigeria` is the only Africa country that has more than 10 start-ups under y-combinator
- Company with a single founder under YC has the highest percentage, **`42.4%`**, while **`38.6%`** and **`13.9%`** are for 2 and 3 founders respecively. The other percentage is shared among 4 and 5 founders.
- `Airbnb` is the largest company under YC in terms of employees
- The total number of people YC has empowered is **`90373`**

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
1. `active_founders` (Founder's description)
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
| Airbnb | http://airbnb.com | Book accommodations around the world. | ['W09', 'Public', 'Marketplace', 'Travel'] | ['https://www.linkedin.com/company/airbnb/', 'https://twitter.com/Airbnb', 'https://www.facebook.com/airbnb/', 'https://www.crunchbase.com/organization/airbnb'] | 2008 | 5000 | San Francisco | ['Nathan Blecharczyk', 'Brian Chesky', 'Joe Gebbia'] | [{'name': 'Joe Gebbia, CPO', 'role': 'CPO', 'social_media_links': ['https://twitter.com/jgebbia']}, {'name': 'Joe Gebbia, CPO', 'role': 'CPO', 'social_media_links': ['https://twitter.com/jgebbia']}, {'name': 'Joe Gebbia, CPO', 'role': 'CPO', 'social_media_links': ['https://twitter.com/jgebbia']}] | Founded in August of 2008 and based in San Francisco, California, Airbnb is a ..  \n

</br>

# Tools
- Selenium - (handled dynamic scraping)
- BeautifulSoup - (for static scraping)
- Pandas - (for data cleaning)
- Matplotlib
- Seaborn
- S3

# Data Analysis
Some charts were created to make sense of the data and communicate the insight from the data. 

### start-up by country
Visualize the country distribution by start-up
![image](https://user-images.githubusercontent.com/55639062/182843337-8e872867-c9e5-442d-ab75-695cb859f68a.png)


### Start-up by year
Distribution of start-up by year
![image](https://user-images.githubusercontent.com/55639062/182843651-d5d9da36-bd2a-466b-af1c-a9bbcb759e7a.png)

### Start-up by founder
![image](https://user-images.githubusercontent.com/55639062/182843935-8cab8514-fb2d-4822-bc81-5f43e92bd56b.png)

### Team size per company
![image](https://user-images.githubusercontent.com/55639062/182844115-0ad55a2b-d3a0-4801-91c5-2af279e8026e.png)


### Total Empowered by Y-Combinator
90373 people