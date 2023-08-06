import mariadb
import sys

class ReMan(object):
	def __init__(self):
		self.connection = None
		self.cursor = None

	def __del__(self):
		if (self.cursor != None):
			self.cursor.close()
		if (self.connection != None):
			self.connection.close()

	def getDBConnection(self):
		try:
			if (self.connection == None):
				self.connection = mariadb.connect(
					user="reman",
					password="reman",
					host="10.58.3.179",
					database="REMAN")
			return self.connection
		except Exception as e:
			print(f"Failed to connect database, error: {e}")
			sys.exit(1)

	def getDBCursor(self):
		try:
			if (self.cursor == None):
				self.cursor = self.getDBConnection().cursor()
			return self.cursor
		except Exception as e:
			print(f"Failed to get database cursor, error: {e}")
			sys.exit(1)

	def getUserChannels(self, releaseName):
		result = None
		try:
			cursor = self.getDBCursor()
			cursor.execute("SELECT users.name, channels.name "
							 "FROM ReleaseChannel as rc "
							 "INNER JOIN Channels as channels ON rc.channelId = channels.id "
							 "INNER JOIN Users as users ON users.id = channels.userId "
							 "INNER JOIN Releases as releases ON  rc.releaseId = releases.id "
							 f"WHERE releases.name = '{releaseName}'"
							)
			result = self.getDBCursor().fetchall()
		except Exception as e:
			print(f"Failed to get user/channel of {releaseName}, error: {e}")
		return result

	def getChannel(self, releaseName, userName):
		result = None
		try:
			cursor = self.getDBCursor()
			cursor.execute("SELECT channels.name "
							 "FROM ReleaseChannel as rc "
							 "INNER JOIN Channels as channels ON rc.channelId = channels.id "
							 "INNER JOIN Users as users ON users.id = channels.userId "
							 "INNER JOIN Releases as releases ON  rc.releaseId = releases.id "
							 f"WHERE releases.name = '{releaseName}' "
							 f"AND users.name = '{userName}'"
							)
			rows = self.getDBCursor().fetchall()
			if (len(rows) == 1):
				result = rows[0][0]
			else:
				print("None or multiple version! " + len(rows))
		except Exception as e:
			print(f"Failed to get user/channel of {releaseName}, error: {e}")
		return result
		pass