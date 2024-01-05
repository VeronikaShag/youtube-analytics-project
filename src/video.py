from src.channel import Channel


class Video(Channel):
    """Класс для ютуб-видео"""

    def __init__(self, video_id: str) -> None:
        """Экземпляр инициализируется id видео. Дальше все данные будут подтягиваться по API."""
        self.__video_id = video_id

        video_response = self.get_service().videos().list(part='snippet,statistics,contentDetails,topicDetails',
                                                          id=self.__video_id
                                                          ).execute()

        self.video_title: str = video_response['items'][0]['snippet']['title']
        self.url: str = f'https://www.youtube.com/channel/{self.__video_id}'
        self.view_count: int = video_response['items'][0]['statistics']['viewCount']
        self.like_count: int = video_response['items'][0]['statistics']['likeCount']
        self.comment_count: int = video_response['items'][0]['statistics']['commentCount']

    def __str__(self):
        return self.video_title

    @property
    def video_id(self):
        return self.__video_id


class PLVideo(Video):
    """Класс для видео из плейлиста"""

    def __init__(self, video_id: str, playlist_id: str) -> None:
        super().__init__(video_id)

        self.__playlist_id = playlist_id
