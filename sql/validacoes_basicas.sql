-- Quantidade e unicidade
SELECT COUNT(*) AS total_registros,
	COUNT(DISTINCT unique_key) AS chaves_unicas
FROM stg_nyc311;

-- Chaves nulas
SELECT COUNT(*) AS chaves_nulas
FROM stg_nyc311
WHERE unique_key IS NULL;

-- Datas 
SELECT MIN(created_date) AS primeira_data, 
	MAX(created_date) AS ultima_data
FROM stg_nyc311;

-- Consistência do tempo de resolução
SELECT COUNT(*) AS tempos_negativos
FROM stg_nyc311
WHERE resolution_time_seconds < 0

-- Quantos chamados ainda não possuem tempo de resolução
SELECT COUNT(*) AS sem_tempo_resolucao
FROM dbo.stg_nyc311
WHERE resolution_time_seconds IS NULL;

SELECT TOP 20
    unique_key,
    created_date,
    closed_date,
    status,
    resolution_time_seconds
FROM dbo.stg_nyc311
WHERE resolution_time_seconds < 0
ORDER BY resolution_time_seconds;

SELECT status,
    COUNT(*) AS quantidade
FROM dbo.stg_nyc311
WHERE resolution_time_seconds < 0
GROUP BY status
ORDER BY quantidade DESC;

-- Confirmando os registros para deletar
SELECT COUNT(8) AS registros_a_remover
FROM stg_nyc311
WHERE closed_date < created_date;

-- Remoção
DELETE FROM stg_nyc311
WHERE closed_date < created_date;

-- Verificação do total
SELECT COUNT(*) AS total_registros
FROM dbo.stg_nyc311;

SELECT COUNT(*) AS inconsistencias
FROM dbo.stg_nyc311
WHERE closed_date < created_date;