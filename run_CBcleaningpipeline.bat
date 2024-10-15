@echo off
python "C:\Users\Public\Documents\ChargeBreakdownPipeline\chargebreakdowncleaning.py" > "C:\Users\Public\Documents\ChargeBreakdownPipeline\Cleaningpipelinelogs\cleanup1.log" 2>&1
python "C:\Users\Public\Documents\ChargeBreakdownPipeline\chargebreakdowncleaningtwo.py" > "C:\Users\Public\Documents\ChargeBreakdownPipeline\Cleaningpipelinelogs\cleanup2.log" 2>&1
python "C:\Users\Public\Documents\ChargeBreakdownPipeline\findsame_cb.py" > "C:\Users\Public\Documents\ChargeBreakdownPipeline\Cleaningpipelinelogs\cleanup3.log" 2>&1
python "C:\Users\Public\Documents\ChargeBreakdownPipeline\sqlconnect.py" > "C:\Users\Public\Documents\ChargeBreakdownPipeline\Cleaningpipelinelogs\DB_Connect.log" 2>&1