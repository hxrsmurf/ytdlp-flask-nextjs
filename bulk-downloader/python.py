import argparse
parser = argparse.ArgumentParser()
parser.add_argument("--channel", "-c")
args = parser.parse_args()
print('Hello World')
print(args.channel)