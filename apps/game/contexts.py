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


def get_purchase_context(purchase):
    return {
        **purchase.get_payment_context(),
        'purchase': purchase,
        'crumbs': [
            {
                'label': 'Browse',
                'url': 'games'
            },
            {
                'label': purchase.game.name,
                'url': 'game_details',
                'is_game_url': True,
                'game': purchase.game,
            },
            {'label': 'Purchase'},
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
                'label': game.name,
                'game': game
            },
        ]
    }


def get_upsert_game_context(game, form, title, url):
    return {
        'form': form,
        'title': title,
        'crumbs': [
            {
                'label': 'Home',
                'url': 'home'
            },
            {
                'label': 'Uploads',
                'url': 'uploads'
            },
            {
                'url': url,
                'label': title,
                'is_game_url': url == 'edit_game',
                'game': game
            },
        ]
    }
