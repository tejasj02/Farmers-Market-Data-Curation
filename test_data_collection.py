import unittest
from unittest.mock import patch, MagicMock
from bs4 import BeautifulSoup
import pandas as pd
from data_collection import *

class TestFarmersMarketScript(unittest.TestCase):

    def test_fetch_census_data(self):
        result = fetch_census_data()

        # Test DataFrame properties
        self.assertIsInstance(result, pd.DataFrame)
        self.assertTrue(len(result) > 0) 

        # Test column names
        expected_columns = ['zipcode', 'total_population', 'median_income', 'pop_18_30']
        self.assertListEqual(list(result.columns), expected_columns)

    def test_extract_market_details(self):
        html_content = '''
        <table cellpadding="4">
            <tr>
                <td>
                    <span class="style1">Market Name</span>
                    <p align="left">
                        <a href="#">Some Link</a>
                        123 Market St, City, NC 12345
                        <strong>End</strong>
                    </p>
                    <a href="http://example.com" string="Web Site">Web Site</a>
                </td>
            </tr>
        </table>
        '''
        soup = BeautifulSoup(html_content, 'html.parser')
        result = extract_market_details(soup)

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['name'], 'Market Name')
        self.assertEqual(result[0]['address'], '123 Market St, City, NC 12345')
        self.assertEqual(result[0]['website'], 'http://example.com')

    @patch('data_collection.request_page')
    @patch('data_collection.extract_market_details')
    def test_fetch_all_markets(self, mock_extract, mock_request):
        # Mock the request_page function
        mock_response = MagicMock()
        mock_response.text = '<html></html>'
        mock_request.return_value = mock_response

        # Mock the extract_market_details function
        mock_extract.return_value = [{'name': 'Market 1'}, {'name': 'Market 2'}]

        result = fetch_all_markets('https://example.com')
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]['name'], 'Market 1')
        self.assertEqual(result[1]['name'], 'Market 2')

if __name__ == '__main__':
    unittest.main()