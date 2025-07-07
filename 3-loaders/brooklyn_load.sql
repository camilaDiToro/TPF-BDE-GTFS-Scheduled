INSERT INTO public.stops
SELECT
    stop_id,
    stop_code,
    stop_name,
    stop_desc,
    stop_loc,
    zone_id,
    stop_url,
    location_type::text::public.location_type_val,
    parent_station,
    stop_timezone,
    wheelchair_boarding::text::public.wheelchair_boarding_val,
    level_id,
    platform_code
FROM brooklyn.stops
ON CONFLICT (stop_id) DO NOTHING;

INSERT INTO public.calendar (service_id, monday, tuesday, wednesday, thursday, friday, saturday, sunday, start_date, end_date)
SELECT
    service_id,
    monday::text::availability,
    tuesday::text::availability,
    wednesday::text::availability,
    thursday::text::availability,
    friday::text::availability,
    saturday::text::availability,
    sunday::text::availability,
    start_date,
    end_date
FROM brooklyn.calendar;

INSERT INTO public.calendar_dates
SELECT
    service_id,
    date,
    exception_type::text::exception_type_v
FROM brooklyn.calendar_dates;

INSERT INTO public.shapes (shape_id, shape_pt_sequence, shape_dist_traveled, shape_pt_loc)
SELECT
    shape_id,
    shape_pt_sequence,
    shape_dist_traveled,
    shape_pt_loc
FROM brooklyn.shapes;

INSERT INTO public.trips (trip_id, route_id, service_id, trip_headsign, trip_short_name,
                         direction_id, block_id, shape_id, wheelchair_accessible, bikes_allowed)
SELECT
    trip_id,
    route_id,
    service_id,
    trip_headsign,
    trip_short_name,
    direction_id,
    block_id,
    shape_id,
    wheelchair_accessible::text::wheelchair_accessibility,
    bikes_allowed::text::bikes_allowance
FROM brooklyn.trips;

INSERT INTO public.stop_times (trip_id, arrival_time, departure_time, stop_id, stop_sequence, stop_sequence_consec,
                              stop_headsign, pickup_type, drop_off_type, shape_dist_traveled, timepoint, trip_start_time)
SELECT
    trip_id,
    arrival_time,
    departure_time,
    stop_id,
    stop_sequence,
    stop_sequence_consec,
    stop_headsign,
    pickup_type::text::pickup_drop_off_type,
    drop_off_type::text::pickup_drop_off_type,
    shape_dist_traveled,
    timepoint::text::timepoint_v,
    trip_start_time
FROM brooklyn.stop_times;