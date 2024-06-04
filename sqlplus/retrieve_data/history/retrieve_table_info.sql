/*
 * Versie voor Rx.Mission
 * ======================
 * Datum:    20240328
 * Bestand:  retrieve_table_info.sql
 * Auteur:   Pierre Veelen
 * 
 * ToDo: 
 * 
 * 
 */
SELECT TABLE_NAME, COLUMN_NAME, DATA_TYPE, DATA_LENGTH
FROM USER_TAB_COLUMNS
WHERE TABLE_NAME = 'ZAAK'
