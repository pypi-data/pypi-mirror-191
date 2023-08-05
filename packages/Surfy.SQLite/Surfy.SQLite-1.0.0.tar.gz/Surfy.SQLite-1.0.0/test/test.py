import sys
import pandas as pd
sys.path.append(sys.path[0]+"/..")
from sqlite import DB

db = DB('test_db')
print('Create DB')

result = db.query('''CREATE TABLE IF NOT EXISTS test_table
			(id INTEGER PRIMARY KEY AUTOINCREMENT,
			data TEXT COLLATE NOCASE,
			extradata TEXT,
			counter INTEGER,
			realNumber REAL,
			object TEXT,
			array TEXT);''')

print('Create Table: {}'.format(result))

# cur = db.db.cursor()
# table = pd.read_sql_query("SELECT * FROM sqlite_master WHERE type='table' AND name='test_table';", db.db)
# print(table)


testTable = db.table('test_table')

print('Test Table: {}'.format(testTable))

insertedID = testTable.insertOne({
	'data': 'Some Data 1',
	'extradata': 'Some Extra Data',
	'counter': 2,
	'realNumber': 2.52,
	'object': {
		'field': 'value'
	},
	'array': [1,2,3]
})

print('Inserted ID: {}'.format(insertedID))

insertedIDs = testTable.insert([
	{ 'data': 'Some Data 2' },
	{ 'data': 'Some Data 3' },
	{ 'data': 'Some Data 4' },
	{ 'data': 'Some Data 5', 'extradata': 'CURRENT_TIME' },
])

print('Inserted IDs: {}'.format(insertedIDs))

result = testTable.findOne(
	{
		'data': 'Some Data 5'
	},
	{
		# 'fields': ['id', 'data']
	}
)

print('Find One:',result)

results = testTable.find(
	{
		'data': {
			'$like': 'Some Data%'
		}
	},
	{
		# 'fields': ['id', 'data']
	}
)

print('Find: ', results)



db.remove()