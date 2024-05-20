# Tableau Dashboard
The purpose of this Tableau dashboard is to demonstrate my proficiency with this tool, mimicking the visualisations made in the Jupyter Notebook.

The Tableau Dashboard shown below is accessible in `Project 1.twbx`.
![](images/Tableau%20Dashboard.gif)

## Optimisations

### Data Source Filter
Records for a number of games go as far back as 2012.

However, for this analysis, such historical data is not required and has been removed with a data source filter to improve performance, avoiding the unnecessary processing of unhelpful and unnecessary data.

If such data is later required by the client, the filter can be adjusted.

![](images/Data%20Source%20Filter.png)


### Cardinality and Referential Integrity
Cardinality and Referential Integrity have been set accordingly to help with performance.

**Tables: Details x Stats**\
![](images/Relationship%20-%20Details%20x%20Stats.png)

**Tables: Details x Tags**\
![](images/Relationship%20-%20Details%20x%20Tags.png)
