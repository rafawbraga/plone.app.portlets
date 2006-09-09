from Acquisition import aq_parent
from Testing.ZopeTestCase import user_name

from zope.app.component.hooks import setSite, setHooks
from zope.component import getMultiAdapter, getUtility

from plone.portlets.interfaces import IPortletManager, IPortletAssignmentMapping

from plone.portlets.constants import USER_CATEGORY
from plone.portlets.constants import GROUP_CATEGORY
from plone.portlets.constants import CONTENT_TYPE_CATEGORY

from plone.app.portlets.tests.base import PortletsTestCase
from plone.app.portlets.portlets.classic import ClassicPortletAssignment

class TestTraversal(PortletsTestCase):

    def afterSetUp(self):
        setHooks()
        setSite(self.portal)

    def testContextNamespace(self): 
        assignment = ClassicPortletAssignment()
        manager = getUtility(IPortletManager, name='plone.leftcolumn')
        mapping = self.folder.restrictedTraverse('++contextportlets++plone.leftcolumn')
        target = getMultiAdapter((self.folder, manager), IPortletAssignmentMapping)
        self.failUnless(aq_parent(mapping) is self.folder)
        mapping['foo'] = assignment
        self.failUnless(target['foo'] is assignment)

    def testCurrentUserNamespace(self): 
        assignment = ClassicPortletAssignment()
        manager = getUtility(IPortletManager, name='plone.leftcolumn')
        mapping = self.portal.restrictedTraverse('++myportlets++plone.leftcolumn')
        self.failUnless(aq_parent(mapping) is self.portal)
        mapping['foo'] = assignment
        self.failUnless(manager[USER_CATEGORY][user_name]['foo'] is assignment)

    def testUserNamespace(self): 
        assignment = ClassicPortletAssignment()
        manager = getUtility(IPortletManager, name='plone.leftcolumn')
        mapping = self.portal.restrictedTraverse('++userportlets++plone.leftcolumn+' + user_name)
        self.failUnless(aq_parent(mapping) is self.portal)
        mapping['foo'] = assignment
        self.failUnless(manager[USER_CATEGORY][user_name]['foo'] is assignment)

    def testGroupNamespace(self): 
        assignment = ClassicPortletAssignment()
        manager = getUtility(IPortletManager, name='plone.leftcolumn')
        mapping = self.portal.restrictedTraverse('++groupportlets++plone.leftcolumn+Reviewers')
        self.failUnless(aq_parent(mapping) is self.portal)
        mapping['foo'] = assignment
        self.failUnless(manager[GROUP_CATEGORY]['Reviewers']['foo'] is assignment)

    def testContentTypeNamespace(self): 
        assignment = ClassicPortletAssignment()
        manager = getUtility(IPortletManager, name='plone.leftcolumn')
        mapping = self.portal.restrictedTraverse('++contenttypeportlets++plone.leftcolumn+Image')
        self.failUnless(aq_parent(mapping) is self.portal)
        mapping['foo'] = assignment
        self.failUnless(manager[CONTENT_TYPE_CATEGORY]['Image']['foo'] is assignment)
        
def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestTraversal))
    return suite