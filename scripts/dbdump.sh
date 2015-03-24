#!/bin/bash
rm /tmp/conceptmapping/cm_data.csv
mysql -u root -p -e "select id, 
email, 
firstname, 
lastname, 
\`condition\`, 
alternative_use, alternative_use_time, 
doc_1, doc_1_time, 
doc_2, doc_2_time, 
proto_1, proto_1_time, 
proto_2, proto_2_time, 
cd_training_time, tool_training_time, proto_training_time
INTO OUTFILE '/tmp/conceptmapping/cm_data.csv' 
FIELDS TERMINATED BY '<A5T$>' ESCAPED BY '' 
LINES TERMINATED BY '<A5T^>' 
from problem_formulator.users;"
