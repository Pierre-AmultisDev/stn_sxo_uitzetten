SELECT 
  z.AANVRAAGNUMMER_STRING AS SQUITXO_ZAAKNUMMER
, z.EXTERN_ZAAKNUMMER AS EXTERN_NUMMER
, z.OMSCHRIJVING as OMSCHRIJVING
, z.GLOBALE_LOCATIE_AANDUIDING as GLOBALE_LOCATIE
--, bw.ZAAK_ID
, bw.OUDE_OPPERVLAKTE
, bw.NIEUWE_OPPERVLAKTE
, bw.OUDE_INHOUD
, bw.NIEUWE_INHOUD
-- , bw.AANTAL_BOUWWERKEN
-- , bw.BOUWTIJD
, bw.VASTGESTELDE_KOSTEN
, bw.VASTGESTELDE_KOSTEN_INC
, bw.BOUWKOSTEN
, bw.BOUWKOSTEN_INC
, bw.GEWIJZIGDE_KOSTEN
, bw.GEWIJZIGDE_KOSTEN_INC
-- , bw.DATUM_VOORLOPIG_BOUW
, bw.DATUM_GEREEDMELDING
-- , bw.DATUM_VOLTOOIING
, bw.DATUM_START_BOUW
-- , bw.BOUWACTIVITEIT_CODE
, bw.BOUWACTIVITEIT_OMSCHRIJVING
-- , bw.BOUWWERKTYPE_CODE
, bw.BOUWWERKTYPE_OMSCHRIJVING
FROM VW_G_BOUW_UNION bw
LEFT JOIN ZAAK z ON bw.ZAAK_ID = z.ID 
ORDER BY 
   z.AANVRAAGNUMMER_STRING
--,  z.startdatum