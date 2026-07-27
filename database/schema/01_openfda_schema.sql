SELECT safety_report_id, COUNT(*)
FROM fact_safety_report
GROUP BY safety_report_id
HAVING COUNT(*) > 1;