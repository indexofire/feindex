# -*- coding: utf-8 -*-
from django.db import models


class Document(models.Model):
    """
    Document objects, used mainly as a hook point for Haystack.
    """
    release = models.ForeignKey(DocumentRelease, related_name='documents')
    path = models.CharField(max_length=500)
    title = models.CharField(max_length=500)

    def __unicode__(self):
        return "/".join([self.release.lang, self.release.version, self.path])

    @models.permalink
    def get_absolute_url(self):
        kwargs = {
            'lang': self.release.lang,
            'version': self.release.version,
            'url': self.path
        }
        return ('document-detail', [], kwargs)
