import math
import fmeobjects

LOGIT = 0


# DISTANCE BEARING SPEED DTIME BEARINGTREND
class FMETelemetry(object):
  
    def __init__(self):
        # Variables to pass attribute values from one feature to the next.
        self.currentBusday = 0
        self.currentBus = 0
        self.currentRoute = 0
        
        self.currentTimestamp = 0.0
        self.currentX = 0.0
        self.currentY = 0.0
        self.currentBearing = 0.0
        self.currentTrend = 0.0
        self.currentSpeed = 0.0
        '''
        self.pX = 0                             
        self.pY = 0
        self.pBus = 0
        self.pEpoch = 0
        self.pSpeed = 0
        
        self.pBearing = 0
        self.pTrend = 0
        '''
        self.logger = fmeobjects.FMELogFile()

    def logging(self, m):
        if LOGIT: self.logger.logMessageString( str(m) )
        
    def input(self,f):
        # Variables to store current attribute values.
        newBus = int(f.getAttribute("BUS"))
        newBusday = int(f.getAttribute("BUSDAY"))
        newRoute = int(f.getAttribute("ROUTE"))
        newTimestamp = float(f.getAttribute("TIMESTAMP"))
        newX,newY = f.getCoordinate( 0 )
       
        # If this is the first record for this bus the bus has not moved
        if (self.currentBusday,self.currentBus,self.currentRoute) != (newBusday,newBus,newRoute):
            f.setAttribute("DISTANCE",0)
            f.setAttribute("BEARING",0)
            f.setAttribute("SPEED",0)
            f.setAttribute("ELAPSED", 0)
            f.setAttribute("DTREND", 0)

            self.currentTimestamp = 0.0
            self.currentBearing = 0.0
            self.currentTrend = 0.0
            self.currentSpeed = 0.0            
            self.currentX,self.currentY = newX,newY

            self.currentBus = newBus
            self.currentBusday = newBusday
            self.currentRoute = newRoute

            ##self.speed = 0
            ##self.bearingDeg = 0
        #If this is the not the first record for this bus we can calculate it's movement
        else:
            # Calculate the elapsed time between records in seconds
            dTime = newTimestamp - self.currentTimestamp
            f.setAttribute("ELAPSED", dTime)
            ##feature.setAttribute("ELAPSED",self.elapsed)
            
            if dTime > 0:
                # Delta X / Delta Y
                self.logging("getting DX DY")
                dX = math.sqrt(math.pow((newX - self.currentX),2))
                dY = math.sqrt(math.pow((newY - self.currentY),2))
        
                # Calculate distance pythagoreas
                self.logging("getting distance")
                distance = float(math.sqrt( math.pow(dX,2) + math.pow(dY,2)))
                f.setAttribute("DISTANCE",distance)
                
                if distance > 20:
                    
                    # Calculate bearing using trigonometry.
                    # bearingRad = math.atan2( dY,dX )
                    newBearing = math.degrees( math.atan2( dY,dX ) ) 
                    
                    # Determine quadrant and add corresponding number of degrees
                    if float(newX)-float(self.currentX) > 0 and float( newY )-float(self.currentY ) >0:    
                        newBearing = 90 - newBearing
                    elif float(newX)-float(self.currentX) > 0 and float( newY )-float(self.currentY ) <0:
                        newBearing = newBearing + 90
                    elif float(newX)-float(self.currentX) < 0 and float( newY )-float(self.currentY ) <0:
                        newBearing = 270 - newBearing
                    elif float(newX)-float(self.currentX) < 0 and float( newY )-float(self.currentY ) >0:
                        newBearing = 270 + newBearing  
                    
                    f.setAttribute("BEARING", newBearing)
            
                    #Calculate speed
                    speed = distance/dTime *3.6
                    f.setAttribute("SPEED", speed)
                    
                    dTrend = (newBearing + self.currentBearing)/2
                    f.setAttribute("DTREND", dTrend)
                    self.currentBearing = newBearing
                    self.currentTrend = dTrend
                    self.currentSpeed = speed
                else:
                    f.setAttribute("BEARING", self.currentBearing)
                    f.setAttribute("DTREND", self.currentTrend)
                    f.setAttribute("SPEED", self.currentSpeed)
            
            # if there is no elapsed time between records SPEED and BEARING are equal to the previous record
            else:
                f.setAttribute("DISTANCE", 0)
                f.setAttribute("BEARING", self.currentBearing)
                f.setAttribute("SPEED", self.currentSpeed)
                f.setAttribute("ELAPSED", 0)
                f.setAttribute("DTREND", self.currentTrend)
        
        #Pass variables to the next feature    
        self.currentX,self.currentY = newX,newY
        self.currentTimestamp = newTimestamp
        #currentSpeed = speed
        
        self.pyoutput( f )
    
    def close(self):
         pass

