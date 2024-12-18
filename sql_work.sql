WITH Sessioned_Events AS (
    SELECT 
        user_id,
        value AS template,
        event_time,
        ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY event_time) AS rn,
        LAG(event_time) OVER (PARTITION BY user_id ORDER BY event_time) AS prev_event_time
    FROM logs
    WHERE event = 'template_selected'
),

Filtered_Templates AS (
    SELECT 
        template,
        COUNT(*) AS template_count,
        SUM(CASE WHEN event_time - prev_event_time <= INTERVAL '5 minutes' THEN 1 ELSE 0 END) AS consecutive_count
    FROM Sessioned_Events
    GROUP BY user_id, template
)

SELECT 
    template,
    SUM(template_count) AS total_count
FROM Filtered_Templates
WHERE consecutive_count >= 1
GROUP BY template
ORDER BY total_count DESC
LIMIT 5;