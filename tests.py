import unittest
import threading
from unittest.mock import MagicMock, patch
from bs4 import BeautifulSoup
import main 

class TestWebScraper(unittest.TestCase):
    
    @patch('main.WebDriverWait')
    def test_get_pane(self, MockWebDriverWait):
        mock_element = MagicMock()
        MockWebDriverWait.return_value.until.return_value = mock_element
        result = main.get_pane()
        self.assertEqual(result, mock_element)
        MockWebDriverWait.assert_called_once()

    @patch('main.WebDriverWait')
    def test_get_next(self, MockWebDriverWait):
        mock_element = MagicMock()
        MockWebDriverWait.return_value.until.return_value = mock_element
        result = main.get_next()
        self.assertEqual(result, mock_element)
        MockWebDriverWait.assert_called_once()

    @patch('main.get_pane')
    @patch('main.get_next')
    @patch('main.get_jobs')
    @patch('main.get_info')
    @patch('main.time.sleep', return_value=None)  # Avoid actual sleeping in tests
    def test_jobs_loop(self, mock_sleep, mock_get_info, mock_get_jobs, mock_get_next, mock_get_pane):
        mock_get_pane.return_value = MagicMock()
        mock_get_next.return_value = MagicMock()
        mock_job = MagicMock()
        mock_get_jobs.return_value = [mock_job]
        mock_get_info.return_value = {"title": "Test Job"}

        main.running = True
        thread = threading.Thread(target=main.jobs_loop)
        thread.start()
        
        # Allow the loop to run briefly, then stop it
        main.running = False
        thread.join()

        mock_get_info.assert_called_once_with(mock_job)

    @patch('main.WebDriverWait')
    def test_get_div_Container(self, MockWebDriverWait):
        mock_container = MagicMock()
        mock_element = MagicMock()
        MockWebDriverWait.return_value.until.return_value = mock_element
        result = main.get_div_Container(mock_container)
        self.assertEqual(result, mock_element)
        MockWebDriverWait.assert_called_once_with(mock_container, 10)

    def test_get_info(self):
        mock_container = MagicMock()
        
        mock_title = MagicMock()
        mock_title.text = "Test Title"
        mock_img = MagicMock()
        mock_img.get_attribute.return_value = "https://example.com/image.jpg"
        
        mock_container.find_element.side_effect = [mock_title, mock_img, MagicMock()]
        mock_container.find_elements.return_value = []

        result = main.get_info(mock_container)
        
        self.assertEqual(result["title"], "Test Title")
        self.assertEqual(result["image"], "https://example.com/image.jpg")

    @patch('main.os.getenv', return_value="output.csv")
    @patch('main.csv.writer')
    @patch('builtins.open', new_callable=unittest.mock.mock_open)
    def test_write_csv(self, mock_open, mock_csv_writer, mock_getenv):
        main.jobs = [
            {
                "image": "https://example.com/image.jpg",
                "company": "Test Company",
                "title": "Test Title",
                "link": "https://example.com/job",
                "extraInfos": ["Info1", "Info2"]
            }
        ]
        main.write_csv()
        
        # Ensure the file is opened correctly
        mock_open.assert_called_once_with("output.csv", mode="w", newline="", encoding="utf-8")
        
        # Verify that writerow was called with the expected headers and row data
        writer_instance = mock_csv_writer()
        headers = ["Image", "Company", "Job Title", "Link", "ExtraInfo 1", "ExtraInfo 2"]
        writer_instance.writerow.assert_any_call(headers)
        
        row_data = [
            '=IMAGE("https://example.com/image.jpg", 4, 50, 50)',
            "Test Company",
            "Test Title",
            '=HYPERLINK("https://example.com/job", "Link")',
            "Info1",
            "Info2"
        ]
        writer_instance.writerow.assert_any_call(row_data)

if __name__ == "__main__":
    unittest.main()
