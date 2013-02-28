import fmeobjects


class FMEPoints2lines(object):
    def __init__(self):
        self.busNumber = 0
        self.routeNumber = 0
        self.lastPoint = None

    def input(self,f):
        if int(f.getAttribute('BUS')) != self.busNumber:
            self.busNumber = int(f.getAttribute('BUS'))
            self.routeNumber = int(f.getAttribute('ROUTE'))
        elif int(f.getAttribute('ROUTE')) != self.routeNumber:
            self.routeNumber = int(f.getAttribute('ROUTE'))
        else:
            fNew = fmeobjects.FMEFeature()
            for a in f.getAllAttributeNames():
                fNew.setAttribute( a, f.getAttribute( a ))

            line = fmeobjects.FMELine()
            line.appendPoints([self.lastPoint, f.getCoordinate( 0 )])
 
            fNew.setGeometry(line)
            self.pyoutput( fNew )
        self.lastPoint = f.getCoordinate( 0 )

    def close(self):
        pass
