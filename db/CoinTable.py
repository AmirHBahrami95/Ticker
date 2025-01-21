import sqlite3 as sq

class CoinTable(object):
	
	# --------------------------------------------------------------- init
	def __createTable(self):
		crs=self.__con.cursor()
		crs.execute("""
			create table if not exists coin(
				id integer primary key,
				symbol varchar(16) not null,
				name varchar(64) not null
			)
		""")
	
	# call it when used outside of "with" clause
	def init(self):
		self.__con=sq.connect(self.path_to_db)
		self.__createTable()
	
	# call it when used outside of "with" clause
	def close(self):
		if self.__con is not None:
			self.__con.close()
	
	def __init__(self,path_to_db):
		self.path_to_db=path_to_db
	
	# --------------------------------------------------------------- insert
	def insert(self,record):
		"""('90', 'BTC', 'Bitcoin')"""
		try:
			crs=self.__con.cursor()
			crs.execute("inert into coin values(?,?,?)",record)
			self.__con.commit()
		except:
			pass
	
	def insertN(self,records_list):
		"""[('90', 'BTC', 'Bitcoin'),]"""
		try:
			crs=self.__con.cursor()
			crs.executemany("insert into coin values(?,?,?)",records_list)
			self.__con.commit()
		except:
			pass
	
	# --------------------------------------------------------------- select
	def __getBy(self,key,val):
		crs=self.__con.cursor()
		crs.execute("select * from coin where {}='{}'".format(key,val))
		return crs.fetchall()
	
	def getById(self,val):
		return self.__getBy('id',val)
	
	def getBySymbol(self,val):
		return self.__getBy('symbol',val)
	
	def getByName(self,val):
		return self.__getBy('name',val)
	
	def getAll(self):
		crs=self.__con.cursor()
		crs.execute("select * from coin")
		return crs.fetchall()

	# --------------------------------------------------------------- closable
	def __enter__(self):
		self.init()
		return self

	def __exit__(self,exc_type, exc_value, traceback):
		self.close()

	# --------------------------------------------------------------- closable

	def printCoins(self,tupleList):
		for tup in tupleList:
			print(tup)
