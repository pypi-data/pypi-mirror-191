from kolibri.core.content import models
from kolibri.core.content.api import ContentNodeViewset


class AllContentNodeViewset(ContentNodeViewset):
    def get_queryset(self):
        return models.ContentNode.objects.all()
