#!/bin/bash

echo "<odoo><data>"

while read line
do
    name=$(echo $line | cut -d',' -f1)
    surname=$(echo $line | cut -d',' -f2)
    dni=$(echo $line | cut -d',' -f3)
    email=$(echo $line | cut -d',' -f4)
    echo "<record id='developer$dni' model='devmeet.developer'>"
    echo "<field name='name'>$name</field>"
    echo "<field name='surname'>$surname</field>"
    echo "<field name='dni'>$dni</field>"
    echo "<field name='email'>$email</field>"
    echo "<field name='events_assistant' eval='[(6,0,[ref("'"devmeet.event1"'")])]'></field>"
    echo "<field name='technologies_known' eval='[(6,0,[ref("'"devmeet.technology1"'")])]'></field>"
    echo "<field name='photo'>$(base64 developer.png)</field>"
    echo "</record>"
done
echo "</data></odoo>"