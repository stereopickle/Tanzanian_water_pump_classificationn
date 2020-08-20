# Tanzanian_water_pump_classificationn
by Eunjoo Byeon and Dolci Sanders

Introduction

For our project, we decided to enter a competition to predict the functionality of wells in Tanzania. Only 57% of people in Tanzania have access to water. Since the government launched an initiative to create water accessibility in 2006, the project has been riddled with obstacles. Even after World Bank stepped in with $1.42 billion in funding in 2007, the theorecal plans have not fared well in the real world. 

Tanzania has often been thought of as a developing country, but it has major potential for aggricultural growth, such as coffee and avocados, that would lead to economic growth in the country where there is an absence of a middle class and wide spread poverty. But agriculture depends on year round water supplies. Water accessibility is critical to the growth of not only the country, but also civil rights by extension. The gathering of water generally falls on the women in the communities and by extension their children, particuarly the girls. These families travel kilometers away for each bucket of water often pulling their girls out of school to help transport this essential resource. 

While Tanzania now has many water points, 60,400 to be exact, the battle is far from over as 22,824 are non functional and another 4,317 are partially functional and in need of repairs. By being able to predict which wells need repair, this would significantly cut down on resources being spent on waterpoint checks where they are less needed and concentrate the focus to the problem areas giving way to quicker improvements and by extension additional availability of this critical resource. 



File Structure

010_Cleaning.ipynb - Quickly cleans data and fills in null values. 
020_EDA.ipynb - Assesses, compares, selects features relevant to the data with visualizations. 					Engineers new features relating to location. 
030_Model_Evaluation - Outlines models evaluatated using balanced accuracy and F1 weighted. 
						The model seems to its best with the balanced accuracy, though we did
						use the F1 weighted as we are not as concerned about false positives or negatives. 

PNG - images saved from EDA 
PKL - pickled cleaning data and models


Data Cleaning

We started with 59400 observations. We cleaned the data by checking duplicates, Nan, and Null  values. The ways they were filled depended on each individual feature, what we knew about the feature, and sometimes the frequency of the input. 
Due to the input being extremely messy for both installers and funcers we untilized vectorization to fix these typo issues before condensing the feature into those with frequencies of over 100 and others. 
35% of the construction years and GPS height were missing values, but because they are important factors, kept the features with input of 0 for unknown years. 

Exploratory Data Analysis

After cleaning up the missing values and typos, we proceeded to a closer analysis of the features as with 40 original columns, we needed to make sure there weren't features that were too similar. For many colums like waterpoint_type, waterpoint_type_group, and waterpoint_type_class the features were almost exact with some additional breakdowns included. After looking at heatmaps between them, we were better able to decide which features were most informative for the prediction.

The location data provided led us to engineer features that included distances to basins and local government authorities. We also paired down some location data such as wards and subvillages to try to filter out some noise. 

While looking though the data we were able to use visualizations to help support and guide our findings. 

Model Evaluation 

-Logistic Regression
-KNN
-Decision Trees
-Random Forest
-Optuna
-GXBoost
-Voting Classifier

Limiting Features

The features of most importance to our study are. 

Conclusion
When we use these features to predict we were able to get up to a balanced accuracy score of: 










