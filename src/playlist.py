import os
import datetime

import isodate
from googleapiclient.discovery import build

from src.channel import Channel


class PlayList(Channel):

    def __init__(self, playlist_id: str):
        self.__playlist_id = playlist_id

        playlist_videos = self.get_service().playlists().list(id=self.__playlist_id, part='snippet').execute()
        self.title: str = playlist_videos['items'][0]['snippet']['title']
        self.url: str = f'https://www.youtube.com/playlist?list={self.__playlist_id}'

        playlist_videos = self.get_service().playlistItems().list(playlistId=self.__playlist_id,
                                                                  part='contentDetails',
                                                                  maxResults=50,
                                                                  ).execute()

        # получить все id видеороликов из плейлиста
        video_ids: list[str] = [video['contentDetails']['videoId'] for video in playlist_videos['items']]

        self.video_response = self.get_service().videos().list(part='contentDetails,statistics',
                                                               id=','.join(video_ids)
                                                               ).execute()

    def print_infoo(self):
        api_key = os.getenv('YT_API_KEY')
        youtube = build('youtube', 'v3', developerKey=api_key)
        channel = youtube.playlistItems().list(playlistId=self.__playlist_id,
                                               part='snippet,contentDetails',
                                               maxResults=50,
                                               ).execute()
        print(channel)

    @property
    def total_duration(self):
        """ возвращает объект класса datetime.timedelta с суммарной длительность плейлиста """

        duration = datetime.timedelta()

        for video in self.video_response['items']:
            # YouTube video duration is in ISO 8601 format
            iso_8601_duration = video['contentDetails']['duration']
            duration += isodate.parse_duration(iso_8601_duration)
        return duration

    def show_best_video(self):
        """ возвращает ссылку на самое популярное видео из плейлиста (по количеству лайков) """
        best_video_like_count = 0
        best_video_id = ''
        for video in self.video_response['items']:
            if int(video['statistics']['likeCount']) > best_video_like_count:
                best_video_like_count = int(video['statistics']['likeCount'])
                best_video_id = video['id']
        return f'https://youtu.be/{best_video_id}'
