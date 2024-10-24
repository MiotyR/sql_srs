SELECT department,
MEAN(wage) as mean_wages
FROM wages
GROUP BY department