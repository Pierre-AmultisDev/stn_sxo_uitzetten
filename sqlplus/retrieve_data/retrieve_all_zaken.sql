/*
 * Versie voor SquitXO
 * ======================
 * Datum:    20240715
 * Versie:   003
 * Bestand:  retreive_all_zaken.sql
 * Auteur:   Pierre Veelen
 *
 * Function: Levert een table met gegevens van alle zaken van SquitXO
 *
 * ToDo: 
 *
 */
select distinct

-- CASE -- als zaakid een deelzaak is vul dan hoofdzaak id in. Anders eigen zaak id
--	WHEN dz1.hoofdzaak_id is not NULL
--      THEN dz1.hoofdzaak_id -- dit is een deelzaak kies hoofdzaak id
--      ELSE z.id -- dit is geen deelzaak kies het eigen zaak id
--   END hoofdzaakid

  CASE -- als zaakid een deelzaak is vul dan hoofdzaak id in. Anders eigen zaak id
	WHEN dz1.hoofdzaak_id is not NULL
      THEN -- dit is een deelzaak kies hoofdzaak id
	    (SELECT aanvraagnummer_string FROM zaak WHERE zaak.id = dz1.hoofdzaak_id)
      ELSE -- dit is geen deelzaak kies het eigen zaak id
	    (SELECT aanvraagnummer_string FROM zaak WHERE zaak.id = z.id)	  
   END squitxo_hoofdzaaknummer
   
,  z.startdatum as zaak_startdatum
,  z.aanvraagnummer_string as squitxo_zaaknummer

--, CASE -- bepaal of zaakid een hoofdzaak is
--	WHEN dz2.id is not NULL
--      THEN 'JA' -- dit is een hoofdzaak
--      ELSE 'NEE' -- dit is geen hoofdzaak
--   END is_hoofdzaak
   
, CASE -- bepaal of zaakid een deelzaak is 
	WHEN dz1.hoofdzaak_id is not NULL
      THEN 'JA' -- dit is een deelzaak
      ELSE 'NEE' -- dit is geen deelzaak
   END is_deelzaak

,  hz.OLO_DOSSIERNUMMER as olo_nummer
,  z.extern_zaaknummer as extern_zaaknummer

,  z.globale_locatie_aanduiding as globale_locatie

-- ,  z.zaak_status as zaak_status_code
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

,  z.omschrijving as omschrijving
,  z.toelichting as toelichting
,  r.omschrijving as zaak_resultaat

-- ,  n.onderwerp as notitie_onderwerp
-- ,  n.tekst as notitie_tekst
-- ,  n.medewerker as notitie_opsteller
-- ,  n.datum as notitie_datum 

,  zp.naam as zaaktype_naam

,  f.omschrijving as zaak_fase_omschrijving

-- , 'bouwgegevens' as div4
-- , bg.*


from 
   zaak z
   left join deelzaak dz1 on z.id=dz1.id
   left join deelzaak dz2 on z.id=dz2.hoofdzaak_id
   left join hoofdzaak hz on z.id=hz.id

   left join zaaktype_parent zp on z.zaaktype_id = zp.id
   left join resultaat r on z.zaak_resultaat_id = r.id
   left join fase f on z.fase_id = f.id
--   left join vw_g_notities n on z.id = n.zaak_id
--   left join vw_g_onderdeel_bouw bg on z.id=bg.hoofdzaak_id

where 0=0

order by 
   z.aanvraagnummer_string
,  z.startdatum