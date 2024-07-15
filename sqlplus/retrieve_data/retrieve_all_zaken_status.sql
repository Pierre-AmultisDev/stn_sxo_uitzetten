select distinct
   z.startdatum as zaak_startdatum
,  TO_CHAR(EXTRACT(YEAR FROM z.startdatum)) as zaak_startjaar
,  z.aanvraagnummer_string as squitxo_zaaknummer
,  z.extern_zaaknummer as extern_zaaknummer
,  CASE
       WHEN z.zaak_status = 'O' 
	      THEN 'Open'  
	   WHEN z.zaak_status = 'G'
          THEN 'Gesloten'
	   WHEN z.zaak_status = 'C'
          THEN 'Concept'
	   WHEN z.zaak_status = 'T'
          THEN 'Toekomst'
       ELSE z.zaak_status	   
   END zaak_status
,  z.globale_locatie_aanduiding as globale_locatie
,  z.omschrijving as omschrijving

from 
   zaak z

where 0=0

order by 
   z.aanvraagnummer_string
,  z.startdatum