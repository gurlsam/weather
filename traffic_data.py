import urllib

link_start = "https://traffic.cit.api.here.com/traffic/6.0/incidents.json?bbox="
link_end = "&app_id=UzNysjRSp2CNESp3p8sr&app_code=1NrX8nns29ndyrCzw2w2Ow&status=active&criticality=critical"
bbox_top_left = "47.665503,12.895546;"
bbox_bottom_right = "47.835744,13.148232"
link = link_start + bbox_top_left + bbox_bottom_right + link_end

f = urllib.urlopen(link)
myfile = f.read()

if len(myfile) != 0:
    print "Traffic!!! Ahhhhh"
else:
    print "The way is clear my friend"

import json
parsed = json.loads(myfile)
print
print json.dumps(parsed, indent = 4, sort_keys = True)

    
