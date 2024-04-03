WITH latest_itinerary AS (
    SELECT 
    driver_id, 
    MAX(itinerary_started::date) as last_itinerary
    FROM dbt_dw.base_itinerary_package
    GROUP BY driver_id
)
SELECT 
    itinerary.driver_id,
    latest_itinerary.last_itinerary,
    itinerary.n2pk_itinerary_id,
    base_package.zip,
    base_package.state,
    itinerary.itinerary_city,
    base_package.destination_neighborhood
FROM 
    dbt_dw.base_itinerary_package itinerary
LEFT JOIN 
    dbt_dw.base_package base_package ON itinerary.n2pk_package_id = base_package.n1pk_package_id
INNER JOIN 
    latest_itinerary ON itinerary.driver_id = latest_itinerary.driver_id AND itinerary.itinerary_started::date = latest_itinerary.last_itinerary
INNER JOIN    
    dbt_dw.drivers_personal_data personal ON personal.driver_id = itinerary.driver_id
WHERE is_active = 'true'
AND operational_status = 'habilitado'
AND last_itinerary > '2023-06-01'