# Tableau Dashboard
The purpose of this Tableau dashboard is to demonstrate my proficiency with this tool, mimicking the visualisations made in the Jupyter Notebook.
Tableau will play a larger part in future projects.

The Tableau Dashboard shown below is accessible in `Project 1.twbx`.
![](images/Tableau%20Dashboard.gif)

## Optimisations

### Data Source Filter
Records for a number of games go as far back as 2012.

However, for this analysis, such historical data is not required and has been removed using a data source filter to improve performance.

If such data is later required by the client, the filter can easily be adjusted.

![](images/Data%20Source%20Filter.png)


### Cardinality and Referential Integrity
Cardinality and Referential Integrity have been set accordingly to help with performance.

**Tables: Details x Stats**\
![](images/Relationship%20-%20Details%20x%20Stats.png)

**Tables: Details x Tags**\
![](images/Relationship%20-%20Details%20x%20Tags.png)
