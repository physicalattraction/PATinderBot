from typing import Dict

import requests

from secrets import TINDER_ACCESS_TOKEN, TINDER_PHONE_NUMBER, TINDER_REFRESH_TOKEN, TINDER_USER_ID, get_from_secrets, \
    set_in_secrets


class TinderAuthenticator:
    """
    Class responsible to make sure the authentication with Tinder is working

    Documented APIs: https://github.com/fbessez/Tinder
    """

    base_url = 'https://api.gotinder.com'
    headers = {'User-Agent': 'Tinder/11.4.0 (iPhone; iOS 12.4.1; Scale/2.00)',
               'content-type': 'application/json'}

    def ensure_authentication(self):
        """
        Set Tinder user ID and auth tokens in secrets file

        We always assume that the current access token is not valid anymore. It is cheap to get a new token anyway.
        We assume however that the refresh token is valid. If it turns out to be invalid, this functionality
        requires user interaction (entering the OTP from the phone)
        """

        # Set the user ID and access token at the start of the function.
        # If all goes well, they are set correctly at the end of this function.
        # If something unexpected happens, the user ID and access token that were present are unreliable.
        set_in_secrets(TINDER_USER_ID, None)
        set_in_secrets(TINDER_ACCESS_TOKEN, None)

        # If there is a refresh token, assume it is valid.
        # If it turns out to be not valid (anymore), we discard it later and try again.
        refresh_token = get_from_secrets(TINDER_REFRESH_TOKEN)
        if not refresh_token:
            phone_number = get_from_secrets(TINDER_PHONE_NUMBER)
            self._send_otp_code(phone_number)
            otp_code = input('Please enter the code you have received by SMS: ')
            refresh_token = self._get_refresh_token(otp_code, phone_number)

        # If the refresh token is not valid, we discard it and try again from scratch
        try:
            access_token = self._get_access_token(refresh_token)
        except PermissionError:
            set_in_secrets(TINDER_REFRESH_TOKEN, None)
            return self.ensure_authentication()

        set_in_secrets(TINDER_USER_ID, access_token['_id'])
        set_in_secrets(TINDER_ACCESS_TOKEN, access_token['api_token'])
        set_in_secrets(TINDER_REFRESH_TOKEN, access_token['refresh_token'])

    def _send_otp_code(self, phone_number: str):
        """
        Let Tinder send a one time password to your phone

        :param phone_number: Phone number to send the otp to
        """

        url = f'{self.base_url}/v2/auth/sms/send'
        response = requests.post(url, headers=self.headers, params={'auth_type': 'sms'},
                                 json={'phone_number': phone_number})
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

        url = f'{self.base_url}/v2/auth/sms/validate'
        response = requests.post(url, headers=self.headers, params={'auth_type': 'sms'},
                                 json={'otp_code': otp_code, 'phone_number': phone_number})
        assert response.ok, response.text
        data = response.json()['data']
        assert data['validated'] is True, response.json()
        return data['refresh_token']

    def _get_access_token(self, refresh_token: str) -> Dict[str, str]:
        """
        Use the refresh token to obtain a new access token

        If the refresh token is not valid, we discard it and raise a PermissionError

        :param refresh_token: Tinder refresh token, obtained from SMS verification
        :return: Dictionary in the following format:
        {
            '_id': 'XXX',  # Tinder user ID
            'api_token': 'XXX',  # Tinder access token, in uuid format
            'refresh_token': 'XXX',  # Tinder refresh token, in jwt format
            'is_new_user': False
        }
        """

        url = f'{self.base_url}/v2/auth/login/sms'
        response = requests.post(url, headers=self.headers, json={'refresh_token': refresh_token})
        if response.status_code in (401, 403):
            raise PermissionError()
        assert response.ok, response.text
        data = response.json()['data']
        return data


if __name__ == '__main__':
    authenticator = TinderAuthenticator()
    authenticator.ensure_authentication()
