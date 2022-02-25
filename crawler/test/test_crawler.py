from rest_framework import status
from rest_framework.test import APITestCase


class CrawlerTestCase(APITestCase):
    def test_surfit의_개발_카테고리_목록_반환_성공(self):
        """
        Surfit에 존재하는 모든 개발 카테고리 목록을 반환한다.
        """
        # given
        expected_response_data = [
            "일반 개발",
            "웹 개발",
            "Javascript",
            "React",
            "Vue.js",
            "Angular",
            "Node.js",
            "Java",
            "Python",
            "PHP",
            "Infra Structure",
            "Database",
            "Android",
            "iOS",
            "Git",
            "빅데이터 · AI · 머신러닝",
        ]
        # when
        response = self.client.get(path="/surfit/categories")
        # then
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()["categories"], expected_response_data)

    def test_surfit의_모든_개발_카테고리별_링크_목록_반환_성공(self):
        # given
        # when
        response = self.client.get(path="/surfit")
        # then
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_특정_카테고리의_링크_목록_반환_성공(self):
        """
        요청 url의 query_param에 해당하는 카테고리의 링크 목록을 반환한다.
        """
        # given
        category = "빅데이터 · AI · 머신러닝"
        # when
        response = self.client.get(path=f"/surfit?category={category}")
        # then
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_올바르지_않은_query_param_키_값일_때_특정_카테고리의_링크_목록_반환_실패(self):
        """
        요청 url의 query param의 키 값이 'category'가 아닌 경우 400을 반환한다.
        """
        # given
        category = "빅데이터 · AI · 머신러닝"
        # when
        response = self.client.get(path=f"/surfit?wrong={category}")
        # then
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {"올바르지 않은 query param 입니다."})

    def test_존재하지_않는_카테고리를_요청한_경우_특정_카테고리의_링크_목록_반환_실패(self):
        """
        존재하지 않는 카테고리를 요청한 경우 응답 코드로 400을 반환한다.
        """
        # given
        category = "wrong"
        # when
        response = self.client.get(path=f"/surfit?category={category}")
        # then
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {"올바르지 않은 query param 입니다."})
