import configparser

def SetupConfig(path):
  # Read and parse the config file to a dict.
  config = configparser.RawConfigParser()
  config.read(path)
  return config

# Other files may import this variable to get all configurations.
conf = SetupConfig('calcaccel/config/config.conf')