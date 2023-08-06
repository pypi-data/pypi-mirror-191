# coding=utf8
""" Brain

Handles authorization / user requests
"""

__author__		= "Chris Nasr"
__version__		= "1.0.0"
__copyright__	= "Ouroboros Coding Inc."
__email__		= "chris@ouroboroscoding.com"
__created__		= "2022-08-25"

# Python imports
import os
import platform
import sys

# Pip imports
from body import access, errors, users
from RestOC import Conf, EMail, Record_MySQL, REST, Services, Session

# Module imports
from . import Brain
from . import records

def cli():
	"""CLI

	Called from the command line to run from the current directory

	Returns:
		uint
	"""

	# Load the config
	Conf.load('config.json')
	sConfOverride = 'config.%s.json' % platform.node()
	if os.path.isfile(sConfOverride):
		Conf.load_merge(sConfOverride)

	# Get Brain config
	dConfig = Conf.get('brain', {
		'user_default_locale': 'en-US',
		'mysql_host': 'brain',
		'redis_host': 'brain'
	})

	# Add the global prepend
	Record_MySQL.db_prepend(Conf.get(('mysql', 'prepend'), ''))

	# Add the primary mysql DB
	Record_MySQL.add_host('brain', Conf.get(('mysql', 'hosts', dConfig['mysql_host']), {
		'host': 'localhost',
		'port': 3306,
		'charset': 'utf8',
		'user': 'root',
		'passwd': ''
	}))

	# If we are installing
	if len(sys.argv) > 1 and sys.argv[1] == 'install':
		return install(dConfig)

	# Init the email module
	EMail.init(Conf.get('email', {
		'error_to': 'errors@localhost',
		'from': 'admin@localhost',
		'smtp': {
			'host': 'localhost',
			'port': 587,
			'tls': True,
			'user': 'noone',
			'passwd': 'nopasswd'
		}
	}))

	# Get redis session config
	dRedis = Conf.get(('redis', 'session'), {
		'host': 'localhost',
		'port': 6379,
		'db': 0,
		'charset': 'utf8'
	})

	# Init the Session module
	Session.init(dRedis)

	# Get the REST config
	dRest = Conf.get('rest', {
		'allowed': 'localhost',
		'default': {
			'domain': 'localhost',
			'host': '0.0.0.0',
			'port': 8800,
			'protocol': 'http',
			'workers': 1
		},
		'services': {
			'brain': {'port': 0},
			'mouth': {'port': 1}
		}
	})

	# Create the REST config instance
	oRestConf = REST.Config(dRest)

	# Set verbose mode if requested
	if 'VERBOSE' in os.environ and os.environ['VERBOSE'] == '1':
		Services.verbose()

	# Get all the services
	dServices = {k:None for k in dRest['services']}

	# Add this service
	dServices['brain'] = Brain()

	# Register all services
	Services.register(
		dServices,
		oRestConf,
		Conf.get(('services', 'salt')),
		Conf.get(('services', 'internal_key_timeout'), 10)
	)

	# Create the HTTP server and map requests to service
	REST.Server({

		'/permissions': {'methods': REST.READ | REST.UPDATE, 'session': True},
		'/permissions/add': {'methods': REST.CREATE, 'session': True},

		'/search': {'methods': REST.READ, 'session': True},

		'/session': {'methods': REST.READ, 'session': True},

		'/signin': {'methods': REST.POST},
		'/signout': {'methods': REST.POST, 'session': True},

		'/user': {'methods': REST.CREATE | REST.READ | REST.UPDATE, 'session': True},
		'/user/email': {'methods': REST.UPDATE, 'session': True},
		'/user/email/verify': {'methods': REST.UPDATE},
		'/user/names': {'methods': REST.READ, 'session': True},
		'/user/passwd': {'methods': REST.UPDATE, 'session': True},
		'/user/passwd/forgot': {'methods': REST.CREATE | REST.UPDATE},
		'/user/setup': {'methods': REST.READ | REST.UPDATE},
		'/users/by/email': {'methods': REST.READ},
		'/users/by/id': {'method': REST.READ},

		'/verify': {'methods': REST.READ, 'session': True},

		},
		'brain',
		'https?://(.*\\.)?%s' % Conf.get(('rest', 'allowed')).replace('.', '\\.'),
		error_callback=errors.service_error
	).run(
		host=oRestConf['brain']['host'],
		port=oRestConf['brain']['port'],
		workers=oRestConf['brain']['workers'],
		timeout='timeout' in oRestConf['brain'] and oRestConf['brain']['timeout'] or 30
	)

	# Return OK
	return 0

def install(conf):
	"""Install

	Installs required files, tables, records, etc. for the service

	Arguments:
		conf (dict): The brain config

	Returns:
		int
	"""

	# Install tables
	records.install()

	# If we don't have an admin
	if not records.User.exists('admin@ouroboroscoding.com', index='email'):

		# Install admin
		oUser = records.User({
			'email': 'admin@ouroboroscoding.com',
			'passwd': records.User.password_hash('Admin123'),
			'locale': conf['user_default_locale'],
			'first_name': 'Admin',
			'last_name': 'Istrator'
		})
		sUserId = oUser.create(changes={'user': users.SYSTEM_USER_ID})

		# Add admin permission
		oPermissions = records.Permissions({
			'_user': sUserId,
			'rights': {
				'brain_user': access.CREATE | access.READ | access.UPDATE,
				'brain_permission': access.READ | access.UPDATE
			}
		})
		oPermissions.create(changes={'user': users.SYSTEM_USER_ID})

	# Return OK
	return 0

# Only run if called directly
if __name__ == '__main__':
	sys.exit(cli())
