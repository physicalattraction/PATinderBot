from typing import Dict

import requests

from secrets import TINDER_ACCESS_TOKEN, TINDER_PHONE_NUMBER, TINDER_REFRESH_TOKEN, TINDER_USER_ID, get_from_secrets, \
    set_in_secrets

# TODO: Unify with syntax in TinderService
CODE_REQUEST_URL = "https://api.gotinder.com/v2/auth/sms/send?auth_type=sms"
CODE_VALIDATE_URL = "https://api.gotinder.com/v2/auth/sms/validate?auth_type=sms"
TOKEN_URL = "https://api.gotinder.com/v2/auth/login/sms"

HEADERS = {'user-agent': 'Tinder/11.4.0 (iPhone; iOS 12.4.1; Scale/2.00)'}


class TinderAuthenticator:
    def set_new_tokens(self):
        """
        Set Tinder user ID and auth tokens in secrets file

        Note: this requires user interaction
        """

        phone_number = get_from_secrets(TINDER_PHONE_NUMBER)
        self._send_otp_code(phone_number)
        otp_code = input('Please enter the code you have received by SMS: ')
        refresh_token = self._get_refresh_token(otp_code, phone_number)
        access_token = self._get_access_token(refresh_token)
        set_in_secrets(TINDER_USER_ID, access_token['_id'])
        set_in_secrets(TINDER_ACCESS_TOKEN, access_token['api_token'])
        set_in_secrets(TINDER_REFRESH_TOKEN, access_token['refresh_token'])

    def _send_otp_code(self, phone_number: str):
        """
        Let Tinder send a one time password to your phone

        :param phone_number: Phone number to send the otp to
        """

        response = requests.post(CODE_REQUEST_URL, headers=HEADERS, json={'phone_number': phone_number})
        assert response.ok, response.text
        data = response.json()['data']
        assert data['sms_sent'] is True, response.json()

    def _get_refresh_token(self, otp_code: str, phone_number: str) -> str:
        """
        Obtain a refresh token using the one time password that Tinder sent

        :param otp_code: One time password sent by Tinder to your phone
        :param phone_number: Phone number used
        :return: Refresh token
        """

        response = requests.post(CODE_VALIDATE_URL, headers=HEADERS,
                                 json={'otp_code': otp_code, 'phone_number': phone_number})
        assert response.ok, response.text
        data = response.json()['data']
        assert data['validated'] is True, response.json()
        print(data)
        return data['refresh_token']

    def _get_access_token(self, refresh_token: str) -> Dict[str, str]:
        """
        Use the refresh token to obtain a new access token

        :param refresh_token: Tinder refresh token, obtained from SMS verification
        :return: Dictionary in the following format:
        {
            '_id': 'XXX',  # Tinder user ID
            'api_token': 'XXX',  # Tinder access token, in uuid format
            'refresh_token': 'XXX',  # Tinder refresh token, in jwt format
            'is_new_user': False
        }
        """

        response = requests.post(TOKEN_URL, headers=HEADERS, json={'refresh_token': refresh_token})
        assert response.ok, response.text
        data = response.json()['data']
        print(data)
        return data


if __name__ == '__main__':
    authenticator = TinderAuthenticator()
    authenticator.set_new_tokens()
