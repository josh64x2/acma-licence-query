#!/usr/bin/env python3
# Query the ACMA licence database for callsign registration and send an
# email notification
import argparse, smtplib, configparser
from urllib.parse import urlencode
from urllib.request import urlopen
from email.mime.text import MIMEText

def _send_mail_for_callsign(callsign):
    """
    Send the email notification
    """
    config = configparser.ConfigParser()
    config.read('acma.conf')

    msg = MIMEText("Registered: " + callsign)
    msg['Subject'] = 'Callsign registered'
    msg['From'] = config['email']['from_name'] + ' <' + config['email']['from_address'] + '>'
    msg['To'] = config['email']['to_name'] + ' <' + config['email']['to_address'] + '>'

    # TODO: Handle config['smtp']['ssl_required'] == 'yes'
    s = smtplib.SMTP(config['smtp']['server'])
    if config['smtp']['auth_required'] == 'yes':
        s.login(config['smtp']['username'], config['smtp']['password'])

    s.send_message(msg)
    s.quit()

def _not_registered():
    """
    Handle a not registered response
    """
    print("Not registered :(")

def _registered(callsign):
    """
    Handle the account being registered
    """
    print("Registered!")
    _send_mail_for_callsign(callsign)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("callsign")
    args = parser.parse_args()
    callsign = args.callsign

    print("Checking: " + callsign)

    acma_search_url = ('http://web.acma.gov.au/pls/radcom/register_search.search_dispatcher')
    form_data = {'pSEARCH_TYPE':'Licences', 'pSUB_TYPE':'Callsign', 'pEXACT_IND':'matches', 'pQRY':callsign,'SUBMIT':'Go'}
    encoded_data = urlencode(form_data).encode('utf-8')
    try:
        f = urlopen(acma_search_url, encoded_data)
        result = f.read()
    finally:
        f.close()

    # process result
    result_string = result.decode('utf-8')
    if "No matches were found for your query" in result_string:
        _not_registered()
    elif callsign.upper() + "</td>" in result_string:
        _registered(callsign)
    else:
        print("Unexpected search result")
