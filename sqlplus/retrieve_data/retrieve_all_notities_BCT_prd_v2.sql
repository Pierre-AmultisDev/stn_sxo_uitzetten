/*
 * Versie voor SquitXO
 * ======================
 * Datum:    20241007
 * Versie:   006
 * Bestand:  retreive_all_notities_BCT_prd_v2.sql
 * Auteur:   Pierre Veelen
 *
 * Function: Levert een table die gegevens van de notities bij zaken van SquitXO
 *
 * ToDo: 
 *
 */
SELECT DISTINCT

-- /* 
--  * Info t.b.v. beoordeling door Tessie en Bianca
--  *
--  */

--   TO_CHAR(EXTRACT(YEAR FROM z.startdatum)) as zaak_startjaar 
-- , z.startdatum as zaak_startdatum
-- , TO_CHAR(EXTRACT(YEAR FROM z.einddatum)) as zaak_eindjaar
-- , z.einddatum as zaak_einddatum
-- , r.omschrijving as zaak_resultaat
-- , zp.naam as zaaktype_naam
  zp.naam as zaaktype_naam

/*
 * Bepalen van mogelijke varianten van SquitXO zaaknummers in Corsa
 *
 */
-- ALS(LINKS(X2;2)="20";"B"&LINKS(X2;4)&"-"&RECHTS(X2;3);"")
-- Kan voorkomen als dossier verwerkt is. Dan is SquitXO nummer handmatig vervangen
-- 20070002 => B2007-002 
, CASE
 	WHEN SUBSTR(z.AANVRAAGNUMMER_STRING,1,2) = '20'
	   THEN 'B' || SUBSTR(z.AANVRAAGNUMMER_STRING,1,4) || '-' || SUBSTR(z.AANVRAAGNUMMER_STRING,-3,3)
	   ELSE ''
  END SQUITXO_ZAAKNUMMER_AANGEPAST_B
  
-- ALS(LINKS(X2;2)="20";"B"&LINKS(X2;4)&"-"&RECHTS(X2;3)&".";"")
-- Kan voorkomen als dossier verwerkt is. Dan is SquitXO nummer handmatig vervangen
-- 20070002 => B2007-002.
, CASE
	WHEN SUBSTR(z.AANVRAAGNUMMER_STRING,1,2) = '20'
	   THEN 'B' || SUBSTR(z.AANVRAAGNUMMER_STRING,1,4) || '-' || SUBSTR(z.AANVRAAGNUMMER_STRING,-3,3) || '.'
	   ELSE ''
  END SQUITXO_ZAAKNUMMER_AANGEPAST_B_PUNT

-- ALS(EN(LINKS(X2;2)="20";DEEL(X2;5;1)="2");"S"&LINKS(X22;4)&"-"&RECHTS(X22;3);"")
-- Kan voorkomen als dossier verwerkt is. Dan is SquitXO nummer handmatig vervangen
-- 20072002 => S2007-002
, CASE
	WHEN (SUBSTR(z.AANVRAAGNUMMER_STRING,1,2) = '20') AND (SUBSTR(z.AANVRAAGNUMMER_STRING,5,1) = '2')
	   THEN 'S' || SUBSTR(z.AANVRAAGNUMMER_STRING,1,4) || '-' || SUBSTR(z.AANVRAAGNUMMER_STRING,-3,3)
	   ELSE ''
  END SQUITXO_ZAAKNUMMER_AANGEPAST_S

-- , 'formule' as EXTERN_ZAAKNUMMER_IN_CORSA_KING_MAIK
-- , 'formule' as EXTERN_ZAAKNUMMER_IN_CORSA_KING_TESSIE
-- , 'formule' as EXTERN_ZAAKNUMMER_IN_CORSA_DOSSIERCODE_TESSIE
-- , 'formule' as SQUITXO_ZAAKNUMMER_IN_CORSA_KING_MAIK
-- , 'formule' as SQUITXO_ZAAKNUMMER_IN_CORSA_KING_TESSIE
-- , 'formule' as SQUITXO_ZAAKNUMMER_IN_CORSA_DOSSIERCODE_TESSIE
-- , 'formule' as SQUITXO_ZAAKNUMMER_B_IN_CORSA_KING_MAIK
-- , 'formule' as SQUITXO_ZAAKNUMMER_B_IN_CORSA_KING_TESSIE
-- , 'formule' as SQUITXO_ZAAKNUMMER_B_IN_CORSA_DOSSIERCODE_TESSIE
-- , 'formule' as SQUITXO_ZAAKNUMMER_B_PUNT_IN_CORSA_KING_MAIK
-- , 'formule' as SQUITXO_ZAAKNUMMER_B_PUNT_IN_CORSA_KING_TESSIE
-- , 'formule' as SQUITXO_ZAAKNUMMER_B_PUNT_IN_CORSA_DOSSIERCODE_TESSIE
-- , 'formule' as SQUITXO_ZAAKNUMMER_S_IN_CORSA_KING_MAIK
-- , 'formule' as SQUITXO_ZAAKNUMMER_S_IN_CORSA_KING_TESSIE
-- , 'formule' as SQUITXO_ZAAKNUMMER_S_IN_CORSA_DOSSIERCODE_TESSIE
-- , 'formule' as KOMT_VOOR_IN_CORSA
-- , '' as LEEG -- hiermee wordt extra kolom gemaakt zodat alle Excel formules blijven werken. Bij documenten is deze kolom nl wel gevuld met een Excel formule
-- , 'PDF' as pdf_splits

/* 
 * Vanaf hier staat de zaakinfo die in pdf documenten moeten komen
 *
 */
 

, CASE -- als zaakid een deelzaak is vul dan hoofdzaak id in. Anders eigen zaak id
	WHEN dz.hoofdzaak_id is not NULL
      THEN -- dit is een deelzaak kies hoofdzaak id
	    (SELECT aanvraagnummer_string FROM zaak WHERE zaak.id = dz.hoofdzaak_id)
      ELSE -- dit is geen deelzaak kies het eigen zaak id
	    (SELECT aanvraagnummer_string FROM zaak WHERE zaak.id = z.id)	  
   END squitxo_hoofdzaaknummer
, z.AANVRAAGNUMMER_STRING AS SQUITXO_ZAAKNUMMER
, z.EXTERN_ZAAKNUMMER AS EXTERN_ZAAKNUMMER
, z.OMSCHRIJVING as OMSCHRIJVING
, z.GLOBALE_LOCATIE_AANDUIDING as GLOBALE_LOCATIE
--   z.id AS zaakid
,  n.onderwerp as notitie_onderwerp
,  n.tekst as notitie_tekst
,  n.medewerker as notitie_opsteller
,  n.datum as notitie_datum 

from 
   zaak z
   left join deelzaak dz on z.id=dz.id
   left join vw_g_notities n on z.id = n.zaak_id
   join vw_deelzaak_hoofdzaak dh ON dh.hoofdzaakid=z.id 
   left join zaaktype_parent zp on z.zaaktype_id = zp.id
   left join resultaat r on z.zaak_resultaat_id = r.id

where 0=0
AND (n.onderwerp is not null OR n.tekst is not null OR n.medewerker is not null OR n.datum is not null)

ORDER BY 
   z.AANVRAAGNUMMER_STRING
