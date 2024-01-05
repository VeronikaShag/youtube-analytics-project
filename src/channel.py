import json
import os
from googleapiclient.discovery import build


class Channel:
    """Класс для ютуб-канала"""

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        self.__channel_id = channel_id


        channel = self.get_service().channels().list(id=self.__channel_id, part='snippet,statistics').execute()

        self.title = channel['items'][0]["snippet"]["title"]
        self.description = channel['items'][0]["snippet"]["description"]
        self.video_count = channel['items'][0]["statistics"]["videoCount"]
        self.url = f'https://www.youtube.com/channel/{self.__channel_id}'
        self.view_count = channel['items'][0]["statistics"]["viewCount"]
        self.subscriberCount = channel['items'][0]["statistics"]["subscriberCount"]


    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        api_key = os.getenv('YT_API_KEY')
        youtube = build('youtube', 'v3', developerKey=api_key)
        channel = youtube.channels().list(id=self.__channel_id, part='snippet,statistics').execute()
        print(channel)

    @classmethod
    def get_service(cls):
        """
        класс-метод, возвращающий объект для работы с YouTube API
        """
        api_key = os.getenv('YT_API_KEY')
        youtube = build('youtube', 'v3', developerKey=api_key)
        return youtube

    def to_json(self, filename: str) -> None:
        """
        метод, сохраняющий в файл значения атрибутов экземпляра Channel
        """
        data = {
            "channel_id": self.__channel_id,
            "title": self.title,
            "description": self.description,
            "url": self.url,
            "subscriberCount": self.subscriberCount,
            "video_count": self.video_count,
            "view_count": self.view_count
        }
        with open(filename, 'w') as f:
            json.dump(data, f)
