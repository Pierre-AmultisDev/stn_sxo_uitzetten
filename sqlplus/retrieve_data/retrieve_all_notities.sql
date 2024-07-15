/*
 * Versie voor SquitXO
 * ======================
 * Datum:    20240715
 * Versie:   002
 * Bestand:  retreive_all_notities.sql
 * Auteur:   Pierre Veelen
 *
 * Function: Levert een table die gegevens van de notities bij zaken van SquitXO
 *
 * ToDo: 
 *
 */
select distinct

   z.id AS zaakid
,  CASE -- als zaakid een deelzaak is vul dan hoofdzaak id in. Anders eigen zaak id
	  WHEN dz.hoofdzaak_id is not NULL
        THEN dz.hoofdzaak_id -- dit is een deelzaak kies hoofdzaak id
        ELSE z.id -- dit is geen deelzaak kies het eigen zaak id
    END hoofdzaakid

,  z.aanvraagnummer_string as squitxo_zaaknummer

,  z.extern_zaaknummer as extern_zaaknummer

,  CASE -- als zaakid een deelzaak is vul dan hoofdzaak sxo nummer in. Anders verklarende tekst
	  WHEN dz.hoofdzaak_id is not NULL
        THEN z.AANVRAAGNUMMER_STRING -- dit is een deelzaak kies hoofdzaak sxo nummer
        ELSE 'dit is een hoofdzaak' -- dit is geen deelzaak kies het eigen zaak id
    END squitxo_hoofdzaaknummer

,  z.globale_locatie_aanduiding as globale_locatie

,  z.omschrijving as omschrijving

,  n.onderwerp as notitie_onderwerp
,  n.tekst as notitie_tekst
,  n.medewerker as notitie_opsteller
,  n.datum as notitie_datum 

from 
   zaak z
   left join deelzaak dz on z.id=dz.id
   left join vw_g_notities n on z.id = n.zaak_id
   join vw_deelzaak_hoofdzaak dh ON dh.hoofdzaakid=z.id 

where 0=0
AND (n.onderwerp is not null OR n.tekst is not null OR n.medewerker is not null OR n.datum is not null)

order by 
   z.aanvraagnummer_string
