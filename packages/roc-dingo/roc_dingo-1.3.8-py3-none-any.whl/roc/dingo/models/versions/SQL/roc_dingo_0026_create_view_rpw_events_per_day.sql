CREATE OR REPLACE VIEW pipeline.rpw_events_per_day AS
    SELECT
        cal_date.cal_date::DATE as date,
        count(event_log.label) as total
        FROM
            (SELECT  CAST('2020-02-01' AS DATE) + (n || ' day')::INTERVAL as cal_date
            FROM generate_series(0, 10000) n ) cal_date
        LEFT OUTER JOIN pipeline.event_log
            ON date_trunc('day', event_log.start_time) = date_trunc('day',cal_date.cal_date)
        LEFT OUTER JOIN pipeline.events
            ON event_log.label = events.label
            AND events.is_tracked
            AND events.origin = 'RPW'
    GROUP BY cal_date.cal_date
    HAVING cal_date.cal_date < now()
    ORDER BY cal_date.cal_date;
