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

- **Gender**: male, female
- **Age**: below 21, 21 to 25, 26 to 30, etc.
- **Marital Status**: single, married partner, unmarried partner, or widowed
- **Number of children**: 0, 1, or more than 1
- **Education**: high school, bachelors degree, associates degree, or graduate degree
- **Occupation**: architecture & engineering, business & financial, etc.
- **Annual income**: less than $12500, $12500 - $24999, $25000 - $37499, etc.
- **Number of times that he/she goes to a bar**: 0, less than 1, 1 to 3, 4 to 8 or greater than 8
- **Number of times that he/she buys takeaway food**: 0, less than 1, 1 to 3, 4 to 8 or greater than 8
- **Number of times that he/she goes to a coffee house**: 0, less than 1, 1 to 3, 4 to 8 or greater than 8
- **Number of times that he/she eats at a restaurant with average expense less than $20 per person**: 0, less than 1, 1 to 3, 4 to 8 or greater than 8
- **Number of times that he/she goes to a bar**: 0, less than 1, 1 to 3, 4 to 8 or greater than 8

### 2. Contextual Attributes

- **Driving destination**: home, work, or no urgent destination
- **Location of user, coupon and destination**: we provide a map to show the geographical location of the user, destination, and the venue, and we mark the distance between each two places with time of driving. The user can see whether the venue is in the same direction as the destination.
- **Weather**: sunny, rainy, or snowy
- **Temperature**: 30F, 55F, or 80F
- **Time**: 10AM, 2PM, or 6PM
- **Passenger**: alone, partner, kid(s), or friend(s)

### 3. Coupon Attributes

- **Time before it expires**: 2 hours or one day

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