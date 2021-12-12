import unittest
from  Clusterization import Clusterize
from Analysis import Analyze
import pandas as pd
import pandas.testing as pd_testing
from matplotlib.testing.decorators import image_comparison

data = {'Order ID':  ['CA-2016-152156', 'CA-2016-152156','CA-2016-138688','US-2015-108966','US-2015-108966','CA-2014-115812','CA-2014-115812'],
        'Order Date': ['11/8/2016', 	'11/8/2016',	  '11/8/2016','10/11/2015','10/11/2015','6/9/2014','6/9/2014'],
        'Profit': ['261.96', '731.94','14.62','957.5775','22.368','48.86','7.28']
        }

data_df = pd.DataFrame (data, columns = ['Order ID','Order Date','Profit'])

result = {'Order ID':  	['CA-2016-152156','CA-2016-138688','US-2015-108966','CA-2014-115812'],
          'Frequency': 	[1, 0, 1, 1],
          'Recency': 	[0, 0,394, 883],
          'logRevenue': [496.95000, 14.62000, 489.97275, 28.07000]
        }

result_df = pd.DataFrame (result, columns = ['Order ID','Frequency','Recency','logRevenue'])

class TestApp(unittest.TestCase): 

	#Analyze(data_df,1,2,3).RFM_dataframe()

	" when testing comment out the graphing section SSEplot in the analyze class"
	#Analyze assert_frame_equal parameters:
		#parameter 1
			#check_dtypebool, default True
			#Whether to check the DataFrame dtype is identical.
		#parameter 2
			#check_index_typebool or {‘equiv’}, default ‘equiv’
			#Whether to check the Index class, dtype and inferred_type are identical.
		#parameter 3
			#check_column_typebool or {‘equiv’}, default ‘equiv’
			#Whether to check the columns class, dtype and inferred_type are identical. Is passed as the exact argument of assert_index_equal().
			#pd_testing.assert_frame_equal(Analyze(data_df,1,2,3).RFM_dataframe(),result_df,False,False,False,False)
		#parameter 4
			#check_frame_typebool, default True
			#Whether to check the DataFrame class is identical.
		#there are many other parameters but these are the most imortant for asserting the correctness of our data

	def test_Analyze_1(self): # when testing comment out the graphing section SSEplot in the analyze class
		pd_testing.assert_frame_equal(Analyze(data_df,1,2,3).RFM_dataframe(),result_df,False,False,False,False)

	def test_Analyze_2(self): # when testing comment out the graphing section SSEplot in the analyze class
		pd_testing.assert_frame_equal(Analyze(data_df,1,2,3).RFM_dataframe(),result_df,True,False,False,False)

	def test_Analyze_3(self): # when testing comment out the graphing section SSEplot in the analyze class
		pd_testing.assert_frame_equal(Analyze(data_df,1,2,3).RFM_dataframe(),result_df,False,False,True,False)

	def test_Analyze_4(self): # when testing comment out the graphing section SSEplot in the analyze class
		pd_testing.assert_frame_equal(Analyze(data_df,1,2,3).RFM_dataframe(),result_df,False,False,False,True)

if __name__ == '__main__':
    unittest.main().shortDescription()