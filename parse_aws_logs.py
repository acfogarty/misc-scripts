import glob
import pandas as pd
import re
import json
from geolite2 import geolite2

# parse many AWS log files and output to csv
# http://docs.aws.amazon.com/AmazonS3/latest/dev/LogFormat.html


def parse_ip(ip):
    data = reader.get(ip)
    try:
        return data['location']['time_zone']
    except KeyError:
        print(ip)


logfile_glob = 'logs/*'

outputfilename = 'logs.csv'

column_names = ['Bucket_Owner', 'Bucket', 'Time1', 'Time2', 'Remote_IP', 'Requester', 'Request_ID', 'Operation', 'Key', 'Request-URI', 'HTTP_status', 'Error_Code', 'Bytes_Sent', 'Object_Size', 'Total_Time', 'Turn-Around_Time', 'Referrer', 'User-Agent', 'Version_Id']

time_format = '[%d/%b/%Y:%H:%M:%S'

reader = geolite2.reader()

dfs = []

logfiles = glob.glob(logfile_glob)

for logfile in logfiles:

    df = pd.read_csv(logfile, sep=' ', header=None, names=column_names)

    # timestamps get read into two separate columns because they contain a space
    # we only need the first part
    df['Time'] = pd.to_datetime(df['Time1'], format=time_format)

    # get country from IP
    df['Country'] = df['Remote_IP'].apply(parse_ip)

    df = df[~df['User-Agent'].str.contains('aws-internal')]
    dfs.append(df)

df = pd.concat(dfs)
df.to_csv(outputfilename, index=False)
