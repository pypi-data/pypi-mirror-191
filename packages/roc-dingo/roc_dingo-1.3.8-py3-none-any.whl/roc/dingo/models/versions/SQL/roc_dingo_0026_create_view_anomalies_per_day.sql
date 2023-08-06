CREATE VIEW pipeline.anomalies_per_day AS
SELECT
    event_log.label,
    is_tracked,
    date_trunc('day',start_time)::DATE as date,
    count(*) as total_anomalies
FROM pipeline.event_log
LEFT OUTER JOIN pipeline.events
ON event_log.label = events.label
WHERE is_anomaly
GROUP BY date_trunc('day', start_time), event_log.label, is_tracked;
