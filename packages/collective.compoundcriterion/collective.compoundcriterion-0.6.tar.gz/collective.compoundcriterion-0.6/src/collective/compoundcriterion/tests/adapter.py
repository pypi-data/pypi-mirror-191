# encoding: utf-8


class TestingCompoundCriterionFilterAdapter(object):

    def __init__(self, context):
        self.context = context

    @property
    def query(self):
        return {'Title': {'query': u'special_text_to_find'}}


class SampleCompoundCriterionFilterAdapter(object):

    def __init__(self, context):
        self.context = context

    @property
    def query(self):
        return {'Title': {'query': u'title_with_sample_text'}}


class PortalTypeCompoundCriterionFilterAdapter(object):

    def __init__(self, context):
        self.context = context

    @property
    def query(self):
        return {'portal_type': {'query': ['Document', 'Folder']}}


class WrongFormatCompoundCriterionFilterAdapter(object):

    def __init__(self, context):
        self.context = context

    @property
    def query(self):
        return {'portal_type': ['Document', 'Folder']}


class NotCompoundCriterionFilterAdapter(object):

    def __init__(self, context):
        self.context = context

    @property
    def query(self):
        return {'portal_type': {'not': ['Folder']}}


class WrongNotCompoundCriterionFilterAdapter(object):

    def __init__(self, context):
        self.context = context

    @property
    def query(self):
        return {'portal_type': {'query': {'not': ['Document']}}}
