**Customer Churn & Retention Analysis**

***Initial Findings*** 

1. **Overall Churn:**
   - Total Customers: 7043
   - Total Churned Customers: 1869
   - Overall Churn Rate: 26.5%

2. **Contract Type**
    - Month-to-month customers have the highest churn rate, approximately 42.7%
    - One year contracts have a churn rate of approximately 11.3%
    - Two year contracts have a churn rate of approximately 2.8%
Business Implication: Investigate targeted retention offers and incentives for eligible month-to-month customers 

3. **Payment Methods**
    - Electronic check users have the highest churn rate, approximately 45%
    - Customers that opt for automatic bank transfers and automatic credit card payments have the lowest churn rates, approximately 17%
Business Implication: Investigate the relationship between payment methods, contract type, and churn before proposing payment changes. Also, consider offering incentives for customers to switch from electronic check to automatic payment methods. 

4. **Monthly Charges**
    - Average monthly charge for churned customers: **74.44**
    - Average monthly charge for retained customers: **61.26**
Business Implication: Investigate whether pricing, services combinations, or customer segments explain the difference

5. **Customer Demographics**
    - Senior Citizens: 20% of customer base, churn rate of ~30%
    - Partners & Dependents: Having a partner or dependents reduces churn, regardless of gender
Business Implication: Consider offering targeted incentives for senior citizens and discounts for customers with partners/dependents

6. **Partner and Dependent Status**
    - Customers without a partner or dependents had the highest observed churn percentage at 34.24%.
    - Customers with both a partner and dependents had the lowest observed churn percentage at 14.24%.
    - The 20-percentage-point difference suggests that household status may be useful for further customer segmentation. Additional analysis is needed to assess the influence of other variables.

7. **Customer Tenure**
    - Customers with 0–12 months of tenure had the highest observed churn percentage at 47.44%.
    - Customers with 49–72 months of tenure had the lowest observed churn percentage at 9.51%.
    - The 37.93-percentage-point difference suggests that early customer retention deserves further investigation, including onboarding, service quality, and customer support.

8. **Monthly Charges and Churn**
    - Customers with monthly charges above the overall average had a churn percentage of 34.54%
    - Customers with monthly charges at or below the overall average had a churn percentage of 16.47%
    - The 18.07-percentage-point difference suggests that higher monthly charges may be associated with higher churn. Additional analysis is needed to assess the influence of other variables.
Recommendation: Investigate whether contract type, tenure, and subscribed services help explain this difference before recommending pricing changes.

9. **Contract Type and Tenure Analysis**
    - Month-to-month customers with 0–12 months of tenure had the highest observed churn percentage at 51.35% (1,024 churned out of 1,994 customers).
    - Month-to-month churn remained elevated across all tenure groups, ranging from 26.02% to 51.35%.
    - Two-year contract segments had comparatively low observed churn percentages, ranging from 0% to 3.33% in this analysis.
    -The results suggest that early-tenure, month-to-month customers are a priority segment for further retention analysis.
Business recommendation: Investigate onboarding and early customer experiences for month-to-month customers. Explore whether targeted support, service improvements, or suitable longer-term contract options are associated with improved retention. Evaluate the results carefully and avoid assuming that contract length alone causes lower churn.

**Segment Comparison Against Overall Churn**
    - The overall churn share was 26.54%.
    - Month-to-month customers with 0–12 months of tenure had a churn percentage of 51.35%, which was 24.82 percentage points above the overall baseline.
    - Month-to-month customers with 13–24 months of tenure had a churn percentage of 37.72%, or 11.18 percentage points above the baseline.
    - Month-to-month customers with 25–48 months of tenure had a churn percentage of 32.92%, or 6.38 percentage points above the baseline.
    - The early-tenure, month-to-month segment was the highest-priority segment for further investigation based on both its elevated churn percentage and its size.
Recommended next step: Investigate early-tenure customer experience and month-to-month contract characteristics. Any retention initiatives should be evaluated with measurable outcomes before concluding that they reduce churn.

**Limitations**
 - These are obsevational associations, not proof of causation
 - The dataset is a snapshot and does not establish a time-specific churn rate 
 - Further analysis is needed before recommending specific interventions 

**Data Quality and Validation**
    -The cleaned dataset contains 7,043 customer records and 21 columns. SQL validation confirmed that all customer IDs are unique and that no customer IDs or churn labels are missing.
    -Additional checks found no negative tenure values, negative monthly charges, negative total charges, tenure values exceeding 72 months, or invalid non-null churn labels.
    -Eleven records have missing `TotalCharges` values. All 11 correspond to customers with zero months of tenure, while no missing values were found among customers with positive tenure. These values were retained as missing rather than imputed without sufficient evidence.

**Limitations:** These checks cover specific data-quality rules and do not establish that every field is error-free. The dataset is a customer snapshot, so the observed associations should not be interpreted as proof of causation.