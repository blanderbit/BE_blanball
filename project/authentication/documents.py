from django_elasticsearch_dsl import Document, Index, fields

from .models import Profile

profile_index = Index("profile")
profile_index.settings(
    number_of_shards=1,
    number_of_replicas=0,
)


@profile_index.doc_type
class ProfileDocument(Document):
    name = fields.TextField(attr="name", fields={"suggest": fields.Completion()})

    class Django:
        model = Profile
        fields = ["id", "age"]