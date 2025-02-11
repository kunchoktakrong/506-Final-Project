# 506-Final-Project

Description: 
Utilizes fighter data to determine which fighter will win or if the fighters will draw in a UFC bout.

Goal:
Predict outcomes of UFC fights based on fighter statistics.

Data Collection:
Scrape ufcstats.com for:
- significant strikes landed per minute
- significant striking accuracy
- significant strikes absorbed per minute
- significant strike defence (the % of opponents strikes that did not land)
- average takedowns landed per 15 minutes
- takedown accuracy
- takedown defense (the % of opponents TD attempts that did not land)
- average submissions attempted per 15 minutes

Data Modeling:
Group fighters into clusters based on their statistics and identify patterns among them.
Use decision trees to predict fight outcomes based on learned patterns.

Data Visualization:
Use scatter plots to determine the relationship between different variables
Create heatmaps to identify which factors are most predictive of winning

Test Plan:
Data will be split - 80% training, 20% testing.
