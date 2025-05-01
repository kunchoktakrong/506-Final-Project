test:
	PYTHONPATH=. pytest my_scraper/analysis/test_predict.py

# CLUSTERING

cluster-stracc-slpm:
	python3 my_scraper/analysis/StrAccVSSLpMCluster.py

cluster-stracc-tdavg:
	python3 my_scraper/analysis/StrAccVSTdAvgCluster.py

cluster-dbscan:
	python3 my_scraper/analysis/StrAccVSTdAvgDB.py

cluster-gmm-slpm:
	python3 my_scraper/analysis/StrAccVSSLpMGaussian.py

cluster-gmm-tdavg:
	python3 my_scraper/analysis/StrAccVSTdAvgGaussian.py

scatter-stracc:
	python3 my_scraper/analysis/StrAccScatter.py

# PREDICTION

predict-forest:
	python3 my_scraper/analysis/predictForest.py

predict-logreg:
	python3 my_scraper/analysis/predictLogReg.py

predict-cluster-forest:
	python3 my_scraper/analysis/ClusterPredictionForest.py

predict-cluster-logreg:
	python3 my_scraper/analysis/ClusterPredictionLogReg.py

# CLUSTER DIAGNOSTICS & ANALYSIS

compare-clusters:
	python3 my_scraper/analysis/ClusterComparison.py

cluster-diagnostics:
	python3 my_scraper/analysis/ClusterDiagnostics.py
