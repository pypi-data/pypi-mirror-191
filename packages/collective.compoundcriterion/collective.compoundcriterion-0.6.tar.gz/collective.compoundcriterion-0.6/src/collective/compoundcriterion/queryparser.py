# encoding: utf-8

from collective.compoundcriterion.interfaces import ICompoundCriterionFilter
from plone.z3cform.layout import FormWrapper
from Products.CMFPlone.Portal import PloneSite
from zope.component import queryAdapter
from zope.globalrequest import getRequest


def _get_real_context(context):
    """If context is a 'Plone Site' (case when used with Collection of
       plone.app.contenttypes), try to get real context from REQUEST."""
    if isinstance(context, PloneSite):
        request = getRequest()
        published = request.get('PUBLISHED', None)
        if published and hasattr(published, 'context'):
            context = published.context
    elif isinstance(context, FormWrapper):
        context = context.context
    return context


def _filter_is(context, row):
    context = _get_real_context(context)
    values = row.values
    # compatibility when using SingleSelectionWidget
    if not hasattr(values, '__iter__'):
        values = [values]

    query = {}
    for value in values:
        named_adapter = queryAdapter(context,
                                     ICompoundCriterionFilter,
                                     name=value)
        if named_adapter:
            # check that query is plone.app.querystring compliant
            # the value needs to be defined with a 'query' dict like :
            # {
            #  'portal_type':
            #  {'query': ['portal_type1', 'portal_type2']},
            #  'created':
            #  {'query': DateTime('2015/05/05'),
            #   'range': 'min'},
            # }
            for term in named_adapter.query.values():
                if not isinstance(term, dict) or \
                   ('query' in term and isinstance(term['query'], dict) and 'not' in term['query']) or \
                   ('query' not in term and 'not' not in term):
                    raise ValueError(
                        "The query format returned by '{0}' named adapter "
                        "is not plone.app.querystring compliant ! "
                        "'query' level must be present in dictionary, excepted for 'not' criteria !".format(row.values))
            query.update(named_adapter.query)
    return query
