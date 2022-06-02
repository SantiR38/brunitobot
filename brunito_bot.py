import schedule
import time

from audio_video.messages import AudioVideoMessage


if __name__ == '__main__':
    audio_video = AudioVideoMessage()
    schedule.every().monday.at("17:00").do(audio_video.send_message_new_week)
    schedule.every().thursday.at("18:30").do(audio_video.send_message_zoom)
    schedule.every().sunday.at("09:00").do(audio_video.send_message_zoom)

    while True:
        schedule.run_pending()
        time.sleep(1)
