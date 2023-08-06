============================
collective.compoundcriterion
============================

.. image:: https://secure.travis-ci.org/collective/collective.compoundcriterion.png
   :target: http://travis-ci.org/collective/collective.compoundcriterion

.. image:: https://coveralls.io/repos/collective/collective.compoundcriterion/badge.svg?branch=master&service=github
  :target: https://coveralls.io/github/collective/collective.compoundcriterion?branch=master


This package add a new kind of criterion available for plone.app.collection.

Motivation
----------

Sometimes, some index are composed of different elements with a certain logic or you need to query particular elements of the site like groups of the current user or anything else.
This is not achievable using default indexes and Collection UI, you need to write python code.

How to use
----------

When adding/editing a Collection, a new criterion filed under the 'Other' category of available indexes called 'Filter' is available.

When selecting a 'Filter', a selection box will show you named adapter that provide the collective.compoundcriterion.interfaces.ICoumpondCriterionFilter interface.

You will be able to select among available ones.  This can still be used together with other criteria.

To register this complex query builder named adapter, you will have to add this kind of code :

.. code:: xml

   <adapter for="*"
            factory="collective.compoundcriterion.tests.adapter.CompoundCrietrionFilterAdapter"
            provides="collective.compoundcriterion.interfaces.ICompoundCriterionFilter"
            name="testing-compound-adapter" />

How to test
-----------

Add the adapter registration zcml here above to a configure.zcml file (like the one in collective.compoundcriterion), it will make the 'testing-compound-adapter' available in the Collection 'Filter' index.

This testing adapter will query elements of the site having string 'special_text_to_find' in the title.  So create a document with such title and it should work.

A second adapter can be used to test :

.. code:: xml

    <adapter for="*"
             factory="collective.compoundcriterion.tests.adapter.SampleCompoundCrietrionFilterAdapter"
             provides="collective.compoundcriterion.interfaces.ICompoundCriterionFilter"
             name="sample-compound-adapter" />

This one will query elements having 'title_with_sample_text' in the title.


Negative index adapters
-----------------------

Two specific adapters exist to negativize query:

- `negative-previous-index` that will negativize the values of the previous index defined in the query;
- `negative-personal-labels` that does the same but for ftw.labels personal labels that needs specific handling as current user id is managed in indexed values.


Translations
------------

This product has been translated into

- French.

- Spanish.

You can contribute for any message missing or other new languages, join us at `Plone Collective Team <https://www.transifex.com/plone/plone-collective/>`_ into *Transifex.net* service with all world Plone translators community.

