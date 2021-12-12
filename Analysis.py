
""" 
Suggested method 
Come up with different Headers; Clothes, Food, Car_parts, Technology
Take each heading and decide what group each column belongs to, add them to that particular list for clusterization

Actual method
R (Recency): Number of days since last purchase
F (Frequency): Number of tracsactions
M (Monetary): Total amount of transactions (revenue contributed)

RFM is a method used for analyzing customer value. It is commonly used in database marketing 
and direct marketing and has received particular attention in retail and professional services industries.

 Customers are assigned a 1-5 value for Recency based on their last order date, Frequency based on how many orders they
 have placed, and Monetary based on how much they have spent on your site in total, and then this combined score (Recency * Frequency * Monetary) 
 is used to generate an overall RFM score of 1 - 125 for each customer.

important Variables:
	df = dataframe


"""





# import required libraries for clustering
import sklearn
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from scipy.cluster.hierarchy import linkage
from scipy.cluster.hierarchy import dendrogram
from scipy.cluster.hierarchy import cut_tree



import pandas as pd

from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt


class Analyze:
	def __init__(self,df,col1,col2,col3):# col1, col2 and col3 are enumbers of the columns we want to analyze
		super(Analyze,self).__init__()
		self.df = df.fillna(0)# fillna fills all empty spaces with nan #pd.read_excel(filename, header=None,sheet_name = "Sheet1",dtype=None) # can also index sheet by name or fetch all sheets

		self.customer_col = self.df.columns[(int(col1)-1)]# returns name each selected column
		self.purchase_date_col = self.df.columns[(int(col2)-1)]
		self.revenue_col = self.df.columns[(int(col3)-1)]

		#print(self.df[:8])

		self.rfm_df = self.RFM_dataframe() # runs function on the three columns

		#print(self.rfm_df[:8])

		for col in ['Frequency', 'Recency', 'logRevenue']:
			#print(col)
			self.SSE_plot(self.rfm_df, col)
		#print(self.RFM_dataframe())
		


	def RFM_dataframe(self):
    # Select only unique customer IDs
		self.cust_df = self.df.groupby(self.customer_col)
		self.cust_df = pd.DataFrame(self.df[self.customer_col].unique(), columns=[self.customer_col])
		self.cust_df[self.customer_col].astype(str)
    
    # Create Dataframe of unique visitors and most recent visit to site
		self.df_recency = self.df.groupby(self.customer_col)[self.purchase_date_col].max().reset_index()
		self.df_recency.columns = [self.customer_col,self.purchase_date_col]
		self.df_recency[self.purchase_date_col] = pd.to_datetime(self.df_recency[self.purchase_date_col], errors='coerce')
		self.df_recency['Recency'] = (self.df_recency[self.purchase_date_col].max() - self.df_recency[self.purchase_date_col]).dt.days
		self.df_recency = self.df_recency.drop(self.purchase_date_col, axis=1)

		self.df_recency.fillna(0)
		self.df_recency['Recency'].astype('Int64')
    
    # Get visit counts for each user and create dataframe
    # Frequency is determined by repeat purchases: Order count - 1
		df_frequency = self.df.groupby(self.customer_col)[self.purchase_date_col].count().reset_index()
   	 
		df_frequency.columns = [self.customer_col,'Frequency']

		df_frequency['Frequency'] = df_frequency['Frequency'] - 1
    
    # Get total order revenue for each unique visitor


		self.df[self.revenue_col] = self.df[self.revenue_col].astype('float')

		df_revenue = self.df.groupby(self.customer_col)[self.revenue_col].mean().reset_index()

		

		df_revenue.columns = [self.customer_col, 'logRevenue']

    
    # Merge data
    
		dfs = [df_frequency, self.df_recency, df_revenue]

		for e in dfs:
			self.cust_df = pd.merge(self.cust_df, e, on = self.customer_col)
	    
		return self.cust_df

	def SSE_plot(self,rfm_df,col_to_plot=False):
		"""
		This function takes in one column of
		the RFM dataframe as a string
		and will plot a KMeans elbow plot of the 
		sum of squared estimate. Where the elbow
		bends will determine how many clusters are
		optimal for the Kmeans clustering.
		"""
		sse={}
		if col_to_plot:
			km_var = rfm_df[[col_to_plot]].copy()
		else:
			km_var = rfm_df.copy()
		for k in range(1, 10):
			kmeans = KMeans(n_clusters=k, max_iter=1000).fit(km_var)
			km_var["clusters"] = kmeans.labels_
			sse[k] = kmeans.inertia_ 
		plt.figure()
		plt.plot(list(sse.keys()), list(sse.values()))
		plt.xlabel("Number of cluster")
		plt.title(str(col_to_plot))
		plt.show();
		plt.savefig("C:/Users/User/Documents/DIPLOMNAYA_PYQT/temp/" + col_to_plot + ".png")


	def ret(self):
		return self.cust_df;


