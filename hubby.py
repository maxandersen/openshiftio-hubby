from github import Github
import urllib
from time import sleep
import sys

# First create a Github instance:
g = Github("maxandersen", "<secret>")

# Then play with your Github objects:

repo = g.get_repo('openshiftio/openshift.io')

print "Fetching labels..."

all = [l for l in repo.get_labels()]

teams = [l for l in all if l.name.startswith('team/') or l.name.startswith ('stream/') ]
status = [l for l in all if l.name.startswith('status/') ]
areas = [l for l in all if l.name.startswith('area/') ]
types = [l for l in all if l.name.startswith('type/') ]
severities = [l for l in all if l.name.startswith('SEV') ]

leftover = [l for l in all if l not in teams and l not in status and l not in areas and l not in types and l not in severities]


#  https://github.com/openshiftio/openshift.io/issues?utf8=%E2%9C%93&q=is%3Aissue+is%3Aopen+label%3Ateam%2Fplatform+


queries = {
    "Missing team" : 'repo:openshiftio/openshift.io is:issue is:open ' + ' '.join(['-label:'+ t.name for t in teams]),
    "Missing types" : 'repo:openshiftio/openshift.io is:issue is:open ' + ' '.join(['-label:'+ t.name for t in types])
}




#print missingteam_url

print ".openshift.io"
print "|==="
    
header ="|Name"

for key in queries:
        query = queries[key] 
        params = { 'q' : query }
        query_url = "https://github.com/openshiftio/openshift.io/issues?" + urllib.urlencode(params)
        header = header + "|" + str(query_url) + "[" + key + "] " + str(g.search_issues(query).totalCount) 

pastresult = {}

print header
for t in teams:
    print "|" + t.name
    for key in queries:
        query = queries[key]  + " label:" + t.name
        params = { 'q' : query }
        query_url = "https://github.com/openshiftio/openshift.io/issues?" + urllib.urlencode(params)

        if key != 'Missing team':
            c =  str(g.search_issues(query).totalCount)
        else:
            c = "<ditto>"

        print "|" + str(query_url) + "[" + str(c) + "]"
        sleep(1)
        sys.stderr.write(t.name + " Wait for it...")


print "|==="
