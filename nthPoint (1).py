from GUIconnection import GUIconnection
from Pt import Pt

## Simplify line data by keeping every other nth point
class nthPoint(GUIconnection):
   
     ## The name used in the GUI for this thinning method
     # @return a string containing the name used in the GUI
     def displayName(self):
         return("nthPoint")
     
     ## The name of the parameter required for this approach
     # @return a string containing the parameter name  
     def displayParameterName(self):
         return("n = ")
    
     ## Every n points are skipped to produce a thinned list of points
     # @param pts: A list of 2D points
     # @param sval: A string containing thevalue for n
     # @return A filtered list of 2D points
     def thinPoints(self, pts, sval):
          # All checking of parameters has been done in the lineSimplification class. Any exceptions will also be caught there
          val =int(sval)
          output = [pts[0]] # Always keep the first point.
          ct =0
          n = len(pts)
          for i in range(1,n):
               ct=ct + 1
               if ct==val:
                   output.append(pts[i])
                   ct=0
  
          return(output)
               
