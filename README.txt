Welcome to the New Franchise Locator app. 

The app that uses the power of ML and data processing to suggest locations of new franchise stores using the information of stores around the city. 

As a future franchise owner, you might wonder where to open a new store. Due to the COVID-19 Pandemic, 1 in 7 stores in New York has closed. With things getting better in 2021, now may be a good time to identify potential location for opening a store.

But what does identifying a location for a store usually entail? 
Lots of market research into the demography, logistical aspects, foot traffic, cost etc. The elaborate research needs to be done for multiple location and even then an ideal location may end up costing too high in rent or may end up being sub-prime. 

But what if we can look at the existing distribution of restaurants and franchises in the city and draw from it where these franchises tend to occur. You might have noticed that international stores tend to be close to one another. Or tiny bakeries close to coffee shops. 

A Random Forest Classifier model is used in this work to learn such patterns and then to identify where the pattern occurs, but the store of interest does not. These locations are our potential locations!


GitHub files:

1) The YelpDownloadData.py file is used to extract the data from the Yelp API. Due to the APIs nature, the data is segmented to not exceed the maximum limit. The location information is sent to the API from the hex-centers.csv file. 
2) The DataAnalysis.py file is used to consolidate the data and create a dataframe. H3 location identifier is added, any duplicate entry occuring at multiple grids is removed, top categories are extracted and associated with each entry. 
3) The MLmodel.py file is used to generate the ML model. 
	- The data from the DataAnalysis.py file is pivoted to have the top 100 categories as features and the observations as the grids (hexagons). 
	- After choosing the store of choice (in our case, a bubble tea store), it is set as the y label
	- Depending on the maximum number of stores in a grid, the label can be divided into classes (in the base case, 1,2,3, 4+ are our classes)
	- A oversampler is used in order to balance the dataset to avoid skewing the results
	- The model is developed using the training fraction and evaluated on the testing data. 
	- False positives and their corresponding h3 indices are identified. 
4) The app.py file generates the streamlit file and launches it in heroku. (Currently built to run using the .csv files in the repo.)
	- Multiple pages of the streamlit site are stored in the apps folder along with the data required to run them (including some images)
	- The apps folder contains:
		- home.py, data.py, ML.py, results.py, summary.py that run the respective streamlit pages on the heroku website
	- The results.py file contains the code to generate the h3 grids on the folium map from the results of the ML model


 


