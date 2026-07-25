-- 1. Analýza OTIF (On-Time In-Full) a meškania podľa kategórií produktov
WITH CategoryStats AS (
    SELECT 
        p.category_name,
        COUNT(f.order_id) AS total_orders,
        SUM(f.late_risk) AS delayed_orders,
        ROUND(AVG(f.days_for_shipping_real), 2) AS avg_real_shipping_days,
        ROUND(AVG(f.days_for_shipment_scheduled), 2) AS avg_scheduled_shipping_days,
        ROUND(SUM(f.gross_profit), 2) AS total_profit
    FROM fact_shipments f
    JOIN dim_product p ON f.product_card_id = p.product_card_id
    GROUP BY p.category_name
)
SELECT 
    category_name,
    total_orders,
    delayed_orders,
    ROUND((delayed_orders::NUMERIC / total_orders) * 100, 2) AS delay_rate_pct,
    ROUND(avg_real_shipping_days - avg_scheduled_shipping_days, 2) AS avg_delay_days,
    total_profit
FROM CategoryStats
WHERE total_orders > 100
ORDER BY delay_rate_pct DESC;

-- Analýza hodnoty zákazníkov (Customer Lifetime Value) pomocou Window Functions
WITH CustomerSpend AS (
    SELECT 
        c.customer_id,
        c.customer_fname || ' ' || c.customer_lname AS customer_name,
        c.customer_segment,
        COUNT(DISTINCT f.order_id) AS total_orders,
        ROUND(SUM(f.sales), 2) AS total_spent,
        ROUND(SUM(f.gross_profit), 2) AS total_profit
    FROM fact_shipments f
    JOIN dim_customer c ON f.customer_id = c.customer_id
    GROUP BY c.customer_id, c.customer_fname, c.customer_lname, c.customer_segment
),
RankedCustomers AS (
    SELECT 
        customer_id,
        customer_name,
        customer_segment,
        total_orders,
        total_spent,
        total_profit,
        -- Rozdelenie zákazníkov do 4 skupín (1 = TOP 25% podľa útrat)
        NTILE(4) OVER (ORDER BY total_spent DESC) AS spend_quartile,
        -- Kumulatívny súčet tržieb cez všetkých zákazníkov
        ROUND(SUM(total_spent) OVER (ORDER BY total_spent DESC), 2) AS cumulative_sales
    FROM CustomerSpend
)
SELECT 
    customer_id,
    customer_name,
    customer_segment,
    total_orders,
    total_spent,
    total_profit,
    spend_quartile
FROM RankedCustomers
ORDER BY total_spent DESC
LIMIT 20;



---------------------------

-- Vytvorenie konsolidovaného analytického pohľadu pre Power BI Dashboard
CREATE OR REPLACE VIEW vw_supply_chain_analytics AS
SELECT 
    f.order_id,
    f.order_item_id,
    f.order_date_key,
    d.full_date AS order_date,
    d.year,
    d.quarter,
    d.month,
    d.month_name,
    d.day_of_week,
    
    -- Zákazník
    c.customer_id,
    c.customer_fname || ' ' || c.customer_lname AS customer_name,
    c.customer_city,
    c.customer_country,
    c.customer_segment,
    
    -- Produkt
    p.product_card_id,
    p.product_name,
    p.category_name,
    p.department_name,
    p.product_price,
    
    -- Logistika a Metriky
    f.days_for_shipping_real,
    f.days_for_shipment_scheduled,
    f.delivery_status,
    f.late_risk,
    f.sales,
    f.order_item_discount,
    f.gross_profit,
    
    -- Vypočítané stĺpce priamo v databáze (znížia záťaž v Power BI)
    (f.days_for_shipping_real - f.days_for_shipment_scheduled) AS shipping_delay_days,
    CASE 
        WHEN f.gross_profit < 0 THEN 1 
        ELSE 0 
    END AS is_unprofitable_order

FROM fact_shipments f
JOIN dim_customer c ON f.customer_id = c.customer_id
JOIN dim_product p ON f.product_card_id = p.product_card_id
JOIN dim_date d ON f.order_date_key = d.date_key;