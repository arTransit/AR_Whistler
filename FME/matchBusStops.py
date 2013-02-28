import fmeobjects

class FMECalculateDifference(object):
    def __init__(self):
        self.logger = fmeobjects.FMELogfile()

    def input(self,feature):
        # Get feature attributes
        self.stopAngle = feature.getListAttribute('close{}.STANGLE')
        self.bearing = feature.getAttribute('BEARING')
        
        # Create new list to store list calculation values
        divergence = []
        
        # Calculate the entry angle onto the bus as being 90 degrees left of the current bearing
        # Boarding angle is equal to the direction one would be facing standing on the sidewalk
        # facing the front door of the bus 
        
        boardingAngle = (float( self.bearing ) -90) %360
        '''
        if self.bearing >= 90:
            boardingAngle = float(self.bearing) -90
        else:
            boardingAngle = float(self.bearing) + 270
        '''
        
        # For each stop within the 60m radius defined by the neighbour finder determine the difference between the 
        # Stop angle and the boarding angle.  0 indicates a perfect match
        
        for n in self.stopAngle:
            divergence.append( abs( boardingAngle - float(n) ) %360 )
            '''
            if boardingAngle < 45 and float(n) > 315:
                divergence.append(abs(float(boardingAngle)-float(n)+360))
            if boardingAngle > 315 and float(n) < 45:
                divergence.append(abs(float(boardingAngle)-float(n)-360))
            else:
                divergence.append(abs(float(boardingAngle)-float(n)))
            '''
        
        # determine the index of the closest match    
        minDivergence = min(divergence)
        minIndex = divergence.index(minDivergence)
        if minDivergence < 90:
            #Return the STOPID of the closest match
            match = feature.getAttribute('close{'+str(minIndex)+'}.STOPID')
            feature.setAttribute('MATCH',match)
        feature.setListAttribute('DIVERGENCE{}.divergence',divergence)    
        feature.setAttribute('BANGLE',boardingAngle)
        feature.setAttribute('DIVERGENCE',minDivergence)
        self.pyoutput(feature)

