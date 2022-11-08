# Udacity Project - 2016 Boston Airbnb

# Description

Airbnb has certainly made an impact on today's hospitality industry. In 2022, Airbnb has recorded 6 million listings in over 100,000 cities world wide, which has left many people wondering, "should I get in on the action?"

# Motivation

Using 2016 Airbnb data from the Boston area, I chose to explore metrics to help investors answer potential questions such as:

#### 1. What is the Relationship Between Price and Utilization?
#### 2. What are the top 10 neighbourhoods with the highest median projected revenue?
#### 3. Which Neighborhoods Will Make Me My Money Back the Soonest?


# Installation  
  The libraries used in this project are all native to Anaconda enviroment. The following libraries were used for the project:
```bash
  import pandas as pd
  import numpy as np
  import matplotlib.pyplot as plt
```

# File
 
  The file used in this analysis was retrieved from Kaggle - https://www.kaggle.com/datasets/airbnb/boston.
  The 'listings.csv' data set consists of 2016 Airbnb listings in the Boston Area. There were a total of 3585 unique obersvations and 95 variables.
  
# Summary of Results
1. I observed that there was **no clear relationship** between **price per nights and utilization rate** in the Boston Airbnb listings within the data set 
2. I determined the neighborhoods with the **highest potential revenue** by combining **prices per night * 365 * utilization rates**
3. Finally, I determined the neighborhoods with the **quickest returns on investment** given their yearly revenue potential and the median house prices per neighborhood

*Other metrics should be considered when exploring potential property investments.

Check out my blog post for more analysis. 

https://medium.com/@lucas.orjales97/where-should-you-invest-for-an-airbnb-96e9f062d651

# Acknowledgements

I used RedFin's **Marketing Insights tool** to collect median house prices per neighborhood in the dataset.

https://www.redfin.com/
  
  
