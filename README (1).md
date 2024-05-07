# An Analysis: What Type of Game Has the Highest Chance of Success in 2024?
<!-- 
Badges: https://shields.io/
GitHub: https://github.com/semasuka/credit-card-approval-prediction-classification?tab=readme-ov-file
-->
## Authors 

## Table of Contents 
- [Business Problem](#business-problem)
- [Data Preparation and Acquisition](#data-preparation-and-acquisition)
- [Notable Techniques](#notable-techniques) 
- [Tech Stack](#tech-stack)
- [Results at a Glance](#results-at-a-glance)
- [Insights & Recommendations](#insights-and-recommendations)
- [Limitations and Potential Improvements](#limitations-and-potential-improvements)
- How to run

## Business Problem 
A game development studio is looking to develop a new game for the PC platform.
The studio would like to know what type of games are most successful, providing the studio highest chance of developing a successful game.

This work answers this question by generating a novel, large-scale dataset concerning the games available on the Steam platform. 
This program and dataset is made available to the public for further use.

## Data Preparation and Acquisition
The dataset used for this project is generated using data from Steam[] and SteamCharts[], using *web scraping* and *website automation*, alongside advanced programming techniques such as multi-threading and resource management (mutexes).

The collected data is also cleaned and transformed in preparation for subsequent data analysis.

The script responsible for data acquisition and preparation is `Data Acquisition.py`.

## Notable Techniques  
**NOTE:** Technical techniques are appended with an asterisk 
- Bivariate data analsys 
- Regression 

- Website scraping *
- Website automation (aka. botting) *
- Multi-threading and resource management *

## Tech Stack 
- Python (Data acquisition and processing)
- MySQL 

## Results at a Glance
<!-- 
For each definition of success
    - f2p vs paid 
    - multi-player vs single-player
    - Genres 

Success definitions 
    - Current player count
    - Max player count
    - (Retaining) 
        - Lasting x years with more than x% of initial population 
 -->

## Insights and Recommendations
- Based on the analysis of this project, we found that...
- Recommendation is to...

## Limitations and Potential Improvements
- Lack of information on:
    - revenue
    - purchase numbers
    - Lead to using metrics biased towards multi-player games
- Collection of data across other gaming platforms (mobile, console etc.)
- Does not take note if game was on discount
- Scraper not identify price of game on steam page, occasionally (slightly inaccurate)

## How to Run

### Explore the Notebook