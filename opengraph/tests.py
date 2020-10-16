"""
test.py module
"""
from django.test import TestCase
from django.urls import reverse


# Create your tests here.
class IndexViewTests(TestCase):
    """This class contains methods for test"""
    def test_index_page(self):
        """Check main page contains the form"""
        response = self.client.get(reverse("index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Open Graph parser')

    def test_correct_url_with_og(self):
        """Check response correct url contains Open Graph"""
        response = self.client.post(
            reverse("index"),
            {'url': 'https://www.youtube.com/watch?v=v_-ircfNnV8'}
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '5 вопросов Игорю Ашурбейли, Главе нации Асгардии')
        self.assertNotContains(response, 'Ошибка URL или ошибка удаленного сервера')

    def test_correct_url_without_og(self):
        """Check response correct url not contains Open Graph"""
        response = self.client.post(reverse("index"), {'url': 'https://asgardia.space/ru/'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Разметка Open Graph отсутствует')
        self.assertNotContains(response, 'Ошибка URL или ошибка удаленного сервера')

    def test_wrong_url(self):
        """Check not existent url"""
        response = self.client.post(reverse("index"), {'url': 'https://sdlffasfjsdlkfhsafh.com'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Ошибка URL или ошибка удаленного сервера')

    def test_empty_url(self):
        """Check empty url"""
        response = self.client.post(reverse("index"), {'url': ''})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Open Graph parser')
