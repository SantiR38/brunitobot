import schedule
import time

from audio_video.audio_video_messages import AudioVideoMessage
from jw_news.jw_news_messages import JWNewsClient


if __name__ == '__main__':
    AudioVideoMessage().schedule_tasks()
    JWNewsClient().schedule_tasks()

    while True:
        schedule.run_pending()
        time.sleep(1)
