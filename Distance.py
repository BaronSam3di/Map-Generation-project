from GUIconnection import GUIconnection
from Pt import Pt

## Simplify line data using a distance threshold to filter out points
class Distance(GUIconnection):
     
     ## The name used in the GUI for this thinning method
     # @return a string containing the name used in the GUI
     def displayName(self):
         return("Distance")
    
     ## The name of the parameter required for this approach
     # @return a string containing the parameter name
     def displayParameterName(self):
         return("min distance")
    
     ## Points are thinned if too close to a previous point
     # @param pts: A list of 2D points
     # @param sval: A string containing the distance value
     # @return A filtered list of 2D points
     def thinPoints(self, pts, sval):
          # All checking of parameters has been done in the lineSimplification class. Any exceptions will also be caught there
          val = float(sval)
          output = [pts[0]]  # Always keep the first point.
          n = len(pts)
          curPt=pts[0] # This is the point we a measuring distances from
          for i in range(1,n):
              if curPt.EuclideanDistance(pts[i])>=val:
                   curPt=pts[i]
                   output.append(pts[i])

          return output

     
