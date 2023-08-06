CREATE VIEW pipeline.anomalies_per_day AS
SELECT label, date_trunc('day',start_time) as date, count(*) as total_anomalies
FROM pipeline.event_log
WHERE label IN
    (SELECT label FROM pipeline.anomalies WHERE tracked)
GROUP BY date_trunc('day', start_time), label;
