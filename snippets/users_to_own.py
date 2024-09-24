import argparse
import os
import logging
import sys

parser = argparse.ArgumentParser(
    prog='users_to_owned',
    description='Generate a Neo4J request to own a list of users'
)

parser.add_argument('users_file', action='store', help='User file containing usernames')
parser.add_argument('domain', action='store', help='Domain name (FQDN)')


args = parser.parse_args()

if not os.path.isfile(args.users_file):
	logging.error("File {} doesn't exist".format(args.users_file))
	sys.exit(1)

if "." not in args.domain:
	logging.error("Fully qualified domain name is required")
	sys.exit(1)

users_file = args.users_file

domain = args.domain.upper()

with open(users_file, 'r') as f:
	users = " OR ".join(["u.name=\"{}@{}\"".format(user.rstrip('\n').upper(), domain) for user in f])

print("MATCH (u:User) WHERE {} SET u.owned=true RETURN u".format(users))
