import time


def current_milli_time():
  return int(round(time.time() * 1000))


def get_timestamp_before_in_milliseconds(seconds):
  return (time.time() - seconds) * 1000
