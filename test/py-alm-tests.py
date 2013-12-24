import unittest
import pyalm.pyalm as pyalm
import datetime
import pprint
import json

#@unittest.skip('Test for live API which require an API Key. See pyalm.api_key.example')
class testOnlineTests(unittest.TestCase):

    def setUp(self):
        self.test_doi = "10.1371/journal.pone.0029797"
        self.test_two_dois = "10.1371/journal.pone.0029797,10.1371/journal.pone.0029798"
        self.test_response_doi = "10.1371/journal.pone.0029797"
        self.test_response_doi2 = "10.1371/journal.pone.0029798"
        self.test_response_title = "Ecological Guild Evolution and the Discovery of the World's Smallest Vertebrate"
        self.test_response_title2 = "Mitochondrial Electron Transport Is the Cellular Target of the Oncology Drug Elesclomol"
        self.test_response_views = 29278
        self.test_response_views2 = 2909
        self.test_response_publication_date = datetime.datetime(2012, 1, 11, 8, 0, 0)
        self.test_response_mendeley_event_url = u'http://www.mendeley.com/research/ecological-guild-evolution-discovery-worlds-smallest-vertebrate/'
        self.test_source = 'twitter,counter,crossref,wikipedia,mendeley'

    def tearDown(self):
        del self.resp

    def testGet(self):
        self.resp = pyalm.get_alm(self.test_doi, source = self.test_source, info ='detail')
        #Basic Tests
        self.assertEqual(self.resp.title, self.test_response_title)
        self.assertEqual(self.resp.doi, self.test_response_doi)
        self.assertGreaterEqual(self.resp.views, self.test_response_views)
        self.assertEqual(type(self.resp.update_date), datetime.datetime)
        self.assertEqual(self.resp.publication_date, self.test_response_publication_date)

        #Sources numeric tests
        self.assertGreaterEqual(self.resp.sources['twitter'].metrics.total, 9)
        self.assertGreaterEqual(self.resp.sources['counter'].metrics.total, 28887)
        self.assertGreaterEqual(self.resp.sources['crossref'].metrics.total, 7)
        #self.assertGreaterEqual(self.resp.sources['pmc'].metrics.total, 391)

        #Sources names and urls
        self.assertEqual(self.resp.sources['mendeley'].events_url,
                                       self.test_response_mendeley_event_url)

        #Sources metrics test
        self.assertGreaterEqual(self.resp.sources['twitter'].metrics.comments, 9)

        #Sources histories tests
        timepoints = self.resp.sources['wikipedia'].histories
        self.assertEqual(timepoints[0][0], datetime.datetime(2012, 9, 19, 12, 56, 23))

    def testGetMultipleDOIs(self):
        self.resp = pyalm.get_alm(self.test_two_dois, info='summary')
        self.assertEqual(self.resp[0].title, self.test_response_title)
        self.assertEqual(self.resp[0].doi, self.test_response_doi)
        self.assertGreaterEqual(self.resp[0].views, self.test_response_views)
        self.assertEqual(self.resp[1].title, self.test_response_title2)
        self.assertEqual(self.resp[1].doi, self.test_response_doi2)
        self.assertGreaterEqual(self.resp[1].views, self.test_response_views2)


class TestOffline(unittest.TestCase):
    def setUp(self):
        self.test_doi = "10.1371/journal.pone.0029797"
        self.test_response_doi = "10.1371/journal.pone.0029797"
        self.test_response_title = "TEST-JSON: Ecological Guild Evolution and the Discovery of the World's Smallest Vertebrate"
        self.test_response_views = 29278
        self.test_response_publication_date = datetime.datetime(2012, 1, 11, 8, 0, 0)
        self.test_response_mendeley_event_url = u'http://www.mendeley.com/research/ecological-guild-evolution-discovery-worlds-smallest-vertebrate/'
        self.test_source = 'twitter'

        with open('test/test_data_history.json', 'r') as f:
            self.json_body = json.load(f)[0]
        self.mock_resp = pyalm.ArticleALM(self.json_body)
        self.mock_resp._resp_json = self.json_body

    def tearDown(self):
        del self.mock_resp
        del self.json_body

class TestBasicElements(TestOffline):
    def testBasicElements(self):
        self.assertEqual(self.mock_resp.title, self.test_response_title)
        self.assertEqual(self.mock_resp.doi, self.test_response_doi)
        self.assertGreaterEqual(self.mock_resp.views, self.test_response_views)
        self.assertEqual(type(self.mock_resp.update_date), datetime.datetime)
        self.assertEqual(self.mock_resp.publication_date, self.test_response_publication_date)

class TestSourcesNumbers(TestOffline):
    def testSourcesNumbers(self):
        self.assertEqual(self.mock_resp.sources['twitter'].metrics.total, 9)
        self.assertEqual(self.mock_resp.sources['counter'].metrics.total, 28887)
        self.assertEqual(self.mock_resp.sources['crossref'].metrics.total, 7)
        self.assertEqual(self.mock_resp.sources['pmc'].metrics.total, 391)
        self.assertEqual(self.mock_resp.sources['twitter'].metrics.total, 9)

class TestSourcesAttributes(TestOffline):
    def testSourcesAttributes(self):
        self.assertEqual(self.mock_resp.sources['mendeley'].events_url,
                                       self.test_response_mendeley_event_url)

class TestSourcesMetrics(TestOffline):
    def testSourcesMetrics(self):
        self.assertEqual(self.mock_resp.sources['twitter'].metrics.comments, 9)

class TestSourcesHistories(TestOffline):
    def testWikipediaHistory(self):
        timepoints = self.mock_resp.sources['wikipedia'].histories
        self.assertEqual(timepoints[0][0], datetime.datetime(2012, 9, 19, 12, 56, 23))
        self.assertEqual(timepoints[0][1], 206)
        self.assertEqual(len(timepoints), 10)

    def testMendeleyHistory(self):
        timepoints = self.mock_resp.sources['mendeley'].histories
        self.assertEqual(timepoints[0][0], datetime.datetime(2012, 1, 12, 8, 7, 32))
        self.assertEqual(timepoints[0][1], 0)
        self.assertEqual(timepoints[83][0], datetime.datetime(2013, 9, 15, 19, 42, 18))
        self.assertEqual(timepoints[83][1], 50)
        self.assertEqual(len(timepoints), 84)

    def testTwitterHistory(self):
        timepoints = self.mock_resp.sources['twitter'].histories

@unittest.skip('no need to print')
class TestSourcesEvents(TestOffline):
    def testTwitterEvents(self):
        print "\n\nTwitter\n"
        pprint.pprint(self.mock_resp.sources['twitter'].events[0])

    def testWikipediaEvents(self):
        print "\n\nWikipedia\n"
        pprint.pprint(self.mock_resp.sources['wikipedia'].events)

    def testCrossrefEvents(self):
        print "\n\nCrossref\n"
        pprint.pprint(self.mock_resp.sources['crossref'].events[0])



if __name__ == "__main__":
    unittest.main()