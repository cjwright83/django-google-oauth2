def profile_response():
    return {
        'emails': [{'value': 'test@example.com'}],
        'name': {'givenName': 'Test', 'familyName': 'User'},
        'hd': 'example.com'
    }


def user_details(**overrides):
    details = {'email': 'test@example.com',
               'username': 'test',
               'name': 'Test User',
               'hosted_domain': 'example.com'}
    details.update(overrides)
    return {'user': {'email': details['email'],
                     'username': details['username'],
                     'name': details['name']},
            'hosted_domain': details['hosted_domain']
            }
