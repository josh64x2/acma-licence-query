# ACMA Registration checker #

This small script will submit a request to the ACMA licence search website
and parse the response to try and determine if the specified callsign has been
registered yet or not.

Please don't be silly and have this script set to run extremely frequently.



## Usage: ##
*Before* use create your own `acma.conf` file using `acma.conf.example` as a starting point.
`python3 acma.py callsign` where `callsign` is the VK callsign you want to query.
