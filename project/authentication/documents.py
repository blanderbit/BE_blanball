from .models import Profile

from django_elasticsearch_dsl import Document
from django_elasticsearch_dsl.registries import registry



@registry.register_document
class ProfileDocument(Document):
    class Index:
        name = 'profiles'
        settings = {
            'number_of_shards': 1,
            'number_of_replicas': 0,
        }

    class Django:
        model = Profile
        fields = ['name','gender','about_me','last_name','age','avatar',
        'height','weight','position']