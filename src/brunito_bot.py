import schedule
import time

from audio_video.audio_video_messages import AudioVideoMessage
from jw_news.jw_news_messages import JWNewsClient


def schedule_audio_video_message():
    """
    Schedule an audio video message to be sent to the user.
    """
    audio_video = AudioVideoMessage()
    schedule.every().monday.at("17:00").do(audio_video.send_message_new_week)
    schedule.every().thursday.at("18:30").do(audio_video.send_message_zoom)
    schedule.every().sunday.at("09:00").do(audio_video.send_message_zoom)


if __name__ == '__main__':
    # schedule_audio_video_message()
    JWNewsClient().send_message()

    # while True:
    #     schedule.run_pending()
    #     time.sleep(1)
