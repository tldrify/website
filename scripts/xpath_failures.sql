SELECT
  id,
  LOWER(CONV(id+1000,10,36)) AS short,
  url
FROM citation
WHERE id IN
  (SELECT
     citation_id
   FROM citation_view
   WHERE xpath_failure IS TRUE
   )
