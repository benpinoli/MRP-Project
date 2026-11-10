import unittest
from samsung_research.long_horizon_pdf_extract import render_pages
class FakePage:
 def __init__(self,s):self.s=s
 def extract_text(self):
  if self.s is None:raise ValueError('test error')
  return self.s
class PDFChecks(unittest.TestCase):
 def test_page_numbers_and_errors(self):
  rows=list(render_pages([FakePage('alpha'),FakePage(None),FakePage('gamma')]))
  self.assertEqual([r[0] for r in rows],[1,2,3]);self.assertEqual(rows[0][1],'alpha');self.assertIn('ValueError',rows[1][2]);self.assertEqual(rows[2][1],'gamma')
if __name__=='__main__':unittest.main()
