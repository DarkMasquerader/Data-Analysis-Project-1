# A Recipe for Success: An Analysis on the Most Popular Steam Games
<!-- 
Badges: https://shields.io/
GitHub: https://github.com/semasuka/credit-card-approval-prediction-classification?tab=readme-ov-file
-->
## Authors 

## Table of Contents 
- [Business Problem](#business-problem)
- [Data Preparation and Acquisition](#data-preparation-and-acquisition)
- [Tech Stack](#tech-stack)
- [Results at a Glance](#results-at-a-glance)
- [Insights & Recommendations](#insights-and-recommendations)
- [Limitations and Potential Improvements](#limitations-and-potential-improvements)
- How to run

## Project Focus 
This project covers all stages of data analysis process, with the strong points of this project taking place within the *data collection* and *data processing* stages.

Details on these stages can be found in the [Python](Python%20Files/) directory.

## Business Problem 
For this project, I consider a hypothetical game development studio that is looking to develop a new game for the PC platform.
The studio would like to know what type of games are most successful, thus providing the studio highest chance of developing a successful game.

This work answers this question by generating a novel, large-scale dataset (first-hand) concerning the games available on the Steam platform and subsequently conducting and analysis.\
(The data acquisition Python script and dataset are made available to the public for further use.)

## Data Preparation and Acquisition
The dataset used for this project is generated using data from [Steam](https://store.steampowered.com/) and [SteamCharts](https://steamcharts.com/).

The collected data is also cleaned and transformed in preparation for subsequent data analysis.

The script responsible for data acquisition and preparation is `Data Acquisition.py`, which can be found [here](Python%20Files/Data%20Acquisition/), alongside its README file.

## Tech Stack 
- [Python](Python%20Files/)
    - Data Acquisition: Website Scraping, Website Automation, Multi-Threading and Resource Management
    - Data Processing: Data Transformation & Handling
    - Data Visualisation: Numpy, Matplotlib
- [Tableau](Tableau/)
- MySQL `TO DO`

## Results at a Glance
Distribution of top 10 tags (categories) of the top 100 games.
![](images/Top%20Tags.png)

Scatter plot showing the relationship between the price of a game and its rank.
![](images/Price%20x%20Ranking.png)

Line plot showing the distribution of payment models of the top 100 games over two years.
![](images/Pricing%20Distribution%20Over%20Time.png)

## Explore the Notebook
The Jupyter notebook used to facilitate data analysis is provided [here](Python%20Files/Jupyter%20Notebook/).

The notebook has been designed to be as dynamic and interactive as possible, adjusting figures and data structures to accommodate the change in the controllable variables.

## Explore the Dashboard (Tableau) 
A Tableau dashboard has been implemented to demonstrate my proficiency and knowledge of this tool.\
For further details and to view the dashboard, go to the [Tableau](Tableau/) directory.

## Insights and Recommendations
Based on the findings of this brief analysis, the recommendation of the type of game for the game studio to create to have the highest chance of being successful (determined by active player count) is an action-based multiplayer game.

Regarding the payment model and pricing, a lower price is suggested due to the negative correlation between price and game popularity.

## Challenges and Limitations

### Data Availability & Bias
A significant challenge faced by this project is the availability of data.

Key information that would enable an accurate, in-depth exploration into this research question (e.g. revenue, purchase numbers, and in-game purchase information) is not publicly available, with such information likely being kept as business secrets of the game studios and platforms.

As a result, this lead to using a criterion for determining success that is biased in favour of multiplayer games: player count (average and current).

This approach to determining the success of a game is biased in favour of multiplayer games is due to such games being designed to retain a consistent player base, and their inability to be 'completed'.
Singleplayer games, on the other hand, typically have a clear end goal with the ability to be 'completed', at which point the game stops being played.

### Data Collection Challenges
The main nature of the challenges faced during data collection is 'unexpected variations' in the pages of the games on Steam.

Though not difficult to address, this greatly increased the development time and complexity of the script.

## How to Run
Details on how the run the included Python and Tableau files are provided in the appropriate directories.
