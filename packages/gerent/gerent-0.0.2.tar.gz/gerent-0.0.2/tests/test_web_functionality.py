import pytest
import requests


class TestClass:
    def test_405_status_code(self):
        request = requests.put("http://192.168.1.77:8090/api")
        assert request.status_code == 405
