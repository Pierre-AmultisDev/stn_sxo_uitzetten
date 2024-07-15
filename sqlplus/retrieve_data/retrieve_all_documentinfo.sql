SELECT 
  z.aanvraagnummer_string AS squitxo_zaaknummer
, z.extern_zaaknummer AS extern_zaaknummer
, d.*
FROM csv_document d
LEFT JOIN zaak z ON d.zaak_id=z.id
