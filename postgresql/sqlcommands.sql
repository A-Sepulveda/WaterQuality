-- create a new table
CREATE TABLE public.waterquality
(
  siteid text,
  date date,
  phmean numeric,
  phmax numeric,
  phmin numeric,
  phsd numeric,
  phcnt numeric,
  camean numeric,
  camax numeric,
  camin numeric,
  casd numeric,
  cacnt numeric,
  tempmean numeric,
  tempmax numeric,
  tempmin numeric,
  tempsd numeric,
  tempcnt numeric,
  uniquesitedates text
)
WITH (
  OIDS=FALSE
);
ALTER TABLE public.waterquality
  OWNER TO doadmin;

-- select rows with both temp and ca values
SELECT siteid,
 SUM (camean) AS meanca
FROM
 waterquality
WHERE
 tempmean IS NOT NULL and camean IS NOT NULL
GROUP BY
  siteid;


-- MONTH PRACTICE
-- SUMMER
SELECT * FROM waterquality
WHERE
EXTRACT(MONTH FROM date) in (6,7,8,9);



-- select rows with both temp and ca values... only during summer months
SELECT siteid,
 AVG (camean) AS camean
FROM
  waterquality
WHERE
  tempmean IS NOT NULL and camean IS NOT NULL
AND
  EXTRACT(MONTH FROM date) in (6,7,8,9)
GROUP BY
  siteid;
