from accounts.models import Ad


def get_ads_by_username(username):
    return Ad.objects.filter(user__username__contains = username)
