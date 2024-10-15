/*
 * Versie voor SquitXO
 * ======================
 * Datum:    20240723
 * Versie:   003
 * Bestand:  retrieve_all_zaken_zaaktype.sql
 * Auteur:   Pierre Veelen
 *
 * Function: Levert een table met de status van alle zaken van SquitXO
 *
 * ToDo: 
 *
 */
select distinct
   z.startdatum as zaak_startdatum
   
,  TO_CHAR(EXTRACT(YEAR FROM z.startdatum)) as zaak_startjaar
  
,  CASE -- als zaakid een deelzaak is vul dan hoofdzaak id in. Anders eigen zaak id
	WHEN dz1.hoofdzaak_id is not NULL
      THEN -- dit is een deelzaak kies hoofdzaak id
	    (SELECT aanvraagnummer_string FROM zaak WHERE zaak.id = dz1.hoofdzaak_id)
      ELSE -- dit is geen deelzaak kies het eigen zaak id
	    (SELECT aanvraagnummer_string FROM zaak WHERE zaak.id = z.id)	  
   END squitxo_hoofdzaaknummer

, CASE -- bepaal of zaakid een deelzaak is 
	WHEN dz1.hoofdzaak_id is not NULL
      THEN 'JA' -- dit is een deelzaak
      ELSE 'NEE' -- dit is geen deelzaak
   END is_deelzaak
   
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
,  zp.naam as zaaktype_naam

from 
   zaak z
   left join deelzaak dz1 on z.id=dz1.id
   left join zaaktype_parent zp on z.zaaktype_id = zp.id
where 0=0

order by 
   z.aanvraagnummer_string
,  z.startdatum