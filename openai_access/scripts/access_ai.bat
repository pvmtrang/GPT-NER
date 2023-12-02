@echo off

set "OPENAI_API_KEY=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"

@REM SET "SOURCEDIR=data\conll_mrc"
@REM SET "SOURCENAME=test.100"
@REM SET "DATANAME=CONLL"
@REM SET "EXAMPLEDIR=data\conll_mrc"
@REM SET "EXAMPLENAME=test.100.simcse.32"
@REM SET "EXAMPLENUM=8"
@REM SET "WRITEDIR=data\conll_mrc\100-results"
@REM SET "WRITENAME=tmp.test"
@REM SET "TRAINNAME=train"

SET "SOURCEDIR=data\phoNER_COVID19"
SET "SOURCENAME=test_1x10_converted_2"
SET "DATANAME=phoNER_COVID19_vie"
SET "EXAMPLEDIR=data\phoNER_COVID19"
SET "EXAMPLENAME=test_500_simcse_10"
SET "EXAMPLENUM=5"
SET "WRITEDIR=data\phoNER_COVID19\results"
SET "WRITENAME=fullprompt.test_1_vie_2"
SET "TRAINNAME=train_converted"

rem read SOURCEDIR\\mrc-ner.TRAINNAME to be train dataset
rem SOURCEDIR\\mrc-ner.SOURCENAME to be test dataset
rem EXAMPLEDIR\\EXAMPLENAME.knn,jsonl is the name of file store embedding of all context of each label

python "%CD%\openai_access\get_results_mrc_knn.py" "--source-dir" "%SOURCEDIR%" "--source-name" "%SOURCENAME%" "--data-name" "%DATANAME%" "--example-dir" "%EXAMPLEDIR%" "--example-name" "%EXAMPLENAME%" "--example-num" "%EXAMPLENUM%" "--train-name" "%TRAINNAME%" "--write-dir" "%WRITEDIR%" "--write-name" "%WRITENAME%"