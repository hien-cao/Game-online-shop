games_context = {
    'games': 'is-active',
    'crumbs': [
        {
            'label': 'Home',
            'url': 'home'
        },
        {
            'label': 'Browse',
            'url': 'games'
        }
    ]
}

library_context = {
    'library': 'is-active',
    'crumbs': [
        {
            'label': 'Home',
            'url': 'home'
        },
        {
            'label': 'Library',
            'url': 'library'
        }
    ]
}

my_context = {
    'my': 'is-active',
    'crumbs': [
        {
            'label': 'Home',
            'url': 'home'
        },
        {
            'label': 'Uploads',
            'url': 'my'
        }
    ]
}

def get_play_game_context(**game_args):
    return {
        'crumbs': [
            {
                'label': 'Home',
                'url': 'home'
            },
            {
                'label': 'Browse',
                'url': 'games'
            },
            {
                'url': 'play',
                'is_game_url': True,
                **game_args
            },
        ]
    }
