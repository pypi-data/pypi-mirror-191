Pydeequ data assertion module 

1. Compliance
2. Completeness
3. Mean
4. ApproxCountDistinct

NOTE: 
Mean Metric Should Contain numeric type column from input source
For Compliance need to provide condition:Required
At Default Information Threshold > Warning Threshold > Error Threshold
Metric_Value > Information Threshold > Warning Threshold > Error Threshold- Returns Null
Information Threshold > Metric_Value > Warning Threshold > Error Threshold- Returns Information
Information Threshold > Warning Threshold > Metric_Value > Error Threshold- Returns Warning
Metric_Value > Information Threshold > Warning Threshold > Error Threshold> Metric_Value - Returns Error