@echo off

@REM below is the wrong private openai key of mine
set OPENAI_API_KEY="sk-YdbCl7kNwUqNqopI1Ki3T3BlbkFJpHJiMzwIU3EH3xDVlzj1aVA6"

SET "SOURCEDIR=data\conll_mrc"
SET "SOURCENAME=test.100"
SET "DATANAME=CONLL"
SET "EXAMPLEDIR=data\conll_mrc"
SET "EXAMPLENAME=test.100.simcse.32"
SET "EXAMPLENUM=8"
SET "WRITEDIR=data\conll_mrc\100-results"
SET "WRITENAME=tmp.test"
SET "TRAINNAME=train"

python "%CD%\openai_access\get_results_mrc_knn.py" "--source-dir" "%SOURCEDIR%" "--source-name" "%SOURCENAME%" "--data-name" "%DATANAME%" "--example-dir" "%EXAMPLEDIR%" "--example-name" "%EXAMPLENAME%" "--example-num" "%EXAMPLENUM%" "--train-name" "%TRAINNAME%" "--write-dir" "%WRITEDIR%" "--write-name" "%WRITENAME%"