import json

def getCoinRecords(jsonData,_id='id',_symbol='symbol',_name='name'):
	df=jsonData # didn't want to change the name
	res=[]
	for i in range(len(df)):
		res.append((
			df[i][_id],
			df[i][_symbol],
			df[i][_name]))
	return res
