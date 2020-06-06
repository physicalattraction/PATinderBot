import json
import os.path
from shutil import copyfile
from typing import Any, Dict

import common

SECRETS_FILE = os.path.join(common.get_dir('json'), 'secrets.json')
SECRETS_TEMPLATE_FILE = os.path.join(common.get_dir('json'), 'secrets_template.json')

# TODO: Make this an Enum
TINDER_PHONE_NUMBER = 'TINDER_PHONE_NUMBER'
TINDER_USER_ID = 'TINDER_USER_ID'
TINDER_ACCESS_TOKEN = 'TINDER_ACCESS_TOKEN'
TINDER_REFRESH_TOKEN = 'TINDER_REFRESH_TOKEN'


def _read_secrets_file() -> Dict[str, Any]:
    if not os.path.isfile(SECRETS_FILE):
        copyfile(SECRETS_TEMPLATE_FILE, SECRETS_FILE)
    with open(SECRETS_FILE, 'r') as f:
        return json.load(f)


def _write_secrets_file(secrets: Dict[str, Any]):
    with open(SECRETS_FILE, 'w') as fp:
        return json.dump(secrets, fp, indent=2)


def get_from_secrets(key: str) -> Any:
    secrets = _read_secrets_file()
    return secrets.get(key)


def set_in_secrets(key: str, value: Any):
    secrets = _read_secrets_file()
    secrets[key] = value
    _write_secrets_file(secrets)
