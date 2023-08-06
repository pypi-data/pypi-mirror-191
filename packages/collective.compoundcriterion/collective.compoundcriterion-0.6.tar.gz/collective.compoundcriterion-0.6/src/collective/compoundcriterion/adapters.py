# -*- coding: utf-8 -*-

from imio.helpers.cache import get_current_user_id


class NegativePreviousIndexValuesAdapter(object):

    # make it easy to determinate adapter name in case it is registered
    # several times or under another name
    _adapter_name = u'negative-previous-index'

    def __init__(self, context):
        self.context = context

    @property
    def query(self):
        '''Special query that will get previous value in DashboardCollection and
           negativize values.  So for example, if previous index is portal_type,
           values are negativized, elements with none of the defined portal_type
           will be found.'''
        # get previous index
        previous = None
        for value in self.context.query:
            if value[u'i'] == u'CompoundCriterion' and \
               self._adapter_name in value[u'v']:
                break
            previous = value

        query = {}
        if previous:
            query[previous[u'i']] = {'not': previous[u'v']}
        return query


class NegativePersonalLabelsAdapter(object):

    def __init__(self, context):
        self.context = context
        self.request = context.REQUEST

    @property
    def query(self):
        '''Special query that will get personal labels defined in DashboardCollection
           query and turn personal labels to negative personal values.'''
        # get personal labels to make current user aware and to negativate
        labels = [value for value in self.context.query if value[u'i'] == u'labels']
        if labels:
            member_id = get_current_user_id(self.request)
            # if no selected values, the 'v' key is not there...
            labels = labels[0].get('v', [])
            personal_labels = ['{0}:{1}'.format(member_id, label) for label in labels]
        return {'labels': {'not': personal_labels}, }
