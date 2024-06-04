select  
   z.*
,  "zaak" as div1
   z.startdatum as zaak_startdatum
,  z.aanvraagnummer_string as squitxo_zaaknummer
,  z.extern_zaaknummer
,  z.zaak_status
,  CONCAT('"',CONCAT(r.omschrijving,'"')) as zaak_resultaat
,  zp.code as zaaktype_code
,  zp.naam as zaaktype_naam
,  ez.code as extern_zaaktype
,  ez.naam as extern_zaaktypenaam
,  CONCAT('"',CONCAT(z.globale_locatie_aanduiding,'"')) as globale_locatie_aanduiding
,  CONCAT('"',CONCAT(z.omschrijving,'"')) as omschrijving
,  hz.olo_dossiernummer
,  z.rappeldatum
from 
   zaak z
   join zaaktype_parent zp on zp.id = z.zaaktype_id
   left join resultaat r on r.id = z.zaak_resultaat_id
   LEFT JOIN HOOFDZAAK hz ON z.id = hz.id
   left join EXTERNE_ZAAKTYPE ez on ez.id = zp.externe_zaaktype_id
where 0=0
--   AND z.extern_zaaknummer not like '%Deelzaak%'
--   AND z.aanvraagnummer_string not like '%Deelzaak%'
-- order by z.startdatum, z.zaak_status, squitxo_zaaknummer
order by z.ID
