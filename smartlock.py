from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

import datetime
from time import strftime
import random
from threading import *
import time
import subprocess

import RPi.GPIO as GPIO

# ---------------------------------------------------------------------------


token_timer = 10
tokens_list = []
list_has_tokens = False
# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

# The ID and range of a sample spreadsheet.
SAMPLE_SPREADSHEET_ID = '1fC6ejV3bEvGc5T0h0lZTUbARf5WzWby_fa0Y7XyCUP8'
sheet_range = 'Membership Current!L:L'

# value_input_option = 'USER_ENTERED'
value_input_option = 'RAW'


# --------------------------------------------------------------------------


def read_rfid():
    global tokens_list

    while True:
        try:
            output = subprocess.Popen(["nfc-list"], stdout=subprocess.PIPE).communicate()[0]

            output = str(output)
            uids = output.count("UID")
            if uids == 1:
                data = output.split(':')

                uid = data[5].lstrip()
                # print("uid is {}".format(uid))

                filtered_uid = uid.split('SAK')
                # print("filtered uid is {}".format(filtered_uid))

                uid = filtered_uid[0].lstrip()
                # print("uid is {}".format(uid))

                card_uid = uid.split('\n')

                print("card_uid is {}".format(card_uid[0]))

                tag = card_uid[0]

                if list_has_tokens:
                    print(len(tokens_list))

                    for i in range(len(tokens_list)):

                        print(tokens_list[i])
                        if tokens_list[i]:

                            if tag == tokens_list[i][0]:
                                print("User found in Database.")

				print ("GPIO mode set to BCM")
				GPIO.setmode(GPIO.BCM)
				print ("GPIO 21 set to OUTPUT")
				GPIO.setup(21, GPIO.OUT)
				print ("GPIO 21 set to LOW")
				GPIO.output(21, GPIO.LOW)
				print("Access granted for 5 seconds")
				time.sleep(5)
				print ("GPIO cleanup")
				GPIO.cleanup()

                                break

                            else:
                                print("User not found at entry {}".format(i + 1))
                else:
                    print("Please wait for list to be updated")
            else:
                print("No Token found on the reader...")

        except:
            pass


# ------------------------------------------------------------------------


def get_valid_tokens(service):
    global tokens_list
    global list_has_tokens
    # Call the Sheets API
    while True:
        # time.sleep(1)
        for i in range(token_timer, -1, -1):
            mins, secs = divmod(i, 60)
            # print ("Time to retrieve list is {},{}".format(mins, secs))
            time.sleep(1)
            if mins == 0 and secs == 0:
                sheet = service.spreadsheets()
                result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID, range=sheet_range).execute()

                values = result.get('values', [])

                if not values:
                    print('No data found.')

                else:
                    # tokens_list = values
                    tokens_list = []
                    for x in range(len(values) - 1):
                        # print (values[0])
                        tokens_list.append(values[x + 1])

                    print("New Validated token are {}".format(tokens_list))
                    list_has_tokens = True
                    # tokens_list = []
                    # for row in values:
                    #     tokens_list.append(row)
                    #
                    # print ("New Validated token are {}".format(tokens_list))


# --------------------------------------------------------


def main():
    """Shows basic usage of the Sheets API.
    Prints values from a sample spreadsheet.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)

    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'client_secret.json', SCOPES)
            creds = flow.run_local_server()
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('sheets', 'v4', credentials=creds)

    # ---------------------------------------------------------------------------------

    t1 = Thread(target=get_valid_tokens, args=(service,))
    t1.daemon = True
    t1.start()

    t2 = Thread(target=read_rfid)
    t2.daemon = True
    t2.start()

    while True:
        time.sleep(1)

    # print('{0} cells updated.'.format(result.get('updatedCells')))


if __name__ == '__main__':
    main()
