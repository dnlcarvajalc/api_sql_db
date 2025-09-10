SELECT
    d.id,
    d.department,
    COUNT(he.id) AS hired
FROM departments d
JOIN hired_employees he ON he.department_id = d.id
WHERE strftime('%Y', he.datetime) = :year
GROUP BY d.id, d.department
HAVING COUNT(he.id) > (
    SELECT AVG(dept_count) FROM (
        SELECT COUNT(he2.id) AS dept_count
        FROM departments d2
        JOIN hired_employees he2 ON he2.department_id = d2.id
        WHERE strftime('%Y', he2.datetime) = :year
        GROUP BY d2.id
    )
)
ORDER BY hired DESC;