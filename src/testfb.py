#! /usr/bin/env python
import sys
from FacebookMiner import FacebookMiner
token = 'AAADxUzUuwZCsBACi2ZCJIQ5gBwfg4jz8Rl58zxyojCWlEDbIXvBA7175Ez5ZAZByqKsmtRXZA1AZCoAs5kkW2oUU6MTdkffj1WNEF7dm2kb9ydPqStcQNI'
lat='25.019508699999996'
lng='121.54150682000002'
def main():
    facebook = FacebookMiner(token)
    print >> sys.stderr, facebook.find_places(lat,lng)
    return 0

if __name__ == '__main__':
    exit(main())
