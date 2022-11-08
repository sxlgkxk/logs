# 1. 代码功能
#	监听从int服务器发来的log
#
# 2. 补充说明
#
import requests
import json
import traceback
import sys
import time
import os
import shutil
import importlib
from flask import Flask, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app, supports_credentials=True)
json_dumps = lambda x: json.dumps(x, ensure_ascii=False, indent=4)


@app.route('/log', methods=['GET', 'POST'])
def log():
	queries = dict(request.args)
	body=request.get_data(as_text=True)
	curtime=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
	with open('content.txt', 'a') as f:
		f.write("{} || {} || {} \n".format(curtime, queries, body))
	return 'success'


@app.route('/view', methods=['GET'])
def view():
	# check password
	password = request.args.get('password')
	if password != '123456':
		return 'wa'

	with open('content.txt', 'r') as f:
		content = f.read()
		html='''<html>
		<head>
			<meta charset="utf-8">
			<title>logs</title>
		</head>
		<body>
			<table>
				<tr>
					<th>time</th>
					<th>queries</th>
					<th>body</th>
				</tr>
		'''
		lines=content.split('\n')
		for line in lines[::-1]:
			if line:
				timestr, queries, body = line.split(' || ')
				html += '''
					<tr>
						<td>{}</td>
						<td>{}</td>
						<td>{}</td>
					</tr>
				'''.format(timestr, queries, body)
		html += '''
			</table>
			<style>
				tr:nth-child(even) {background-color: #f2f2f2;}
				th, td {
					text-align: left;
					padding: 8px;
				}
			</style>
		</body>
		</html>
		'''

		if os.path.getsize('content.txt') > 1024 * 5:
			with open('content.txt', 'w') as f:
				newLines=lines[len(lines)//2:]
				f.write('\n'.join(newLines))
			
			bak_filename='content.txt.{}.bak'.format(int(time.time()))
			with open(bak_filename, 'w') as f:
				oldLines=lines[:len(lines)//2]
				f.write('\n'.join(oldLines))

		return html


app.run(host='0.0.0.0', port=9000, debug=True)
