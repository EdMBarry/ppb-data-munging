#!/bin/sh

#firstly copy the data to a new dataset. The raw data is in a sub-repo of this one
cp -r rawIRR mungeIRR

cd mungeIRR

sed -i 's/  /,/g' *.IRR
sed -i 's/ //g' *.IRR
