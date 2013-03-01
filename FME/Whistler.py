import fmeobjects
import bisect

""" Global Variables
"""
# NEEDED_ATTRIBUTES=['APC{0}.LON','APC{0}.LAT','APC{0}.TIMESTAMP','APC{1}.LON','APC{1}.LAT','APC{1}.TIMESTAMP']
LOGIT=1


class FMEmatchAPC(object):
    def __init__(self):
        self.apcTimes = {}
        self.apcIDs = {}
        self.gfiData = []
        
        self.logger = fmeobjects.FMELogFile()

    def logging(self, m):
        if LOGIT: self.logger.logMessageString( str(m) )

        
    def input(self,f):
        if f.getAttribute('_SOURCE') == 'GFI':
            self.gfiData.append( f )
        elif f.getAttribute('_SOURCE') == 'APC':
            busID = int( f.getAttribute('BUSID') )
            if busID not in self.apcTimes.keys():
                self.apcTimes[ busID ] = []
                self.apcIDs[ busID ] = []
            self.apcTimes[ busID ].append( int(f.getAttribute('TIMESTAMP')) )
            self.apcIDs[ busID ].append( int(f.getAttribute('_ID')) )
        else:
            self.logging("FMEmatchAPC: Unknown feature.")


    def close(self):
        self.logging("FMEmatchAPC: Processing...")
        self.logging("FMEmatchAPC: gfiData %s" % len(self.gfiData) )
        
        for gfi in self.gfiData:
            self.logging("\nFMEmatchAPC: working on %s %s" % (
                    gfi.getAttribute( 'BUS' ),gfi.getAttribute( 'TIMESTAMP' )))
            
            busID = int( gfi.getAttribute('BUS') )
            i = bisect.bisect_right( self.apcTimes[ busID ], 
                    int( gfi.getAttribute( 'TIMESTAMP' )) ) -1
            self.logging("\nFMEmatchAPC: index %d" % i)
            if i >=0 :
                gfi.setAttribute( '_APCMATCHID', 
                        self.apcIDs[ busID ][i])
            else :
                gfi.setAttribute( '_APCMATCHID', 0)
            
            self.pyoutput( gfi )



                
