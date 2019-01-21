from .models import Highscore

games_context = {
    'games': 'is-active',
    'crumbs': [
        {
            'label': 'Home',
            'url': 'home'
        },
        {
            'label': 'Browse'
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
            'label': 'Library'
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
            'label': 'Uploads'
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
        # Select top 10 scores
        'highscores': Highscore.objects.filter(game=game).order_by('-score')[:10],
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
                'url': 'game_details',
                'is_game_url': True,
                'game': game,
            },
            {
                'label': "play",
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
