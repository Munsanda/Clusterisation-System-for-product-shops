# import required libraries for dataframe and visualization

import numpy as np
import pandas as pd

from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt


import datetime as dt


# import required libraries for clustering
import sklearn
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from scipy.cluster.hierarchy import linkage
from scipy.cluster.hierarchy import dendrogram
from scipy.cluster.hierarchy import cut_tree
"""
Recency refers to the interval between the time, that the latest consuming behavior happens,
and present. Many direct marketers believe that most-recent purchasers are more likely to
purchase again than less-recent purchasers. Frequency is the number of transactions that a
customer has made within a certain period. This measure is used based on the assumption
that customers with more purchases are more likely to buy products than customers with
fewer purchases. Monetary refers to the cumulative total of money spent by a particular
customer.  

Unlike supervised learning, clustering is considered an unsupervised learning method since we
 don’t have the ground truth to compare the output of the clustering algorithm to the true labels 
 to evaluate its performance. We only want to try to investigate the structure of the data by 
 grouping the data points into distinct subgroups.
"""


class Clusterize: 
# Reading the data on which analysis needs to be done
	def __init__(self,freq_k, recen_k, rev_k, rfm_df ):

		self.rfm_df = rfm_df

		self.rfm_df = self.frequency_cluster(freq_k, 'Frequency', self.rfm_df)

		self.rfm_df.groupby('FrequencyCluster')['Frequency']

		self.rfm_df = self.recency_cluster(recen_k, 'Recency', self.rfm_df)
		self.rfm_df.groupby('RecencyCluster')['Recency']

		self.rfm_df = self.revenue_cluster(rev_k, 'logRevenue', self.rfm_df)
		self.rfm_df.groupby('RevenueCluster')['logRevenue']

		self.rfm_df['OverallScore'] = self.rfm_df['RecencyCluster'] + self.rfm_df['FrequencyCluster'] + self.rfm_df['RevenueCluster']
		self.rfm_df.groupby('OverallScore')['Recency','Frequency','logRevenue'].mean()

		self.rfm_df.to_excel("C:/Users/User/Documents/DIPLOMNAYA_PYQT/temp/clusters.xlsx")

		self.graphClusters()
		#self.graphIndividaulMeasures()



	def order_cluster(self,cluster_col, feature_col, df, ascending):
		df_new = df.groupby(cluster_col)[feature_col].mean().reset_index()
		df_new = df_new.sort_values(by=feature_col,ascending=ascending).reset_index(drop=True)
		df_new['index'] = df_new.index
		df_final = pd.merge(df,df_new[[cluster_col,'index']], on=cluster_col)
		df_final = df_final.drop([cluster_col],axis=1)
		df_final = df_final.rename(columns={"index":cluster_col})

		return df_final
  
	def frequency_cluster(self, cluster_number, frequency_col, dataframe):
		frequency_kmeans = KMeans(n_clusters=cluster_number)
		frequency_kmeans.fit(dataframe[[frequency_col]])
    
    	# Assigning cluster prediction to customers
		dataframe['FrequencyCluster'] = frequency_kmeans.predict(dataframe[[frequency_col]])
    
    	# Ordering clusters from low to high and identifying statistics
		dataframe = self.order_cluster('FrequencyCluster', frequency_col, dataframe, True)
    
		return dataframe

	def recency_cluster(self, cluster_number, recency_col, dataframe):
		recency_kmeans = KMeans(n_clusters=cluster_number)
		recency_kmeans.fit(dataframe[[recency_col]])
    
    	# Assigning cluster prediction to customers
		dataframe['RecencyCluster'] = recency_kmeans.predict(dataframe[[recency_col]])
    
    	# Ordering clusters from low to high and identifying statistics
		dataframe = self.order_cluster('RecencyCluster', recency_col, dataframe, False)
    
		return dataframe

	def revenue_cluster(self, cluster_number, revenue_col, dataframe):    
		revenue_kmeans = KMeans(n_clusters=cluster_number)
		revenue_kmeans.fit(dataframe[[revenue_col]])
    
    	# Assigning cluster prediction to customers
		dataframe['RevenueCluster'] = revenue_kmeans.predict(dataframe[[revenue_col]])
    
    	# Ordering clusters from low to high and identifying statistics
		dataframe = self.order_cluster('RevenueCluster', revenue_col,dataframe,True)
    
		return dataframe


	def graphClusters(self):
		#print("************************************")
		#print(self.rfm_df)
		#print("************************************")	

		# Naming and defining segments
		self.rfm_df['Segment'] = 0
		self.rfm_df.loc[self.rfm_df['OverallScore']>2,'Segment'] = 1 
		self.rfm_df.loc[self.rfm_df['OverallScore']>4,'Segment'] = 2
		self.rfm_df.loc[self.rfm_df['OverallScore']>6,'Segment'] = 3
		self.rfm_df.loc[self.rfm_df['OverallScore']>8,'Segment'] = 4

		high = self.rfm_df.query('Segment == 4')
		mid_high = self.rfm_df.query('Segment == 3')
		mid = self.rfm_df.query('Segment == 2')
		mid_low = self.rfm_df.query('Segment == 1')
		low = self.rfm_df.query('Segment == 0')

		fig = plt.figure()
		ax = fig.add_subplot(111, projection='3d')

		g0= (low['Frequency'].values, low['Recency'].values, low['logRevenue'].values)
		g1 = (mid_low['Frequency'].values, mid_low['Recency'].values, mid_low['logRevenue'].values)
		g2= (mid['Frequency'].values, mid['Recency'].values, mid['logRevenue'].values)
		g3= (mid_high['Frequency'].values, mid_high['Recency'].values, mid_high['logRevenue'].values)
		g4= (high['Frequency'].values, high['Recency'].values, high['logRevenue'].values)

		data = [g0,g1, g2, g3,g4]
		colors = ['#440154FF', '#20A387FF', '#FDE725FF','#080808','#c21f3d']
		groups = ['Low','Mid_low', 'Med','Mid_high', 'High']

		for data, color, group in zip(data, colors, groups):
			x, y, z = data
			ax.scatter(x, y, z, alpha=0.5, c=color, label=group)

		# Make legend
		ax.legend()
		ax.set_xlabel('Frequency')
		ax.set_ylabel('Recency')
		ax.set_zlabel('Revenue')
		ax.set_title('Spatial Representation of Segments', loc='left')
		plt.show();
		plt.savefig("C:/Users/User/Documents/DIPLOMNAYA_PYQT/temp/" + "Cluster" + ".png")


