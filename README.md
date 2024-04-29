# Is the Loot-Box Business Model the Solemn Future of the Gaming Industry?
This exploration contributes to the generation of a large and easily parse-able dataset comprising <> games with a generation time of <> hours.

Data acquired for this project is acquired first-party, primarily through techniques such as *automated web scraping* and *automated website interaction* using advanced programming techniques such as multi-threading and mutexes.

<!-- I have made this data available in the files <> and <>.

This project comprises the usual data analysis steps of data preparation (acquisition), data processing (cleaning), data analysis, and lastly, data sharing.
These steps are used to guide the structure of the presentation of my findings. -->


## A Brief Introduction 
Since the early 2010's, and likely due to the invention of the iPod and the advancement of smartphones and the internet, there has been a consistent and significant increase in the number of 'free-to-play' games which generate revenue through advertisements and/or in-game purchases.
Some high-profile examples of these games are Candy Crush and Clash of Clans.

This then-new model of gaming (or service, as this model goes beyond the realm of games) is very different from what was the standard where games purchased on consoles on pc games were 'complete'; users got the full experience of the game with their initial purchase.
(Though, I do believe that if the internet were sufficiently advanced back then, such a business model would have been present then, too!)

### My Motivation
The motivation for this project is that despite the apparent mainstream negative public sentiment towards such business model for their predatory behaviour (and often being referred to as `cash grabs'), they are still present and appear to be flourishing.

These two statements are in direct contrast to one another, but what is the truth? Are games that use this free-to-play model (more commonly known as F2P) more successful than those built on the paid model? 

Let's find out!

[!NOTE]
I will also be including some technical information in this post, but feel free to skip over it you're not interested!

### How *do* we define `successful'?
So, when looking into which gaming model is more successful, we need some criteria for `success'. 
Naturally, with the subjective nature of this word, there are many definitions.
In this project, I explore as many possible definitions as the datasets will allow.
Some example definitions are: total sales, average number of players, and lasting x years with more than x% of the initial playerbase.

More on this later on!

## Project Challenges  
During my time on this project, I encountered a number of challenges, primarily in the data acquisition phase.
- Data acquisition
    - Information of sales, popularity desireable for this research 
    - Info that companies keep secret from competitors and future clients to give them the edge
    - Existing games on one list but not steam
- x
- x

## Tools Used 
My weapons of choice for this project are Python (data acquisition and cleaning), SQL, and R.

## Data Acquisition 

### Data Landscape
- First step is acquiring data on games in an automated manner and relevant details where possible 
- Naturally consider following domains:
    - PC (Steam)
    - Console (Sony, Nintendo, Xbox)
    - Mobile (Android, iOS)

- Unfortunately, modbile and console privates are very conservative with informtion they make available, includitng historical 
    - Unfortunate as i believe mobile is ideal platofrm for this research

- Primary focus is Steam, due to the level of granularity and historical data available from steamcharts, a user-managed site, providing data such as ... over a long duration

- Working with a limited, and biased dataset, as different platforms are known to have differnt habbits and cultures
    - Successful game genres 
    - Likelihood to pay for game or pay full price for games

### Approach 
- Python primary tool used for data acquisition 
- Scraping:
    - https://steamcharts.com/top
        Simple due to predictable URL and HTML pages; foregoing need of automtion tools and conditional checks
    - https://store.steampowered.com/
        Not the case for steam, discussed more in challenges section
    
- Steam charts used to get information on player count; take as indication of popularity for this project 
- Official steam site is used to pricing information 
- Due to unpredictable nature of steam URL's, to automate this process, use `Selenium` package to automate web browsers 
    - Interact with search box so we can search for game as if normal user 

- Diagram of steps
- Link to source code 

#### Challenge 
- Unexpected surprise is some games requireing extra screen for age restricted games 
- Game pages inconsistent, needing to be handled
    - Discounts 
    - Unique drop-down menus (GTA V)
    - Changed the way identified datafields

## Data Cleaning 
- Months to SQL format, orderable (March 2024 -> 2024-03) and (Last 30 Days -> Current month year)
- Missing prices
- Random games having random tabs in html
- Not having appropriate singe-player tags in 'correct' place 
- Some games will be incorrect with outliers such as Wallpaper Engine







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