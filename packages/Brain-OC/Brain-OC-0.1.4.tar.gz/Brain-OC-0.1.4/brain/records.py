# coding=utf8
""" Brain Records

Handles the record structures for the Authorization service
"""

__author__		= "Chris Nasr"
__version__		= "1.0.0"
__maintainer__	= "Chris Nasr"
__email__		= "chris@ouroboroscoding.com"
__created__		= "2022-03-20"

# Python imports
from hashlib import sha1
import re
import pathlib

# Pip imports
from FormatOC import Tree
from RestOC import Conf, JSON, Record_MySQL, StrHelper

# Module variable
_moRedis = None

# Get the definitions path
_defPath = '%s/definitions' % pathlib.Path(__file__).parent.resolve()

def cache(redis=None):
	"""Cache

	Get/Set the cache instance

	Arguments:
		redis (StrictRedis): The instance to set, None for getting

	Returns:
		None|StrictRedis
	"""
	global _moRedis
	if not redis:
		return _moRedis
	else:
		_moRedis = redis

def install():
	"""Install

	Handles the initial creation of the tables in the DB

	Returns:
		None
	"""
	Key.table_create()
	Permissions.table_create()
	User.table_create()

class Key(Record_MySQL.Record):
	"""Key

	Represents a key for email verification, forgotten password, etc.

	Extends:
		Record_MySQL.Record
	"""

	_conf = None
	"""Configuration"""

	@classmethod
	def config(cls):
		"""Config

		Returns the configuration data associated with the record type

		Returns:
			dict
		"""

		# If we haven't loaded the config yet
		if not cls._conf:
			cls._conf = Record_MySQL.Record.generate_config(
				Tree.fromFile('%s/key.json' % _defPath),
				override={'db': Conf.get(('mysql', 'db'), 'brain')}
			)

		# Return the config
		return cls._conf

class Permissions(Record_MySQL.Record):
	"""Permissions

	Represents a single group of permissions associated with a user

	Extends:
		Record_MySQL.Record
	"""

	_conf = None
	"""Configuration"""

	@classmethod
	def clear(cls, _id):
		"""Clear

		Removes permissions from the cache by ID

		Arguments:
			_id (str): The ID of the user to remove

		Returns:
			None
		"""

		# Delete the key in Redis
		_moRedis.delete('perms:%s' % _id)

	@classmethod
	def config(cls):
		"""Config

		Returns the configuration data associated with the record type

		Returns:
			dict
		"""

		# If we haven't loaded the config yet
		if not cls._conf:
			cls._conf = Record_MySQL.Record.generate_config(
				Tree.fromFile('%s/permissions.json' % _defPath),
				override={'db': Conf.get(('mysql', 'db'), 'brain')}
			)

		# Return the config
		return cls._conf

	@classmethod
	def get(cls, _id=None, index=None, filter=None, match=None, raw=None, distinct=False, orderby=None, limit=None, custom={}):
		"""Get

		Returns records by primary key or index, can also be given an extra filter

		Arguments:
			_id (str|str[]): The primary key(s) to fetch from the table
			index (str): N/A in MySQL
			filter (dict): Additional filter
			match (tuple): N/A in MySQL
			raw (bool|list): Return raw data (dict) for all or a set list of
				fields
			distinct (bool): Only return distinct data
			orderby (str|str[]): A field or fields to order the results by
			limit (int|tuple): The limit and possible starting point
			custom (dict): Custom Host and DB info
				'host' the name of the host to get/set data on
				'append' optional postfix for dynamic DBs

		Returns:
			Record|Record[]|dict|dict[]
		"""

		global _moRedis

		# If we have an ID
		if _id:

			# If we have no index
			if not index:

				# If we have one ID
				if isinstance(_id, str):

					# Try to fetch it from the cache
					sPermissions = _moRedis.get('perms:%s' % _id)

					# If it's found
					if sPermissions:

						# Decode the data
						dPermissions = JSON.decode(sPermissions)

					# Else, permissions not found in cache
					else:

						# Fetch the record from the DB
						dPermissions = super().get(_id, raw=True, custom=custom)

						# Store it in the cache
						_moRedis.set('perms:%s' % _id, JSON.encode(dPermissions))

					# If we want raw data
					if raw:

						# If we want all data
						if raw is True:
							return dPermissions

						# Else return only specific fields
						return {k:dPermissions[k] for k in raw if k in dPermissions}

					# Else, create and return an instance
					return cls(dPermissions)

				# Else, if we have multiple IDs
				elif isinstance(_id, list):

					# Fetch multiple keys
					lPermissions = _moRedis.mget(['perms:%s' % k for k in _id])

					# Go through each one
					for i in range(len(_id)):

						# Generate the key
						sKey = 'perms:%s' % i

						# If we have a record
						if lPermissions[sKey]:

							# Decode it
							lPermissions[i] = JSON.decode(lPermissions[sKey])
							del lPermissions[sKey]

						else:

							# Fetch the record from the DB
							lPermissions[i] = super().get(_id[i], raw=True, custom=custom)

					# Store it in the cache
					_moRedis.set('perms:%s' % _id[i], JSON.encode(lPermissions[i]))

					# If we want raw
					if raw:

						# If we want all data
						if raw is True:
							return lPermissions

						# Else return only specific fields
						return [{k:dPermissions[k] for k in raw if k in d} for d in lPermissions]

					# Else, create and return an instances
					return [d and cls(d) or None for d in lPermissions]

		# Invalid use of get
		raise ValueError('Invalid use of Permissions.get')

class User(Record_MySQL.Record):
	"""User

	Represents a single user in the micro services system

	Extends:
		Record_MySQL.Record
	"""

	_conf = None
	"""Configuration"""

	@classmethod
	def cache(cls, _id, raw=False, custom={}):
		"""Cache

		Fetches the Users from the cache and returns them

		Arguments:
			_id (str|str[]): The ID(s) to fetch
			raw (bool): Return raw records or Users
			custom (dict): Custom Host and DB info
				'host' the name of the host to get/set data on
				'append' optional postfix for dynamic DBs

		Returns:
			User|User[]|dict|dict[]
		"""

		global _moRedis

		# If we got a single ID
		if isinstance(_id, str):

			# Fetch a single key
			sUser = _moRedis.get(_id)

			# If we have a record
			if sUser:

				# Decode it
				dUser = JSON.decode(sUser);

			else:

				# Fetch the record from the DB
				dUser = cls.get(_id, raw=True, custom=custom)

				# Store it in the cache
				_moRedis.set(_id, JSON.encode(dUser))

			# If we don't have a record
			if not dUser:
				return None

			# If we want raw
			if raw:
				return dUser

			# Return an instance
			return cls(dUser)

		# Else, fetch multiple
		else:

			# Init the return
			lRet = []

			# Fetch multiple keys
			lUsers = _moRedis.mget([k for k in _id])

			# Go through each one
			for i in range(len(_id)):

				# If we have a record
				if lUsers[i]:

					# Decode it
					lUsers[i] = JSON.decode(lUsers[i])

				else:

					# Fetch the record from the DB
					lUsers[i] = cls.get(_id[i], raw=True, custom=custom)

					# Store it in the cache
					_moRedis.set(_id[i], JSON.encode(lUsers[i]))

			# If we want raw
			if raw:
				return lUsers

			# Return instances
			return [d and cls(d) or None for d in lUsers]

	@classmethod
	def clear(cls, _id):
		"""Clear

		Removes a user from the cache

		Arguments:
			_id (str): The ID of the user to remove

		Returns:
			None
		"""

		# Delete the key in Redis
		_moRedis.delete(_id)

	@classmethod
	def config(cls):
		"""Config

		Returns the configuration data associated with the record type

		Returns:
			dict
		"""

		# If we haven't loaded the config yet
		if not cls._conf:
			cls._conf = Record_MySQL.Record.generate_config(
				Tree.fromFile('%s/user.json' % _defPath),
				override={'db': Conf.get(('mysql', 'db'), 'brain')}
			)

		# Return the config
		return cls._conf

	@staticmethod
	def password_hash(passwd):
		"""Password Hash

		Returns a hashed password with a unique salt

		Arguments:
			passwd (str): The password to hash

		Returns:
			str
		"""

		# Generate the salt
		sSalt = StrHelper.random(32, '_0x')

		# Generate the hash
		sHash = sha1(sSalt.encode('utf-8') + passwd.encode('utf-8')).hexdigest()

		# Combine the salt and hash and return the new value
		return sSalt[:20] + sHash + sSalt[20:]

	@classmethod
	def password_strength(cls, passwd):
		"""Password Strength

		Returns true if a password is secure enough

		Arguments:
			passwd (str): The password to check

		Returns:
			bool
		"""

		# If we don't have enough or the right chars
		if 8 > len(passwd) or \
			re.search('[A-Z]+', passwd) == None or \
			re.search('[a-z]+', passwd) == None or \
			re.search('[0-9]+', passwd) == None:

			# Invalid password
			return False

		# Return OK
		return True

	def password_validate(self, passwd):
		"""Password Validate

		Validates the given password against the current instance

		Arguments:
			passwd (str): The password to validate

		Returns:
			bool
		"""

		# Get the password from the record
		sPasswd = self.field_get('passwd')

		# Split the password
		sSalt = sPasswd[:20] + sPasswd[60:]
		sHash = sPasswd[20:60]

		# Return OK if the rehashed password matches
		return sHash == sha1(sSalt.encode('utf-8') + passwd.encode('utf-8')).hexdigest()

	@classmethod
	def simple_search(cls, query, custom={}):
		"""Simple Search

		Looks for query in multiple fields

		Arguments:
			query (str): The query to search for
			custom (dict): Custom Host and DB info
				'host' the name of the host to get/set data on
				'append' optional postfix for dynamic DBs

		Returns:
			str[]
		"""

		# Get the structure
		dStruct = cls.struct(custom)

		# Generate the SQL
		sSQL = "SELECT `_id`\n" \
				"FROM `%(db)s`.`%(table)s`\n" \
				"WHERE `first_name` LIKE '%%%(query)s%%'\n" \
				"OR `last_name` LIKE '%%%(query)s%%'\n" \
				"OR CONCAT(`first_name`, ' ', `last_name`) LIKE '%%%(query)s%%'\n" \
				"OR `email` LIKE '%%%(query)s%%'\n" \
				"OR `phone_number` LIKE '%%%(query)s%%'" % {
			'db': dStruct['db'],
			'table': dStruct['table'],
			'query': Record_MySQL.Commands.escape(dStruct['host'], query)
		}

		# Run the search and return the result
		return Record_MySQL.Commands.select(
			dStruct['host'],
			sSQL,
			Record_MySQL.ESelect.COLUMN
		)
