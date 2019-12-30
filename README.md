tldrify.com
============

Source code for [tldrify.com](https://tldrify.com).

### Components ###

 * `app.py`                 Python Flask application.
 * `backup-mysql.sh`        Backup script that should run periodically.
 * `init-db.py`             Script that initializes database from entities contained in tldr/model.py.
 * `send-mails.py`          Offline mail sender script that should run periodically.
 * `daily-report.py`        Script that should run on daily basis, which sends usage report to admins.

### Useful DB queries for debugging ###

##### Latest 10 links added #####

```sql
SELECT
  id,
  LOWER(CONV(id+1000,10,36)) AS short,
  url,
  user_id,
  created
FROM citation
ORDER BY created DESC LIMIT 10
```

##### Short links with broken text selection #####

```sql
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
```

##### 5 mostly viewed citations #####

```sql
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
```

