-- Создание таблицы
CREATE TABLE street_works (
    id SERIAL PRIMARY KEY,
    dataset_code VARCHAR(10),
    source_object_id VARCHAR(20),
    work_type TEXT,
    status VARCHAR(20),
    start_dt DATE,
    end_dt DATE,
    contractor TEXT,
    priority NUMERIC,
    geom_a_wkt TEXT,
    geom_b_wkt TEXT,
    geom_c_wkt TEXT,
    address_raw TEXT,
    comment TEXT,
    geometry GEOMETRY
);

-- Загрузка CSV
\copy street_works(
    dataset_code, source_object_id, work_type, status, 
    start_dt, end_dt, contractor, priority, 
    geom_a_wkt, geom_b_wkt, geom_c_wkt, address_raw, comment
) 
FROM 'D:/Projects/street_cases.csv' 
DELIMITER '$' 
CSV HEADER;

-- Проверка
SELECT COUNT(*) FROM street_works;
SELECT * FROM street_works LIMIT 5;


-- 1. Общая статистика
SELECT 
    COUNT(*) AS total_records,
    COUNT(DISTINCT dataset_code) AS datasets,
    STRING_AGG(DISTINCT dataset_code, ', ') AS datasets_list
FROM street_works;

-- Количество записей по наборам
SELECT 
    dataset_code,
    COUNT(*) AS record_count
FROM street_works
GROUP BY dataset_code
ORDER BY dataset_code;


-- 2. Дубликаты source_object_id
SELECT 
    dataset_code,
    source_object_id,
    COUNT(*) AS duplicate_count,
    STRING_AGG(id::text, ', ') AS duplicate_ids
FROM street_works
GROUP BY dataset_code, source_object_id
HAVING COUNT(*) > 1;


-- 3. Некорректные даты
SELECT 
    dataset_code,
    source_object_id,
    start_dt,
    end_dt
FROM street_works
WHERE start_dt > end_dt;


-- 4. Пропуски в полях
-- contractor
SELECT 
    dataset_code,
    source_object_id
FROM street_works
WHERE contractor IS NULL OR contractor = '';

-- priority
SELECT 
    dataset_code,
    source_object_id
FROM street_works
WHERE priority IS NULL;

-- end_dt
SELECT 
    dataset_code,
    source_object_id
FROM street_works
WHERE end_dt IS NULL;


-- 5. Геометрия
-- Отсутствие данных
SELECT 
    dataset_code,
    source_object_id,
    CASE 
        WHEN geom_a_wkt IS NOT NULL THEN 'A'
        WHEN geom_b_wkt IS NOT NULL THEN 'B'
        WHEN geom_c_wkt IS NOT NULL THEN 'C'
        ELSE 'NONE'
    END AS geom_source
FROM street_works
WHERE (geom_a_wkt IS NULL OR geom_a_wkt = 'nan')
  AND (geom_b_wkt IS NULL OR geom_b_wkt = 'nan')
  AND (geom_c_wkt IS NULL OR geom_c_wkt = 'nan');

-- Невалидная геометрия
SELECT 
    dataset_code,
    source_object_id,
    geom_a_wkt AS geometry_wkt
FROM street_works
WHERE geom_a_wkt IS NOT NULL 
  AND geom_a_wkt != 'nan'
  AND NOT ST_IsValid(ST_GeomFromText(geom_a_wkt, 4326))
UNION ALL
SELECT 
    dataset_code,
    source_object_id,
    geom_b_wkt
FROM street_works
WHERE geom_b_wkt IS NOT NULL 
  AND geom_b_wkt != 'nan'
  AND NOT ST_IsValid(ST_GeomFromText(geom_b_wkt, 4326))
UNION ALL
SELECT 
    dataset_code,
    source_object_id,
    geom_c_wkt
FROM street_works
WHERE geom_c_wkt IS NOT NULL 
  AND geom_c_wkt != 'nan'
  AND NOT ST_IsValid(ST_GeomFromText(geom_c_wkt, 4326));
