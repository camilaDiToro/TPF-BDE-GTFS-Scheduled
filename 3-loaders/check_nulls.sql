SELECT * FROM public.agency a
WHERE (agency_id IS NOT NULL 
AND agency_name IS NOT NULL
AND agency_url IS NOT NULL
AND agency_timezone IS NOT NULL);

SELECT *
FROM public.stops s
WHERE (stop_id IS NOT NULL
  AND stop_name IS NOT NULL
  AND location_type = 'stop'
  AND stop_loc IS NOT NULL
  );

SELECT *
FROM public.routes r
WHERE (route_id IS NOT NULL
  AND agency_id IS NOT NULL
  AND route_type IS NOT NULL
  AND (
    route_short_name IS NOT NULL
    OR route_long_name IS NOT NULL
  ));

SELECT *
FROM public.trips t
WHERE (trip_id IS NOT NULL
  AND route_id IS NOT NULL
  AND service_id IS NOT NULL
  AND shape_id IS NOT NULL);

SELECT *
FROM public.stop_times st
WHERE NOT (trip_id IS NOT NULL
  AND stop_sequence IS NOT NULL
  AND stop_id IS NOT NULL
  AND arrival_time IS NOT NULL
  AND departure_time IS NOT NULL 
);

SELECT *
FROM public.calendar c
WHERE (service_id IS NOT NULL
  AND monday IS NOT NULL
  AND tuesday IS NOT NULL
  AND wednesday IS NOT NULL
  AND thursday IS NOT NULL
  AND friday IS NOT NULL
  AND saturday IS NOT NULL
  AND sunday IS NOT NULL
  AND start_date IS NOT NULL
  AND end_date IS NOT NULL
);

SELECT *
FROM public.calendar_dates cd
WHERE (service_id IS NOT NULL
  AND date IS NOT NULL
  AND exception_type IS NOT NULL);

SELECT *
FROM public.shapes s
WHERE NOT (shape_id IS NOT NULL
  AND shape_pt_loc IS NOT NULL
  AND shape_pt_sequence IS NOT NULL);