import schedule
import time

from audio_video.audio_video_messages import AudioVideoMessage
from jw_news.jw_news_messages import JWNewsClient


if __name__ == '__main__':
    # AudioVideoMessage().schedule_audio_video_message()
    JWNewsClient().send_message()

    # while True:
    #     schedule.run_pending()
    #     time.sleep(1)
