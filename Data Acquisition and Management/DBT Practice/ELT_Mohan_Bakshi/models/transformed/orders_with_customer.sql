{{config(materialized='table')}}


SELECT 
    o.order_id,
    c.first_name,
    c.last_name,
    o.order_date,  
    o.total_amount
FROM {{ source('MOHAN_AI2024', 'ORDERS') }} o
JOIN {{ source('MOHAN_AI2024', 'CUSTOMER') }} c ON c.customer_id = o.customer_id