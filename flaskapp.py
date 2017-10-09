import os
import boto3
import pymysql
import time
import MySQLdb
from azure.storage.blob import BlockBlobService
from azure.storage.blob import ContentSettings
from flask import Flask, request, send_from_directory, render_template

app = Flask(__name__)

block_blob_service = BlockBlobService(account_name='accoutName', account_key='accountKey')

blobStore = "blobStoreageURL"
localStore = "localPathToDefaultStorageOfFilesAndImages"

hostname = "azureHostName"
username = "azureUsername"
password = "azurePassword"
database = "azureDatabaseName"

mySQLCon = MySQLdb.connect(host="mysqlHostName", user="mysqlUsername", passwd="mysqlPassword", db="mysqlDBName")

def doQuery(mySQLCon, cityName, fare1, fare2):
    cur = mySQLCon.cursor()
    cur.execute("Query to fetch description of file/image") 
    return cur.fetchall()

@app.route('/', methods=['GET', 'POST'])
@app.route('/home')
def home():
    return render_template('index.html')


@app.route('/upload', methods=['GET', 'POST'])
def upload():
    objFile = request.files['thefile']
    filename = objFile.filename.encode('ascii', 'ignore')
    block_blob_service.create_blob_from_path(
    'image',
    filename,
    localStore + filename,
    content_settings=ContentSettings(content_type='image/png')
            )
    cur = mySQLCon.cursor()
    cur.execute("Insert query to store comments on files") 
    mySQLCon.commit()
    cur.execute("Comments count query")
    data = cur.fetchall()
    return render_template('index.html', 
                           upmessage = 'File Uploaded',
                           tblPics = data)

@app.route('/download', methods=['POST', 'GET'])
def download():
    fileName = request.form['nameOfFile'].encode('ascii', 'ignore')
    pathAndFileNames = os.path.join(saveToCloudDir, fileName)
    objS3 = s3Session.Object(bucket_name = s3BucketName, key = fileName)
    objResponse = objS3.get() 
    fileContent = objResponse['Body'].read()
    with open(pathAndFileNames, "w") as file:
        file.write(fileContent)
    #return send_from_directory(app.config[saveToCloudDir],
    #                           fileName,
    #                           as_attachment=True)
    return render_template('index.html',
                           downmessage = 'File Downloaded')

@app.route('/display', methods=['POST', 'GET'])
def display():
    cal1 = request.form['cal1'].encode('ascii', 'ignore')
    cal2 = request.form['cal2'].encode('ascii', 'ignore')
    cal3 = request.form['cal3'].encode('ascii', 'ignore')
    start = time.time()
    if(cal3 != ''):
        cur = mySQLCon.cursor()
        cur.execute("Custom queries to filter fetching files")
        data = cur.fetchall()
    else:
        cur = mySQLCon.cursor()
        cur.execute("Custom queries to filter fetching files")
        data = cur.fetchall()
    end = time.time()
    total = end - start
    return render_template('table.html', timetaken = str(total),
                           tblQuakes = data)

@app.route('/read', methods=['POST', 'GET'])
def readFile():
    start = time.time()
    cur = mySQLCon.cursor()
    cur.execute("Query to get all file names for tabluar purposes")
    data = cur.fetchall()
    end = time.time()
    total = end - start
    return render_template('table.html', timetaken = total, tblQuakes = data)
	
@app.route('/remove', methods=['POST', 'GET'])
def remFile():
    f = request.form['f'].encode('ascii', 'ignore')
    w = request.form['w'].encode('ascii', 'ignore')
    start = time.time()
    cur = mySQLCon.cursor()
    cur.execute("Query to delete comments and files")
    data = cur.fetchall()
    end = time.time()
    total = end - start
    cur = mySQLCon.cursor()
    cur.execute("Query to delete folder and links")
    mySQLCon.commit()
    return render_template('table.html', timetaken = str(total), tblQuakes = data)

@app.route('/Fatremove', methods=['POST', 'GET'])
def fatFile():
    start = time.time()
    cur = mySQLCon.cursor()
    cur.execute("Queries to check for duplicate/auto replicated files and removing of them")
    data = cur.fetchall()
    end = time.time()
    total = end - start
    return render_template('table.html', timetaken = "Removal Success")
