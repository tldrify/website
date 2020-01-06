SELECT
  c.id,
  LOWER(CONV(c.id+1000,10,36)) AS short,
  c.url,
  c.user_id,
  c.created,
  s.views
FROM citation c
JOIN 
  (SELECT
    citation_id,
    count(1) AS views
   FROM citation_view
   GROUP BY citation_id ORDER BY 2 DESC LIMIT 5) s
ON c.id=s.citation_id
ORDER BY s.views desc
