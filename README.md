# 506-Final-Project (Final Report Added)

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

Final Report:

To reproduce these results, clone the repository, install the required dependencies, and use the Makefile to run key scripts. From the root directory, run make install to install all Python packages listed in the requirements.txt. Next, you can run make StrAccVSSLpMCluster.py to see the modeling of KMeans clusters based on striking accuracy and volume, make StrAccVSTdAvgCluster.py for clustering modeling based on takedowns and striking accuracy, or make predictForest.py to train and evaluate a random forest classifier for predicting fight winners. test_predict.py can be executed using make test, and a GitHub Actions workflow (.github/workflows/test.yml) is provided.

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

I generated elbow plots and silhouette score plots to determine the optimal number for k. The elbow plot showed a noticeable bend at k = 4, where the marginal improvement in inertia began to level off. Additionally, silhouette scores peaked around k = 3, indicating that fighters were relatively well-separated and compact within their assigned clusters at that value. I chose to use k = 4 for the clustering since I had tried 3 before and wanted to determine if 4 yielded better results. I created interactive clustering visuals for both Striking Accuracy vs Significant Strikes Landed per Minute and Striking Accuracy vs Average Takedowns. 

The StrAcc vs SSLpM graph showed that:
Cluster 0 fighters were moderate in accuracy and high in SSLpM -> likely high volume, relatively efficient strikers.
Cluster 1 fighters were low in both features -> likely lesser skilled or newer fighters
Cluster 2 fighters had moderate SSLpM and low accuracy -> likely less efficient strikers
Cluster 3 fighters had low SSLpM but high accuracy -> likely grapplers who strike when necessary

The StrAcc vs TdAvg graph showed that:
Cluster 0 fighters had high accuracy but low takedown averages -> likely pure strikers
Cluster 1 fighters were varied in accuracy but high in takedown averages -> likely grapplers of varying striking ability
Cluster 2 fighters had moderate to high accuracy and moderate takedown averages -> likely well balanced fighters
Cluster 3 fighters were low in both features -> likely lesser skilled or newer fighters. 

I also modeled Striking Accuracy vs Takedown Average using DBSCAN, which found a small cluster of fighters with higher than average takedown averages and moderate striking accuracies. This may indicate a type of fighter who is primarily a grappler but is also a precise striker. The vast majority of fighters fell into a cluster characterized by low takedown averages and all levels of striking accuracy. Finally, there were many outliers that would not have fit into their own cluster. Unfortunately, DBSCAN did not provide any meaningful insight. 

Next, I modeled Striking Accuracy vs Takedown Average using GMM with 4 clusters:
Cluster 0 fighters had varied accuracy and low takedown averages -> likely strikers of varying ability
Cluster 1 fighters had varied accuracy and high takedown averages -> likely grapplers
Cluster 2 fighters had varied accuracy and moderate takedown averages -> likely well-rounded fighters
Cluster 3 fighters had varied accuracy and low takedown averages -> likely strikers of varying ability

After that, I modeled Striking Accuracy vs Significant Strikes Landed per Minute using GMM with 4 clusters:
Cluster 0 fighters had moderate to high accuracy and high SSLpM -> likely very skilled strikers
Cluster 1 fighters had low accuracy and SSLpM -> likely lesser skilled or newer fighters
Cluster 2 fighters had moderate accuracy and SSLpM -> likely well rounded fighters
Cluster 3 fighters had high accuracy and low SSLpM -> likely cautious strikers

I then trained supervised models to predict whether a fighter would win a given match. I started by using a fighter's cluster from StrAcc vs TdAvg as the sole feature with Random Forest and found that it overfitted and predicted Fighter 1 winning 100% of the time. I then changed class weight to balanced and achieved a 58% accuracy. It predicted wins with 62% accuracy and losses with 54% accuracy. I then tried using Logistic Regression with class weight = balanced and only achieved a 55% accuracy. It predicted wins with 58% accuracy and losses with 51% accuracy. Next, I tried using Logistic Regression but with the features being the difference between the two fighters': Significant Strikes Landed per Minute, Striking Accuracy, Takedown Average, Striking Defence, and Takedown Defence. This method yieled and improved accuracy of 61%. It predicted a win with 75% accuracy and a loss with 46% accuracy. I believe that the bias for win predictions stems from the dataset being unbalanced, with Fighter 1 winning more often than Fighter 2. 

Tests were added to validate that the model runs correctly and reaches a reasonable accuracy threshold. A GitHub Actions workflow was implemented to run test_predict.py, ensuring that future commits do not break the training pipeline. The entire project is reproducible with the provided Makefile, requirements.txt, and test automation.
