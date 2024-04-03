SELECT
personal.address_formatted,
personal.vicinity,
personal.city,
zip,
personal.state,
driver_id,
onboard_date,
has_taken_itineraries,
marital_status,
gender,
transport_type,
first_itinerary_created,
last_itinerary_created,
source,
fleet_type,
itineraries
FROM dbt_dw.drivers_personal_data personal
LEFT JOIN prodpostgres.players_loggiuseraddress address
ON address.user_id = personal.driver_id
WHERE operational_status = 'habilitado'
AND is_active = 'true'
AND personal.address_formatted IS NOT NULL
AND last_itinerary_created::date > '2023-06-01'