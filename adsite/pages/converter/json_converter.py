import json

from core.forms.create_ad_form import AdForm
from core.models import Ad


def convert_json_to_ad(data_json):
    ad_json = json.loads(json.dumps(data_json))

    ad = Ad()

    ad.server_id = ad_json.get('id')
    ad.is_featured = ad_json.get('featured', False)
    ad.description = ad_json.get('description')
    ad.short_description = ad_json.get('short_description')
    ad.title = ad_json.get('title')
    ad.category = ad_json.get('category')
    ad.personality = ad_json.get('personality')
    ad.price = ad_json.get('price')

    return ad


def convert_form_to_ad(form: AdForm):
    ad = Ad()
    ad.price = form.cleaned_data['price']
    ad.personality = form.personality
    ad.title = form.title
    ad.short_description = form.short_description
    ad.category = form.category
    ad.description = form.description
    return ad
