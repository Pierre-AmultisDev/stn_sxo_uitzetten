SELECT 
  z.AANVRAAGNUMMER_STRING AS squitxo_zaaknummer
, z.EXTERN_ZAAKNUMMER AS EXTERN_NUMMER
, bw.*
FROM VW_G_BOUW_UNION bw
LEFT JOIN ZAAK z ON bw.ZAAK_ID = z.id 
order by 
   z.aanvraagnummer_string
--,  z.startdatum