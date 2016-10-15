import argparse

# Setup input arguments
arg_parser = argparse.ArgumentParser(description='Pi Controls options')
arg_parser.add_argument('--webserver', dest='runwebserver', action='store_true', help="Run Pi Controls web server")
args = vars(arg_parser.parse_args())

print(str(args))

