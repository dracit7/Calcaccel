import configparser

def SetupConfig(path):
  config = configparser.RawConfigParser()
  config.read(path)
  return config

conf = SetupConfig('calcaccel/config/config.conf')