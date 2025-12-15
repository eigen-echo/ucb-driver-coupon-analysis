# Assignment 5.1: Will the Customer Accept the Coupon?

## Context

Imagine driving through town and a coupon is delivered to your cell phone for a restaurant near where you are driving. Would you accept that coupon and take a short detour to the restaurant? Would you accept the coupon but use it on a subsequent trip? Would you ignore the coupon entirely? What if the coupon was for a bar instead of a restaurant? What about a coffee house? Would you accept a bar coupon with a minor passenger in the car? What about if it was just you and your partner in the car? Would weather impact the rate of acceptance? What about the time of day?

Obviously, proximity to the business is a factor on whether the coupon is delivered to the driver or not, but what are the factors that determine whether a driver accepts the coupon once it is delivered to them? How would you determine whether a driver is likely to accept a coupon?

## Overview

The goal of this project is to use what you know about visualizations and probability distributions to distinguish between customers who accepted a driving coupon versus those that did not.

## Data

This data comes to us from the UCI Machine Learning repository and was collected via a survey on Amazon Mechanical Turk. The survey describes different driving scenarios including the destination, current time, weather, passenger, etc., and then ask the person whether he will accept the coupon if he is the driver. Answers that the user will drive there 'right away' or 'later before the coupon expires' are labeled as 'Y = 1' and answers 'no, I do not want the coupon' are labeled as 'Y = 0'. There are five different types of coupons -- less expensive restaurants (under $20), coffee houses, carry out & take away, bar, and more expensive restaurants ($20 - $50).

## Deliverables

Your final product should be a brief report that highlights the differences between customers who did and did not accept the coupons. To explore the data you will utilize your knowledge of plotting, statistical summaries, and visualization using Python. You will publish your findings in a public facing github repository as your first portfolio piece.

## Data Description

Keep in mind that these values mentioned below are average values.

The attributes of this data set include:

### 1. User Attributes

Feature | Data Type | Values | Description
| --- | --- | --- | --- |
destination | Enum | Home, No Urgent Place, Work | Driving destination, 3 distinct values
passanger |Enum |  Alone, Friend(s), Kid(s), Partner | Passangers in the car, 4 distinct values
weather | Enum | Rainy, Snowy, Sunny | Driving weather conditions, 3 distinct values
temperature | Number | 30, 55, 80 | Numerical, rounded to nearest value, Temperature in Fahrenheit
time | Enum | 7AM, 10AM, 2PM, 6PM, 10PM | Rounded to nearest Time of the day in Hour format, 5 distinct values
coupon | Enum | Bar, Carry out & Take away, coffeehouse, Restaurant(<20), Restaurant(20-50) | Coupon category - Restaurant(<20) and Restaurant(20-50) mean restaurants where the expense per person is less than $20 and between $20-$50 respectively
expiration | Enum | 2h, 1d | When does the coupon expire, 2 distinct values
gender | Enum |  Female, Male | Driver's gender
age | Enum | below21, 21, 26, 31, 36, 41, 46, 50plus | Driver's age grouped in bins
maritalStatus | Enum | Divorced, Married partner, Single, Unmarried partner, Widowed | Driver's marital/relationship status
has_children | Boolean | 0, 1 | Whether driver has children or not
education | Enum | Some High School, High School Graduate, Some college - no degree, Associates degree, Bachelors degree, Graduate degree (Masters or Doctorate) | Driver's highest education degree obtained
occupation | Enum | Architecture & Engineering, Arts Design Entertainment Sports & Media, Building & Grounds Cleaning & Maintenance, Business & Financial, Community & Social Services, Computer & Mathematical, Construction & Extraction, Education&Training&Library, Farming Fishing & Forestry, Food Preparation & Serving Related, Healthcare Practitioners & Technical, Healthcare Support, Installation Maintenance & Repair, Legal, Life Physical Social Science, Management, Office & Administrative Support, Personal Care & Service, Production Occupations, Protective Service, Retired, Sales & Related, Student, Transportation & Material Moving, Unemployed | Driver's occupation, 25 distinct values
income | Enum |  Less than $12500, $12500 - $24999, $25000 - $37499, $37500 - $49999, $50000 - $62499, $62500 - $74999, $75000 - $87499, $87500 - $99999, $100000 or More | Driver's income range, 9 distinct groups
car | Enum | Car that is too old to install Onstar :D, crossover, do not drive, Mazda5, Scooter and motorcycle | Car type, lot of nulls
Bar | Enum | never, less1, 1~3, 4~8, gt8 | Number of times respondent goes to a bar every month
CoffeeHouse | Enum | less1, never, 1~3, 4~8, gt8 | Number of times respondent goes to a coffeehouse every month, 5 distinct values
CarryAway | Enum | never, less1, 1~3, 4~8, gt8 | Number of times respondent eats take away food every month
RestaurantLessThan20 | Enum | never, less1, 1~3, 4~8, gt8 | Number of times respondent eats at a restaurant where the expense per person is less than $20 every month
Restaurant20To50 | Enum | never, less1, 1~3, 4~8, gt8 | Number of times respondent eats at a restaurant where the expense per person is between $20 to $50 every month
toCoupon_GEQ5min | Boolean | 0, 1 | Driving distance to the venue for the coupon is greater than 5 minutes
toCoupon_GEQ15min | Boolean | 0, 1 | Driving distance to the venue for the coupon is greater than 15 minutes
toCoupon_GEQ25min | Boolean | 0, 1 | Driving distance to the venue for the coupon is greater than 25 minutes
direction_same | Boolean | 0, 1 | Is the venue for the coupon in the same driving direction as the driver's destination?
direction_opp | Boolean | 0, 1 | Is the venue for the coupon in the opposite driving direction as the driver's destination?
Y | Boolean | 0, 1 | Did the respondent accept the coupon? (1 if they answered 'right away' or 'later before the coupon expires'; 0 if they answered 'no, I do not want the coupon')


## Analysis Problems

Use the prompts below to get started with your data analysis:

### Initial Data Exploration

1. Read in the `coupons.csv` file.
2. Investigate the dataset for missing or problematic data.
3. Explore the data for null records and operate on them
4. What proportion of the total observations chose to accept the coupon?
5. Use a bar plot to visualize the `coupon` column.
6. Use a histogram to visualize the temperature column.

### Investigating the Bar Coupons

Now, we will lead you through an exploration of just the bar related coupons:

1. Create a new `DataFrame` that contains just the bar coupons.
2. What proportion of bar coupons were accepted?
3. Compare the acceptance rate between those who went to a bar 3 or fewer times a month to those who went more.
4. Compare the acceptance rate between drivers who go to a bar more than once a month and are over the age of 25 to the all others. Is there a difference?
5. Use the same process to compare the acceptance rate between drivers who go to bars more than once a month and had passengers that were not a kid and had occupations other than farming, fishing, or forestry.
6. Compare the acceptance rates between those drivers who:
   - go to bars more than once a month, had passengers that were not a kid, and were not widowed *OR*
   - go to bars more than once a month and are under the age of 30 *OR*
   - go to cheap restaurants more than 4 times a month and income is less than 50K.
7. Based on these observations, what do you hypothesize about drivers who accepted the bar coupons?

### Independent Investigation

Using the bar coupon example as motivation, you are to explore one of the other coupon groups and try to determine the characteristics of passengers who accept the coupons.