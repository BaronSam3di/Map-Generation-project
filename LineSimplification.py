## ISD Term 2 Coursework 2

from tkinter import Frame, Entry, Menu, Canvas, Label, Listbox, StringVar, Button, END, RIDGE, E
from tkinter.messagebox import showerror, showinfo
from tkinter.filedialog import askopenfilename, asksaveasfilename


from GUIconnection import GUIconnection
from Pt import Pt

# Amend here to add/remove a plugin
# Note that the remainder of this file does not explicitly refer to these classes.
# In particular look at the method _Process, which relies on polymorphism to select the appropriate thining approach 

from Distance import Distance
from nthPoint import nthPoint
mPluginsAvailable = {"Distance":Distance(), "nthPoint":nthPoint()}
DisplayNameToClass = {Distance().displayName():Distance(), nthPoint().displayName():nthPoint()}
# The above lines could be improved by automating the import (which is beyond the scope of this module)
# and consequently automating the construction of the 2 dictionaries. Well done to those who achieved this level of automation!


## GUI for line simplification
class LineSimplification(Frame):
    
    CANVAS_SIZE = 400  # Square Region used to display image
    PLUGIN_FILE = 'plugins.txt'# Assumed to be located in the same directory as the main program
    
    def __init__(self, master=None):

        Frame.__init__(self, master)
        self.grid()
        self.master.title("Line Simplification")

        self._simplify = None   # Method used to simplify data
        self._data = []         # Loaded Data, a list of class Pt. This will not change until a new data file is loaded
        self._displayData = []  # Data to display, a list of class Pt. This is the result of the simplification

        # Menu has load/save options only
        self.mbar = Menu(self)
        self.master.config(menu=self.mbar)
        self.filemenu = Menu(self.mbar, tearoff=0)
        self.mbar.add_cascade(label="File", menu=self.filemenu)

        self.filemenu.add_command(label="Open", command=self.getfile)
        self.filemenu.add_command(label="Save", command=self.savefile)


        # All the entry widgets are placed on a frame, to separate them from the canvas
        frame = Frame(self)
        frame.grid(row=0, column=0, sticky="n")

        Label(frame, text="Select Method").grid(row=0, column=0)


        #For the listbox add all the available methods that are referred to in  plugins.txt
        self.listbox = Listbox(frame,  height=3)
        self.listbox.grid(row=0, column=1)

        lines = self.GetSimplificationMethods()
        
        numPlugins = len(lines)
        for item in lines:
            try:
                self.listbox.insert(END, mPluginsAvailable[item].displayName())
            except KeyError:  #ignore any plugins that are not available
                pass

        self.listbox.bind('<<ListboxSelect>>', self.SelectMethod)


        #Have the ability to change the parameter name depending on the selected method
        self._parameterName = StringVar()
        self._parameterName.set("")
        self._lbl_parameter = Label(frame, textvariable=self._parameterName, width=10, anchor=E)
        self._lbl_parameter.grid(row=0, column=2)
       
        
        #Text entry for simplification parameter
        self._parameterValue = StringVar()
        self._parameterValue.set("")
        self._paramEntry = Entry(frame, textvariable=self._parameterValue, width=5)
        self._paramEntry.grid(row=0, column=3)
    
        #Perform the simplification Button
        self._processButton = Button(frame, text="Process", command=self.Process, padx=5)
        self._processButton.grid(row=0, column=4, padx=5)
        
        #Finally the canvas that is used to display an image. It is placed directly under the frame containing all the entry widgets
        self._cnv = Canvas(
            self, bg="white", width=self.CANVAS_SIZE, height=self.CANVAS_SIZE, relief=RIDGE)
        self._cnv.grid(row=1, column=0)

    ## Reads plugin.txt for list of available thinning methods
    # @return a list of names
    #
    def GetSimplificationMethods(self):
        try:
            with open(self.PLUGIN_FILE) as f:
                lines = f.readlines()
                del lines[0]  # remove the header line
                for i in range(len(lines)):

                    lines[i] = lines[i].strip()  #remove new line character
        except IOError:
            lines = []
        return (lines)
   
    ## Thin the dataset and display the result
    #
    def Process(self):
        if len(self._data) > 0:   #Don't do anything if there is no data
            try:
                self._displayData = self.method.thinPoints(self._data, self._parameterValue.get())
            except:
                self._displayData = self._data.copy()
        self.Display()

    ## Set state variables when a thinning method has been selected from the listbox
    # @param event: the listbox event 
    #
    def SelectMethod(self, event): 
        a = self.listbox.curselection()
        if a != ():
            try:
                print(self.listbox.get(a))
                self.method = DisplayNameToClass[self.listbox.get(a)]
                self._parameterName.set(self.method.displayParameterName())
            except KeyError:
                showerror('Error!', "Simplification Method Unavailable")
    
    ## Determine the range of x and y values to ensure the image is displayed within the canvas
    # @return  a tuple containing the  minimum  value and a scale for both x and y directions
    #
    def GetdisplayDataScaleAndMin(self):
        minx = self._displayData[0].getX()  #lots of repetition here! Could be made more succinct. This could involve automating the getX() and getY() (which outside the scope of this module)
        miny = self._displayData[0].getY()
        maxx = minx
        maxy = miny
        for p in self._displayData:
            x = p.getX() 
            y = p.getY()
            if x < minx:
                minx = x
            elif x > maxx:
                maxx = x
            if y < miny:
                miny = y
            elif y > maxy:
                maxy = y

        scalex = (maxx - minx)
        if scalex == 0:
            scalex = 1
        scaley = (maxy - miny)
        if scaley == 0:
            scaley = 1

        return (minx, scalex, miny, scaley)
    
    
    ## Display data on screen
    #
    def Display(self):
        self._cnv.delete("all")  #Make sure the canvas is clear before adding to it
        if self._displayData != []:
            minx, scalex, miny, scaley = self.GetdisplayDataScaleAndMin()

            polygon = [] # object is displayed as a polygon. This means it will form a closed loop
            for p in self._displayData:
                x = p.getX()
                y = p.getY()

                x = ((self.CANVAS_SIZE-1) * (x - minx) / scalex) + 1#minor tweak to make sure smallest value is not on the boundary
                y = (self.CANVAS_SIZE) - (
                    (self.CANVAS_SIZE - 1) * (y - miny) / scaley) + 1  #minor tweak to make sure highest point is not on the boundary
                polygon.append(x)
                polygon.append(y)

            self._cnv.create_polygon(polygon, fill="", outline="black")

    ## (x,y) point data loaded and sorted into numeric order then displayed
    #
    def loadData(self, filename):
        dct = {}
        with open(filename) as f:
            lines = f.readlines()
            for l in lines:
                words = l.split(",")
                #Each line has the form "id",x,y    
                #Where id is the sequential index for the list of points
                #These lines are not necessarily in index order
                dct[int(words[0].strip('"'))] = Pt(float(words[1]), float(words[2]))

        #sort by "id"
        self._data = []
        for key in sorted(dct):
            self._data.append(dct[key])

        self._displayData = self._data.copy()
        self.Display()
   
   
    ## Display data saved with a new ordering value that is based on each data point's list index
    # @param filename The name and path of the file to (over)write.
    def saveData(self, filename):
        try:
            with open(filename, "w") as f:
                for i in range(len(self._displayData)):
                
                    f.write(
                        '"' + str(i + 1) + '",' + str(self._displayData[i].getX()) + ',' +
                        str(self._displayData[i].getY()) + "\n")
        except:
             showerror('Error!', "Failed to Save")   
   
   
    ## Select a file to open. This will result in data already opened to be removed
    #
    def getfile(self):
        f = askopenfilename(parent=self, title="Please select a file")
        if (len(f) > 0): # Ensure that the cancel button has not been pressed
            try:
                self.loadData(f)
            except Exception:
                showerror('Error!', "File could not be read")
                self._data = []   #reset all the data
                self._displayData = []
                self.Display()
    
    
    ## Select a file to save processed data to.
    #             
    def savefile(self):
        if self._displayData == []:
            showinfo("Save", "There is nothing to save!")
        else:
            filename = asksaveasfilename(parent=self)
            if filename is "": # Ensure that the cancel button has not been pressed
                return
            else:
                try:
                    self.saveData(filename)
                except Exception:
                    showerror('Error!', "Data could not be saved")


if __name__ == "__main__":
    LineSimplification().mainloop()
