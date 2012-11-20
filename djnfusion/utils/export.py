import csv

from django.contrib.auth.models import User

from djnfusion import _user_dict


def export_users_csv(users, file):
    """Write user data into a file, in a csv-format suitable for InfusionSoft. Caller is responsible for opening and closing the file."""

    writer = csv.writer(file, delimiter=',', quoting=csv.QUOTE_MINIMAL)

    # build sorted list of keys for heading
    _dummy_user = User.objects.all()[0]
    _dummy_user_dict = _user_dict(user=_dummy_user, create=True)
    sorted_keys = sorted(_dummy_user_dict.keys())

    # write heading
    writer.writerow(sorted_keys)

    # write users
    for user in users:
        user_dict = _user_dict(user=user, create=True)
        dict_items = user_dict.items()
        sorted_dict_items = sorted(dict_items, key=lambda i: i[0]) # sort by dict key
        sorted_dict_values = [unicode(v).encode('utf-8') for k, v in sorted_dict_items]
        writer.writerow(sorted_dict_values)

    
        