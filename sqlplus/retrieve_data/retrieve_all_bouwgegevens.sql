/*# =============================================================================
  #
  # @package    stn_sxo_uitzetten
  # @container  retrieve_data
  # @name       retrieve_all_bouwgegegevens.sql
  # @purpose    SQL statements to retrieve bouw information
  # @version    v0.0.2  2024-06-04
  # @author     pierre@amultis.dev
  # @copyright  (C) 2020-2024 Pierre Veelen
  #
  # =============================================================================
*/
SELECT 
  z.AANVRAAGNUMMER_STRING AS squitxo_zaaknummer
, z.EXTERN_ZAAKNUMMER AS EXTERN_NUMMER
, bw.*
FROM VW_G_BOUW_UNION bw
LEFT JOIN ZAAK z ON bw.ZAAK_ID = z.id 
order by 
   z.aanvraagnummer_string
--,  z.startdatum