from __future__ import annotations

import random
from pathlib import Path
from urllib.parse import quote

from faker import Faker
from social_media.common.media_generator import ASSETS_ROOT, get_image_files, image_to_data_uri

HOME_STATES = [
    'home', 'category_selected', 'search_suggestions', 'pin_menu',
    'save_to_board_dialog', 'create_board_dialog', 'notifications',
    'account_menu', 'empty_feed',
]
POPUP_STATES = {
    'search_suggestions', 'pin_menu', 'save_to_board_dialog',
    'create_board_dialog',
    # 'notifications', 'account_menu',
}
CATEGORIES = ['For you', 'Home decor', 'Recipes', 'Travel', 'Fashion', 'Art', 'Gardening', 'Photography']


def placeholder_image(index: int) -> str:
    """An explicit offline placeholder, rather than a broken image URL."""
    colors = ['#D6C5AF', '#A7B7A4', '#A6BAC8', '#C9AFBC', '#DBCAA0']
    color = colors[index % len(colors)]
    svg = (
        '<svg xmlns="http://www.w3.org/2000/svg" width="480" height="640" viewBox="0 0 480 640">'
        f'<rect width="480" height="640" fill="{color}"/>'
        '<circle cx="350" cy="165" r="65" fill="#FFFFFF" opacity=".45"/>'
        '<path d="M0 640V460L170 240 330 460 400 350 480 440V640Z" fill="#344039" opacity=".45"/>'
        '<text x="240" y="590" text-anchor="middle" font-family="Arial" font-size="24" fill="#172019">Image placeholder</text>'
        '</svg>'
    )
    return 'data:image/svg+xml;charset=utf-8,' + quote(svg)


def generate_home_page(state: str = 'home', *, seed: int | None = None,
                       num_pins: int = 60, assets_root: Path | None = None) -> dict:
    if state not in HOME_STATES:
        raise ValueError(f'Unknown Pinterest home state: {state!r}')
    if num_pins < 1:
        raise ValueError('num_pins must be at least 1')
    rng = random.Random(seed)
    fake = Faker()
    if seed is not None:
        fake.seed_instance(seed)
    root = Path(assets_root) if assets_root is not None else ASSETS_ROOT
    # Optional Pinterest-specific assets; otherwise reuse the shared folder.
    pin_root = root / 'pinterest' / 'pins'
    avatar_root = root / 'pinterest' / 'avatars'
    pin_files = get_image_files(str(pin_root if pin_root.exists() else root))
    avatar_files = get_image_files(str(avatar_root)) if avatar_root.exists() else ()
    # Encode each selected local asset only once per generated sample.
    cache: dict[Path, str] = {}

    def media(files: tuple, index: int) -> str:
        if not files:
            return placeholder_image(index)
        path = rng.choice(files)
        if path not in cache:
            cache[path] = image_to_data_uri(path)
        return cache[path]

    pins = []
    for index in range(num_pins):
        topic = rng.choice(CATEGORIES[1:])
        author = fake.name()
        pins.append({
            'id': index, 'title': f'{rng.choice(["Fresh", "Cozy", "Creative", "Beautiful", "Simple"])} {topic.lower()} ideas',
            'image': media(pin_files, index), 'aspect_ratio': rng.choice(['3/4', '2/3', '4/5', '1/1', '3/5']),
            'author': author, 'initials': ''.join(p[0] for p in author.split()[:2]),
            'avatar': media(avatar_files, index) if avatar_files else None,
            'domain': fake.domain_name(), 'saved': rng.random() < .18,
            'promoted': rng.random() < .12, 'topic': topic,
        })
    boards = [{'name': name, 'count': rng.randint(12, 240), 'cover': media(pin_files, i), 'secret': i == 2}
              for i, name in enumerate(['Dream home', 'Weekend recipes', 'Places to visit', 'Style inspiration', 'Creative projects'])]
    active = rng.choice(CATEGORIES[1:]) if state == 'category_selected' else 'For you'
    if state == 'category_selected':
        # A category state visibly changes content, while preserving pin identities.
        pins = [pin for pin in pins if pin['topic'] == active] or pins[:6]
    name = fake.name()
    return {
        'state': state, 'popup_visible': state in POPUP_STATES,
        'categories': CATEGORIES, 'active_category': active,
        'pins': [] if state == 'empty_feed' else pins, 'selected_pin': pins[0],
        'boards': boards, 'query': 'cozy home',
        'suggestions': ['Cozy home decor', 'Cozy home office', 'Cozy bedroom ideas', 'Small apartment inspiration'],
        'user': {'name': name, 'email': fake.email(), 'initials': ''.join(p[0] for p in name.split()[:2])},
        'notifications': [{'name': fake.name(), 'message': rng.choice(['saved a Pin from your board', 'shared new ideas with you', 'started following you']),
                           'time': f'{rng.randint(1, 59)}m', 'image': media(pin_files, i)} for i in range(6)],
        'asset_count': len(pin_files),
    }
