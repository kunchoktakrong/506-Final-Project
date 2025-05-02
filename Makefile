# TESTING
test:
	PYTHONPATH=. pytest data_functions/test_predict.py

# CLUSTERING
cluster-stracc-slpm:
	python3 data_functions/StrAccVSSLpMCluster.py

cluster-stracc-tdavg:
	python3 data_functions/StrAccVSTdAvgCluster.py

cluster-dbscan:
	python3 data_functions/StrAccVSTdAvgDB.py

cluster-gmm-slpm:
	python3 data_functions/StrAccVSSLpMGauss.py

cluster-gmm-tdavg:
	python3 data_functions/StrAccVSTdAvgGauss.py

scatter-stracc:
	python3 data_functions/StrAccScatter.py

# PREDICTION
predict-forest:
	python3 data_functions/predictForest.py

predict-logreg:
	python3 data_functions/predictLogReg.py

predict-cluster-forest:
	python3 data_functions/ClusterPredictionForest.py

predict-cluster-logreg:
	python3 data_functions/ClusterPredictionLogReg.py

# CLUSTER ANALYSIS
compare-clusters:
	python3 data_functions/ClusterComparison.py

cluster-diagnostics:
	python3 data_functions/ClusterDiagnostics.py
