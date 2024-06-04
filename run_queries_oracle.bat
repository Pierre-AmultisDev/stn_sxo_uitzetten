::# =============================================================================
::#
::# @package    stn_sxo_uitzetten
::# @container  retrieve_data
::# @name       run_queries_oracle.bat
::# @purpose    batch files to start exe
::# @version    v0.0.2  2024-06-04
::# @author     pierre@amultis.dev
::# @copyright  (C) 2020-2024 Pierre Veelen
::#
::# =============================================================================
@echo off

:: BASIC SETTINGS
:: ==============
:: Setting the name of the script
SET ME=%~n0
:: Setting the name of the directory
SET PARENT=%~p0
SET PDRIVE=%~d0
:: Setting the directory and drive of this commandfile
SET "CMD_DIR=%~dp0"

REM https://stackoverflow.com/questions/15478002/how-do-i-call-concat-variable-when-the-variable-has-internal-spaces
SET "baselinepath=%CD%"
SET "thisappname=run_queries_oracle"

echo [%ME%] [INFO   ] START at %date% %time% ... >"%baselinepath%\%thisappname%_runlog.txt"
echo [%ME%] [INFO   ] BY %username% ... >>"%baselinepath%\%thisappname%_runlog.txt"

echo [%ME%] [INFO   ] START at %date% %time% ... >"%baselinepath%\%thisappname%_errlog.txt"
echo [%ME%] [INFO   ] BY %username% ... >>"%baselinepath%\%thisappname%_errlog.txt"

echo [%ME%] [DEBUG  ] START at %date% %time% ... >"%baselinepath%\%thisappname%_dbglog.txt"
echo [%ME%] [DEBUG  ] BY %username% ... >>"%baselinepath%\%thisappname%_dbglog.txt"

echo [%ME%] [INFO   ] %baselinepath% >>"%baselinepath%\%thisappname%_runlog.txt"
echo [%ME%] [INFO   ] %baselinepath%\%thisappname%.exe >>"%baselinepath%\%thisappname%_runlog.txt"

echo [%ME%] [DEBUG  ] %CD% >"%baselinepath_SUB%\%thisappname_SUB%_dbglog.txt"
echo [%ME%] [DEBUG  ] dir /s >>"%baselinepath_SUB%\%thisappname_SUB%_dbglog.txt"

"%baselinepath%\%thisappname%.exe" 1>>"%baselinepath%\%thisappname%_runlog.txt" 2>>"%baselinepath%\%thisappname%_errlog.txt"

echo [%ME%] [INFO   ] STOP at %date% %time% ... >>"%baselinepath%\%thisappname%_runlog.txt"
echo [%ME%] [INFO   ] STOP at %date% %time% ... >>"%baselinepath%\%thisappname%_errlog.txt"
echo [%ME%] [DEBUG  ] STOP at %date% %time% ... >>"%baselinepath%\%thisappname%_dbglog.txt"
