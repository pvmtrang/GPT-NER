@echo off

set "OPENAI_API_KEY=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"

SET "MRCDIR=data\conll_mrc"
SET "MRCNAME=test.100"
SET "GPTDIR=data\conll_mrc\100-results"
rem SET "GPTNAME=openai.32.knn.sequence.fullprompt"
SET "GPTNAME=tmp.test"
SET "DATANAME=CONLL"
SET "WRITEDIR=data\conll_mrc\100-results"
SET "WRITENAME=openai.32.knn.sequence.fullprompt.verified"
python "%CD%\openai_access\verify_results.py" "--mrc-dir" "%MRCDIR%" "--mrc-name" "%MRCNAME%" "--gpt-dir" "%GPTDIR%" "--gpt-name" "%GPTNAME%" "--data-name" "%DATANAME%" "--write-dir" "%WRITEDIR%" "--write-name" "%WRITENAME%"