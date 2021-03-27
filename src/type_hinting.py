from typing import Any, Dict, Union

TinderUserDict = Dict[str, Any]  # Dictionary representation of a Tinder User

# {'crop_info': {'algo': {'height_pct': 0.17501609, 'width_pct': 0.16193028,
#                         'x_offset_pct': 0.47167337, 'y_offset_pct': 0.21596518},
#                'processed_by_bullseye': True,
#                'user': {'height_pct': 0.8, 'width_pct': 1.0,
#                         'x_offset_pct': 0.0, 'y_offset_pct': 0.0},
#                'user_customized': False},
#  'extension': 'jpg,webp',
#  'fileName': '<uuid>.jpg',
#  'id': '<uuid>',
#  'processedFiles': [{'height': 800,'width': 640,
#                      'url': 'https://images-ssl.gotinder.com/<user_id>/640x800_<uuid>.jpg',},
#                     {'height': 400,'width': 320,
#                      'url': 'https://images-ssl.gotinder.com/<user_id>/320x400_<uuid>.jpg',},
#                     {'height': 216,'width': 172,
#                      'url': 'https://images-ssl.gotinder.com/<user_id>/172x216_<uuid>.jpg',},
#                     {'height': 106,'width': 84,
#                      'url': 'https://images-ssl.gotinder.com/<user_id>/84x106_<uuid>.jpg',}],
#  'url': 'https://images-ssl.gotinder.com/<user_id>/original_<uuid>.jpeg'}
PhotoDict = Dict[str, str]

# {
#     'id': 131231,  # Ignored in this code
#     'name': 'Amsterdam University'
# }
SchoolDict = Dict[str, Union[str, int]]
