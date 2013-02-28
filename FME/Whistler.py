import fmeobjects

""" Global Variables
"""
# NEEDED_ATTRIBUTES=['APC{0}.LON','APC{0}.LAT','APC{0}.TIMESTAMP','APC{1}.LON','APC{1}.LAT','APC{1}.TIMESTAMP']
LOGIT=0


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
            if f.getAttribute('BUSID') not in apcTimes.keys():
                apcTimes[ f.getAttribute('BUSID') ] = []
                apcIDs[ f.getAttribute('BUSID') ] = []
            self.apcTimes[ f.getAttribute('BUSID') ].append(f.getAttribute('TIMESTAMP'))
            self.apcIDs[ f.getAttribute('BUSID') ].append(f.getAttribute('TIMESTAMP'))
        else:
            self.logging("FMEmatchAPC: Unknown feature.")


    def close(self):
        currentBus = 0
        currentTime = 0
        currentApc = self.apcData.pop(0)
        lastApc = None
        
        self.logging("FMEmatchAPC: Processing...")
        self.logging("FMEmatchAPC: gfiData %s" % len(self.gfiData) )
        
        for gfi in self.gfiData:
            self.logging("\nFMEmatchAPC: working on %s %s" % (
                    gfi.getAttribute( 'BUS' ),gfi.getAttribute( 'TIMESTAMP' )))
            
            i = bisect.bisect_right( self.apcTimes[ gfi.getAttribute('BUSID') ], 
                    gfi.getAttribute( 'TIMESTAMP' )) -1
            if i >=0 :
                g.setAttribute( '_APCMATCHID', 
                        self.apcIDs[ gfi.getAttribute('BUSID') ][i])
            else :
                g.setAttribute( '_APCMATCHID', 0)
            
            self.pyoutput( gfi )



                
