![logo_ironhack_blue 7](https://user-images.githubusercontent.com/23629340/40541063-a07a0a8a-601a-11e8-91b5-2f13e4e6b441.png)

# Lab | Customer Analysis

In today's lesson we talked about linear regression and how multicollinearity can impact the model. In this lab, we will test your knowledge on those things using the `marketing_customer_analysis.csv` file. You have been using the same data in the previous labs. You can continue using the same jupyter file. The file can be found in the `Data` folder.

### Get the data 

Use the jupyter file from the previous lab on Customer Analysis

### Complete the following task 

- Check the data types of the columns. Get the numeric data into dataframe called `numerical` and categorical columns in a dataframe called `categoricals`. (You can use np.number and np.object to select the numerical data types and categorical data types respectively)

- For the numerical variables:
  - Use Matplotlib to construct histograms to check the normality of the numerical variables visually
  - Check the multicollinearity between the features. Please note that we will use the column `total_claim_amount` later as the target variable. 
  
- Drop one of the two features that show a high correlation between them (greater than 0.9). Write code for both the correlation matrix and for seaborn heatmap. If there is no pair of features that have a high correlation, then do not drop any features

- Split data into Y (`total_claim_amount`) and X (numerical, independent variables)

- Conduct Linear Regressions
  - Using Statsmodels
  - Using sklearn
  - Interpret results