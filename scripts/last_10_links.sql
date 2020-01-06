SELECT
  id,
  LOWER(CONV(id+1000,10,36)) AS short,
  url,
  user_id,
  created
FROM citation
ORDER BY created DESC LIMIT 10
