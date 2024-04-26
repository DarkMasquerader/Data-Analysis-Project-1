# Is the Loot-Box Business Model the Solemn Future of the Gaming Industry?

## Introduction 
- Since early 10's, likely due to iPod and advancement of smart phones, seen an increasing number of f2p games with in-game purchases
- High Profile examples 
    - Candy Crush 
    - Clash of Clans
- Despise apparent negative public sentiment of such models
    - Predatory behaviour
    - Seen as 'cash grabs'
- They are still present and seeming to be more widely adopted
- These two statement appear to be in direct contrast, but what is the truth?
- Are games built on the F2P model more successful than those built on the traditional paid model?

### Defining `successful'
- Ofc, need to define `success`
    - Naturally, subjective nature, many definitions 
- Explore as many possible definitions as datasets allow, examples including:
    - Total sales 
    - Average player count
    - Survive 5 years with more than x initial playerbase
        - 1/2
        - 3/4

### Challenges 
The main challenges encountered throughout this project's lifetime are:
- Data acquisition
    - Information of sales, popularity desireable for this research 
    - Info that companies keep secret from competitors and future clients to give them the edge
- x
- x

### Notable Techniques
-

### Document Structure 
The structure of this document is as followed:
- <title>:<summary>

## Data Acquisition 

### Data Landscape
- First step is acquiring data on games in an automated manner and relevant details where possible 
- Naturally consider following domains:
    - PC (Steam)
    - Console (Sony, Nintendo, Xbox)
    - Mobile (Android, iOS)

- Primary focus is Steam, due to the level of granularity and historical data available from steamcharts, a user-managed site, providing data such as ... over a long duration

- Sony considered
    - Ability to sort by downloads and current popularity 
    - Less granular details 
    - Inclusion depend on findings from primary dataset

- Remaining platforms do not provide a means of obtaining the data needed, as they are likely kept as 'business secrets'

- Working with very limited, and biased dataset, as different platforms are known to have differnt habbits and cultures
    - Successful game genres 
    - Likelihood to pay for game or pay full price for games

### Approach 
- Python primary tool used for data acquisition 
- Scraping:
    - https://steamcharts.com/top
    - https://store.steampowered.com/
    
- Steam charts used to get information on player count; take as indication of popularity for this project 
- Official steam site is used to pricing information 
- Due to unpredictable nature of steam URL's, to automate this process, use `Selenium` package to automate web browsers 
    - Interact with search box so we can search for game as if normal user 

- Diagram of steps
- Link to source code 

##








========


## Visualisations 
- How many paid games include DLC
    - Maybe further break down the DLC
- Are certain models more successful on different platforms
- For those paid games in the top 10, is 'loyalty' a factor?
    - I.e., are only old paid games in the top 10?
- Average amount spent in game 
- Are top 100 currently played games biased towards multiplayer games with inherent replay value?

## Quesrtions
- Were any of the decreases in player count to do with DLC/lootboxes