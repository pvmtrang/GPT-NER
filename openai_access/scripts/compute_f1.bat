@echo off

SET "REF=data/phoNER_COVID19/mrc-ner.test_1x10_converted_2"
@REM SET "REF=data\conll_mrc\mrc-ner.test.100"
rem SET "PRE=data\conll_mrc\100-results\openai.32.knn.sequence.fullprompt.verified"
@REM SET "PRE=data\conll_mrc\100-results\tmp.test"
SET "PRE=data\phoNER_COVID19\results\fullprompt.test_1_eng"
echo "compute results of access_ai.bat"
python "%CD%\openai_access\compute_f1.py" "--candidate-file" "%PRE%" "--reference-file" "%REF%"