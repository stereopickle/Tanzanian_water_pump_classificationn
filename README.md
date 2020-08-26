# Tanzanian Water Points Prediction
by Eunjoo Byeon and Dolci Sanders

### Multi-Class Prediction of Water Points Functionality 

This repository contains a process for running multi-class prediction on the water points condition in Tanzania. Our goal of this project is to predict the functionality of water points around the country in order to improve maintenance operations and increase the accessibility of clean water in Tanzania. 

## Data
Data is from the Taarifa and Tanzanian Ministry of Water data provided as part of a DrivenData.Org competition.

## The Problem

Only 57% of people in Tanzania have access to safe water. Since the government launched an initiative to create water accessibility in 2006, the project has been riddled with obstacles (water.org). Even after World Bank stepped in with $1.42 billion in funding in 2007, the theorecal plans have not fared well in the real world (Chloe Farand for the Independent). 

Tanzania National website states that water-borne illesses like cholera and malaria account for over half of the disease in the country.  

Tanzania has often been thought of as a developing country, but it has major potential for aggricultural growth, such as coffee and avocados, that would lead to economic growth in the country where there is an absence of a middle class and wide spread poverty. But agriculture depends on year round water supplies. Water accessibility is critical to the growth of not only the country, but also civil rights by extension. The gathering of water generally falls on the women in the communities and by extension their children, particuarly the girls. These families travel kilometers away for each bucket of water often pulling their girls out of school to help transport this essential resource.  

While Tanzania now has many water points, 60,400 to be exact, the battle is far from over as 22,824 are non functional and another 4,317 are partially functional and in need of repairs (information only based on our current dataset).  


## File Structure

#### 010.Data_Cleaning.ipynb 
- Structural cleaning of data such as dealing with missing values. 

#### 020.Exploratory_Data_Analysis.ipynb 
- Assesses, compares, selects features relevant to the data with visualizations.
- Engineers new features relating to location. 

#### 030.Model_Evaluation_Clean.ipynb  
- Outlines the process of model testing and evaluation

#### 040_Final_Testing.ipynb
- Final model performance on test set

#### 050_A_Data_Story.ipynb
- Additional visualization and context

## Data Cleaning

We started with 59,400 observations. We cleaned the data by checking duplicates and missing values. Missing values were imputed based on what we knew about the feature, and sometimes the frequency of the input. 

Due to the input being extremely messy for both installers and funders, we untilized vectorization to fix these typo issues before condensing the feature into those with frequencies of over 100 and others. 

Large amount of the construction years and GPS height were missing, but because they were important predictors, we implemented categorization to keep these features.


## Exploratory Data Analysis



<img src="./PNG/class_imbalance.png"> 

## Target: Water Point Status Group 

Our target variable is the status of each water points. It consists of three classes (functional, not functional, needs repair) that are heavily imbalanced as seen above.  

## Predictors 
Here we outline a few predictors that were included in our model.  

### Construction Year

Construction year had a significant implication to our data but many were missing. So we created sub-bins and treated this variable as categorical. The initial EDA showed that most of functional water points were built recently. At the same time, there were also significant number of recently built water points that were already not functional.

### Locations

<img src="./PNG/waterpoint_location.png">

This is a map of water points by condition in Tazania. We can see that some clustering of functionality is visible. As location information seemed important, we expanded upon the current features by engineering with distance and location predictors such as distance to the basin and local government area center. 

### Payment 
<img src="./PNG/Payment.png">
Payment type seems to be a direct predictor of the maintenance of these water points as we can expect. Steadier payment plan is, it is likely to be functioning. This brings a question of how funding for Tanzania water project is actually being utilized. 

### Extraction Type
<img src="./PNG/extraction_type.png">
Most pumps utilize gravity pump or old fashioned hand pump. We can see that electric water pumps like motor pump and submersible pump are not well maintained and more likely to fail. The few wind-powered extraction types seemed to be not working as well. 

### Other Predictors included ...
amount_tsh - total static head  
funder - who funded the project  
installer - who installed the project  
quantity - the output level of the waterpoint  
water_quality - quality of water  
payment_type - how payment is made (per bucket, monthly, yearly)  
source - water source  
waterpoint_type - how the water is pumped by then end user  
management - team responsible for the maintanence  
public_meeting - "true/false" was all the explaination given  
permit - if the waterpoint has a permit  
scheme_managemen - operator of the waterpoint  
num_private 


## Model Evaluation

### Evaluation Metrics
Our target is multi-class with imbalance issue where we have a very few observations of water points that needs repair compared to the ones that are functioning. It was important to us to not miss the non functioning or need for repair cases, as it is directly related to the lives of people using that water points. 

So for our model evaluation, we prioritized the **balanced accuracy score**. This computes the average accuracy score weighted by the inverse prevalence of the true classes. We also specifically looked at the **recall of the needs repair** classes to make sure we are not missing when the water point is needing repair.

Additionally weighted F1 score was considered for overall performance.

### Class Imbalance
Our dataset has high class imbalance issue. We mostly solved this by setting the class weight within each model, but in some cases where imbalance weight was not adequately dealt with by algorithm we tested with resampled set using SMOTE.

We tested a number of models including ...
1. Multi-class Logistic Regression with Lasso Regularization  
2. kNearestNeighbors  
3. Simple Decision Tree  
4. Random Forest  
5. XGBoost  
6. Voting Classifier  

Hyperparameter tuning was done using both GridSearchCV and Optuna.  

### Baseline Model
Our stratified dummy predictor yielded balanced accuracy of .336 and the minority recall score of 0.08. 

### Model Performance
Here we outline the best performing score of each algorithm.  
| Model | Weightd F1 | Balanced Accuracy | Minority Recall |
| --- | --- | --- | --- |
| Baseline | 0.444 | 0.336  | 0.08 |
| Decision Tree | 0.728 | 0.642  | 0.45 |
| kNN | 0.753 | 0.631  | 0.32 |
| Random Forest | 0.731 | 0.694  | 0.66 |
| XGBoost | 0.779 | 0.687  | 0.47 |
| Voting Classifier | 0.758 | 0.708 | 0.64 |

XGBoost and KNN models did the best on weighted f1 score, and overall accuracy, but they missed many of the minority class.
Random Forest model fit our goal best with high prediction of all classes throughout including the minority class, with slight tendency to over-predict the minority class. Voting classifier model also performed well, but we chose random forest model because its sensitivity for minority classes were the highest. 

### Final Model Performance (On test data)
| Model | Weightd F1 | Balanced Accuracy | Minority Recall |
| --- | --- | --- | --- |
| Baseline | 0.372 | 0.322  | 0.331 |
| Final Model | 0.725 | 0.672  | 0.63 |

Our final model nearly doubled in weighted F1 and balanced accuracy score from a stratified baseline model. It performed with approximately 70% of overall accuracy. 63% of the minority classes were correctly identified, which is a significant improvement from 8% we saw in the stratified baseline model performance.

## Future Directions

Failing pumps are costly and take critical resources away from the locals that depend on them.  
	- Further research into types and longevity of waterpumps that could replace the heavily failing motor and gravity pumps currently used would be a good start.  

The world bank study showed that village managed waterpoints are 20-40% more likely to fail between years 1 and 20.   
	- Education and technical training for local communities would will allow those in the communities to maintain waterpoints and better manage water pumps.  

Payment is a large issues especially when the average monthly salary in Tanzania is $50.   
	- Financial support systems from local government areas or districs in addition to payment arrangements in place is crucial to driving a reliable water system.  


## Conclusion

Successful prediction of water point condition would allow appropriate allocation of resources in maintenance of water points in Tanzania. This will be an important step in building a sustainable infrastructure that will better many lives in Tanzania.









