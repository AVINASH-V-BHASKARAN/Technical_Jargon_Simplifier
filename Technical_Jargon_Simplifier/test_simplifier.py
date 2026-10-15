import unittest
from simplifier import GLOSSARY, simplify, preprocess

class SimplifierTests(unittest.TestCase):
    def test_required_glossary(self):
        self.assertGreaterEqual(len(GLOSSARY),30)
        self.assertTrue({'AI','Computer science','Networking','Programming'} <= {x['category'] for x in GLOSSARY})
    def test_example(self):
        r=simplify('Machine learning algorithms utilize training datasets to optimize predictive models.')
        self.assertEqual(r['simplified'],'Machine learning methods learn from examples to make better predictions.')
        self.assertIn('training dataset',{x['term'] for x in r['terms']})
    def test_longest_term(self):
        r=simplify('A neural network uses machine learning.')
        self.assertEqual({x['term'] for x in r['terms']},{'neural network','machine learning'})
    def test_boundaries(self):
        self.assertEqual(simplify('The domain contains snails.')['terms'],[])
    def test_empty(self):
        self.assertEqual(simplify('   ')['status'],'empty')
    def test_plain_text(self):
        text='The cat sleeps on the chair.'
        r=simplify(text);self.assertEqual(r['status'],'no_terms');self.assertEqual(r['simplified'],text)
    def test_repeated_and_plural(self):
        r=simplify('Algorithms and algorithms use APIs.')
        self.assertEqual(len(r['terms']),2);self.assertEqual(r['terms'][0]['count'],2)
    def test_negation(self):
        r=simplify('Encryption does not prevent every attack.')
        self.assertIn('not',r['simplified']);self.assertIn('not',r['preprocessing']['content_tokens'])
    def test_hyphen_case(self):
        self.assertIn('machine learning',{x['term'] for x in simplify('MACHINE-LEARNING uses DATASETS.')['terms']})
    def test_definitions_in_output(self):
        r=simplify('The compiler checks source code.')
        for term in r['terms']:self.assertIn(term['definition'],r['explanation'])
    def test_no_cascading(self):
        r=simplify('An API connects software.')
        self.assertEqual([x['term'] for x in r['terms']],['API'])
    def test_articles(self):
        result=simplify('The compiler uses an API.')['simplified']
        self.assertNotIn('The a ',result)
        self.assertNotIn('an a ',result)
        self.assertIn('a way',result)
    def test_singular_plural_phrases(self):
        self.assertEqual(simplify('A function calls a function.')['simplified'],'A reusable block of instructions calls a reusable block of instructions.')
        self.assertEqual(simplify('A variable stores a number.')['simplified'],'A named place that holds a value stores a number.')
        self.assertEqual(simplify('A packet is sent.')['simplified'],'A small piece of transmitted data is sent.')
        self.assertEqual(simplify('Packets are sent.')['simplified'],'Small pieces of transmitted data are sent.')
    def test_invalid_type(self):
        with self.assertRaises(TypeError):simplify(None)
    def test_stopwords_inspection_only(self):
        p=preprocess('The database is not ready.')
        self.assertNotIn('the',p['content_tokens']);self.assertIn('not',p['content_tokens'])
    def test_unicode_and_whitespace(self):
        self.assertEqual(simplify('  The\u00a0API\nconnects software.  ')['normalized'],'The API connects software.')

if __name__=='__main__':unittest.main()
