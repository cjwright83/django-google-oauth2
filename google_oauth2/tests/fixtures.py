def profile_response():
    return {
        'emails': [{'value': 'test@example.com'}],
        'name': {'givenName': 'Test', 'familyName': 'User'},
        'hd': 'example.com'
    }


def user_details(**overrides):
    details = {'email': 'test@example.com',
               'username': 'test',
               'first_name': 'Test',
               'last_name': 'User',
               'hosted_domain': 'example.com'}
    details.update(overrides)
    return {'user': {'email': details['email'],
                     'username': details['username'],
                     'first_name': details['first_name'],
                     'last_name': details['last_name']},
            'hosted_domain': details['hosted_domain']
            }
