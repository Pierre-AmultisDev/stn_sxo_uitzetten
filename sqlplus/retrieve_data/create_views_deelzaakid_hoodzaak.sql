/*
 * Versie voor SquitXO
 * ======================
 * Datum:    20240715
 * Versie:   001
 * Bestand:  create_views_deelzaakid_hoodzaak.sql
 * Auteur:   Pierre Veelen
 *
 * Function: Creert een aantal hulp views t.b.v. SquitXO. 
 *           Moet worden uitgevoerd voordat andere queries worden uitgevoerd.
 *
 * ToDo: 
 *
 */
DROP VIEW vw_deelzaak_hoofdzaak
;

CREATE VIEW vw_deelzaak_hoofdzaak AS
select distinct

  CASE -- als zaakid een deelzaak is vul dan hoofdzaak id in. Anders eigen zaak id
	   WHEN dz.hoofdzaak_id is not NULL
        THEN dz.hoofdzaak_id -- dit is een deelzaak kies hoofdzaak id
        ELSE z.id -- dit is geen deelzaak kies het eigen zaak id
     END hoofdzaakid

,  z.id AS deelzaakid

--,  z.aanvraagnummer_string as squitxo_zaaknummer

--,  z.extern_zaaknummer as extern_zaaknummer

--,  CASE -- als zaakid een deelzaak is vul dan hoofdzaak sxo nummer in. Anders verklarende tekst
--	   WHEN dz.hoofdzaak_id is not NULL
--        THEN 'hoofdzaaknummer nog maken' -- dit is een deelzaak kies hoofdzaak sxo nummer
--        ELSE 'dit is een hoofdzaak' -- dit is geen deelzaak kies het eigen zaak id
--     END squitxo_hoofdzaaknummer

from 
   zaak z
   left join deelzaak dz on z.id=dz.id
;

DROP VIEW vw_final_hz_dz
;

CREATE VIEW vw_final_hz_dz AS
SELECT 
  hzdz.DEELZAAKID
, z.AANVRAAGNUMMER_STRING AS SQUITXO_HOOFDZAAKNUMMER
FROM vw_deelzaak_hoofdzaak hzdz
LEFT JOIN zaak z ON hzdz.HOOFDZAAKID=z.id
WHERE HOOFDZAAKID!=DEELZAAKID
;

SELECT * FROM vw_final_hz_dz