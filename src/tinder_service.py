import json
from typing import Any, Dict, Iterator, List, Union

import requests

from secrets import TINDER_ACCESS_TOKEN, TINDER_USER_ID, get_from_secrets
from tinder_authenticator import TinderAuthenticator
from tinder_user import TinderUser, TinderUserDict

OptionalJSON = Union[List, Dict, float, int, str, bool, None]


class TinderService:
    """
    Class responsible to make API calls to Tinder

    Documented APIs: https://github.com/fbessez/Tinder
    """

    base_url = 'https://api.gotinder.com'

    def __init__(self):
        if not get_from_secrets(TINDER_ACCESS_TOKEN):
            self._update_tinder_tokens()

    @property
    def headers(self) -> Dict[str, Any]:
        return {
            'app_version': '3',
            'platform': 'ios',
            'X-Auth-Token': get_from_secrets(TINDER_ACCESS_TOKEN)
        }

    def get_user(self, user_id: str) -> TinderUser:
        user_dict: TinderUserDict = self._make_get_call(url=f'/user/{user_id}/')['results']
        return TinderUser(user_dict)

    def get_recommendations(self) -> Iterator[TinderUser]:
        recommendations: List[TinderUserDict] = self._make_get_call(url='/user/recs', params={'count': 1})['results']
        for user_dict in recommendations:
            yield TinderUser(user_dict)

    def like(self, user: TinderUser) -> bool:
        """
        Swipe a user to the right

        :param user: User to swipe
        :return: Flag indicating whether you have match
        """

        return self._make_get_call(url=f'/like/{user.id}')['match']

    def nope(self, user: TinderUser):
        """
        Swipe a user to the left

        :param user: User to swipe
        """

        return self._make_get_call(url=f'/pass/{user.id}')

    def send_message(self, user_id: str, message: str):
        """
        Send a message to the given user

        Note: This endpoint results in a 403 ERROR with the following message:
                Bad request. We can't connect to the server for this app or website at this time.
                There might be too much traffic or a configuration error. Try again later, or
                contact the app or website owner.
        """

        return self._make_post_call(url=f'/user/matches/{user_id}', body={'message': message})

    def _update_tinder_tokens(self):
        authenticator = TinderAuthenticator()
        authenticator.set_new_tokens()

    def _make_get_call(self, url: str, params: Dict[str, Any] = None) -> OptionalJSON:
        response = requests.get(self.base_url + url, headers=self.headers, params=params)

        if response.status_code in (401, 403):
            # When we are not authorized, we refresh the tokens. In theory, this could lead to an
            # infinite loop of the tokens remain invalid, but in practice this never happens, since
            # user interaction is required to obtain the tokens.
            self._update_tinder_tokens()
            return self._make_get_call(url, params)

        assert response.ok, response.text
        return response.json()

    def _make_post_call(self, url: str, params: Dict[str, Any] = None, body: Dict[str, Any] = None) -> OptionalJSON:
        response = requests.get(self.base_url + url, headers=self.headers, params=params, json=body)

        if response.status_code in (401, 403):
            # When we are not authorized, we refresh the tokens. In theory, this could lead to an
            # infinite loop of the tokens remain invalid, but in practice this never happens, since
            # user interaction is required to obtain the tokens.
            self._update_tinder_tokens()
            return self._make_post_call(url, params, body)

        assert response.ok, response.text
        return response.json()


if __name__ == '__main__':
    service = TinderService()
    user_id = get_from_secrets(TINDER_USER_ID)
    result = service.get_user(user_id)
    print(result)
