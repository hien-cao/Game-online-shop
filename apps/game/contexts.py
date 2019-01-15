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
    'uploads': 'is-active',
    'crumbs': [
        {
            'label': 'Home',
            'url': 'home'
        },
        {
            'label': 'Uploads',
            'url': 'uploads'
        }
    ]
}

def get_play_game_context(game):
    return {
        'game': game,
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
                'game': game
            },
        ]
    }
