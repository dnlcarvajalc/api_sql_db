SELECT
    d.department AS department,
    j.job AS job,
    SUM(CASE WHEN strftime('%m', he.datetime) BETWEEN '01' AND '03' THEN 1 ELSE 0 END) AS Q1,
    SUM(CASE WHEN strftime('%m', he.datetime) BETWEEN '04' AND '06' THEN 1 ELSE 0 END) AS Q2,
    SUM(CASE WHEN strftime('%m', he.datetime) BETWEEN '07' AND '09' THEN 1 ELSE 0 END) AS Q3,
    SUM(CASE WHEN strftime('%m', he.datetime) BETWEEN '10' AND '12' THEN 1 ELSE 0 END) AS Q4
FROM hired_employees he
JOIN departments d ON he.department_id = d.id
JOIN jobs j ON he.job_id = j.id
WHERE strftime('%Y', he.datetime) = :year
GROUP BY d.department, j.job
ORDER BY d.department ASC, j.job ASC;