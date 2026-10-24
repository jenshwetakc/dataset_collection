from __future__ import annotations

import importlib
import random
from pathlib import Path
from faker import Faker

FAKE = Faker()
GENRES = ['Drama', 'Fantasy', 'Comedy', 'Action', 'Slice of life', 'Romance', 'Superhero', 'Sci-fi']
DAYS = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun', 'Completed']
STATES = ['home', 'popular_selected', 'category_selected', 'daily_selected', 'completed_selected', 'carousel_next', 'search_open', 'search_results', 'search_empty', 'login_dialog', 'language_menu', 'recently_viewed']


def compact(value: int) -> str:
    if value >= 1_000_000:
        return f'{value / 1_000_000:.1f}M'
    if value >= 1000:
        return f'{value / 1000:.0f}K'
    return str(value)


def generate_home_page(package_root: str = 'social_media') -> dict:
    media = importlib.import_module(f'{package_root}.common.media_generator')
    assets = Path(media.ASSETS_ROOT)
    folders = {}
    for kind in ['covers', 'banners']:
        preferred = assets / 'webtoon' / kind
        folders[kind] = preferred if media.get_image_files(str(preferred)) else (assets if kind == 'covers' else None)
    cover_available = bool(media.get_image_files(str(folders['covers'])))
    series = []
    # Enough records for every category and release day to produce full sections.
    for index in range(112):
        series.append({
            'id': index, 'title': FAKE.sentence(nb_words=random.randint(3, 6)).rstrip('.'),
            'creator': FAKE.name(), 'genre': GENRES[index % len(GENRES)],
            'day': DAYS[index % len(DAYS)],
            'cover': media.get_random_image(folders['covers']) if cover_available else None,
            'views': compact(random.randint(250_000, 900_000_000)),
            'likes': compact(random.randint(20_000, 8_000_000)),
            'change': random.choice([-3, 0, 2, 4, 7, 11]),
            'badge': random.choice(['', '', '', 'UP', 'NEW']),
        })
    return {
        'series': series, 'genres': GENRES, 'days': DAYS,
        'trending': random.sample(series, 10), 'popular': random.sample(series, 10),
        'new_releases': random.sample(series, 10), 'indie': random.sample(series, 12),
        'recent': random.sample(series, 3),
        'banner': media.get_random_image(folders['banners']) if folders['banners'] else None,
        'banner_title': 'Discover a new world of stories',
        'query': series[0]['title'], 'category_choice': random.choice(GENRES[1:]),
        'day_choice': random.choice(DAYS[1:7]), 'state': 'home', 'popup': False,
    }


def make_state(content: dict, state: str) -> dict:
    if state not in STATES:
        raise ValueError(f'Unknown WEBTOON state: {state}')
    data = dict(content)
    genre = content['category_choice'] if state == 'category_selected' else 'Drama'
    day = 'Completed' if state == 'completed_selected' else content['day_choice'] if state == 'daily_selected' else 'Mon'
    page_index = 1 if state == 'carousel_next' else 0
    ranking = content['popular'] if state == 'popular_selected' else content['trending']
    data.update(
        state=state, popup=state in {'login_dialog', 'language_menu', 'recently_viewed'},
        heading='Home', ranking_tab='Popular' if state == 'popular_selected' else 'Trending',
        selected_genre=genre, selected_day=day, carousel_page=page_index,
        ranking_cards=ranking[page_index * 5:(page_index + 1) * 5],
        category_cards=[s for s in content['series'] if s['genre'] == genre][:6],
        daily_cards=[s for s in content['series'] if s['day'] == day][:12],
        new_cards=content['new_releases'][:5], indie_cards=content['indie'][:6],
        search_visible=state in {'search_open', 'search_results', 'search_empty'},
        search_results=[],
    )
    if state == 'search_results':
        data['search_results'] = [s for s in content['series'] if content['query'].casefold() in s['title'].casefold()]
    elif state == 'search_empty':
        data['query'] = 'No matching series 7391'
    elif state == 'search_open':
        data['query'] = ''
    return data
