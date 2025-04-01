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

Midterm Report:

https://youtu.be/CZqmuTy_K7g

Scrapped data from http://www.ufcstats.com/statistics/fighters and http://ufcstats.com/statistics/events/completed?page=all using scrapy.
Generated the starting URLs and then parsed through the listing pages and the individual fighter pages.
Retrieved performance metrics such as strikes landed per minute (SLpM), significant strike accuracy (StrAcc), strikes absorbed per minute (SApM), striking defense (StrDef), takedown average (TDAvg), takedown accuracy (TDAcc), takedown defense (TDDef), and submission average (SubAvg) using XPath expressions.

Used K means clustering to visualize Significant Striking Accuracy vs Significant Strikes Landed per 15 minutes. 
Cluster Centers:
      StrAcc      SLpM
0  48.892060  5.352940
1  32.128607  1.914946
2  50.179945  2.635804
Cluster 0 fighters threw more punches and landed at an above average accuracy.
Cluster 1 fighters threw less punches and were landing at a below average accuracy.
Cluster 2 fighters threw a moderate amount of punches and landed at a similar accuracy to fighters from Cluster 0.

Used K means clustering to visualize Significant Striking Accuracy vs Average Takedowns per 15 Minutes.
Cluster Centers:
      StrAcc     TDAvg
0  52.214689  7.113277
1  36.322785  1.670497
2  51.117207  1.738645
Cluster 0 fighters attempted above average takedowns and also had above 50% significant striking accuracy.
Cluster 1 fighters attempted average takedowns and had a 36% significant striking accuracy.
Cluster 2 fighters attempted similar takedowns to cluster 1 fighters and had around 50% significant striking accuracy.

Used Seaborn to create a scatterplot of fighter 1's significant striking accuracy vs fighter 2's significant striking accuracy in a match.
The spread of points covered the entire range of significant striking percentages.
The points form a cloud and the distribution points spread widely on both axis.
No strong correlation found yet. 
