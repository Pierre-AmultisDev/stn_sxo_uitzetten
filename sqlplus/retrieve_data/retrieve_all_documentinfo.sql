/*
 * Versie voor SquitXO
 * ======================
 * Datum:    20240715
 * Versie:   002
 * Bestand:  retreive_all_documentinfo.sql
 * Auteur:   Pierre Veelen
 *
 * Function: Levert een table die gegevens van de documenten in de lokale DMS van SquitXO
 *
 * ToDo: 
 *
 */
SELECT 
  z.aanvraagnummer_string AS squitxo_zaaknummer
, z.extern_zaaknummer AS extern_zaaknummer
, d.*
FROM csv_document d
LEFT JOIN zaak z ON d.zaak_id=z.id
