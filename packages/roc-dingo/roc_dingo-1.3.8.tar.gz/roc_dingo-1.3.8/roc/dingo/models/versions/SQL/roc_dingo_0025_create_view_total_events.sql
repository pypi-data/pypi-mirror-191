CREATE VIEW pipeline.total_events AS
SELECT label,count(label) AS total_event
FROM pipeline.event_log
GROUP BY label;
