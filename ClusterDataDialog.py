# Maan Qraitem 
# CS 251

import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox


###############################################################################
# Dialog for displaying information about the cluster data. 	 
# 							  
###############################################################################

class ClusterDataDialog(tk.Toplevel):

	def __init__(self, parent, codebooks, codes, errors, quality):

		tk.Toplevel.__init__(self, parent)
		self.transient(parent)

		self.title("Clustering Data")

		self.codes = codes.reshape(codes.shape[0]).tolist()

		self.codebooks = codebooks 

		self.errors = errors 

		self.quality = quality 

		self.K = self.codebooks.shape[0] 

		self.cancelled = True

		self.parent = parent

		self.result = []

		body = tk.Frame(self)
		self.body(body)
		body.pack(padx=5, pady=5)

		self.buttonbox()

		self.grab_set()

		self.protocol("WM_DELETE_WINDOW", self.cancel)

		self.geometry("+%d+%d" % (parent.winfo_rootx()+50,
									parent.winfo_rooty()+50))

		self.wait_window(self)

		self.binhisto = None


	def listToString(self, mean): 
		final = "("
		for i in mean: 
			final += "{:0.2f}".format(i) + " ,"	
		final = final[:-1]
		final += ")"
		return final


	#Builds the entry widget. 
	#Returns the widget to set it as initial focus. 
	def body(self, master):

		frame = tk.Frame(master)

		Labels = []

		Labels.append(tk.Label(frame, text= "Cluster Coordinates", width=20 ).grid(row = 0, column = 0))
		for j in range(self.K): 
			Labels.append(tk.Label(frame, text= self.listToString(self.codebooks[j,:]), width=20 ).grid(row = j + 1, column = 0))

		Labels.append(tk.Label(frame, text= "Number of data points", width=20 ).grid(row = 0, column = 1))
		for j in range(self.K): 
			Labels.append(tk.Label(frame, text= str(self.codes.count(j)), width=20 ).grid(row = j + 1, column = 1))

		Labels.append(tk.Label(frame, text= "Error", width=10 ).grid(row = 0, column = 2))
		for j in range(self.K): 
			Labels.append(tk.Label(frame, text= "{:0.2f}".format(self.errors[j, 0]), width=20 ).grid(row = j + 1, column = 2))

		Labels.append(tk.Label(frame, text= "Quality error", width=20 ).grid(row = 0, column = 3))
		Labels.append(tk.Label(frame, text= "{:0.2f}".format(self.quality), width=20 ).grid(row = 1, column = 3))

		frame.grid()


    #Set up the standard (OK, Cancel) buttons. 
	def buttonbox(self):

		box = tk.Frame(self)

		w = tk.Button(box, text="OK", width=10, command=self.ok, default=tk.ACTIVE)
		w.pack(side=tk.LEFT, padx=5, pady=5)
		w = tk.Button(box, text="Cancel", width=10, command=self.cancel)
		w.pack(side=tk.LEFT, padx=5, pady=5)

		self.bind("<Return>", self.ok)
		self.bind("<Escape>", self.cancel)

		box.pack()

	#Handles pressing the Ok button. 
	#if the inputs was validated: destroyes the window and call cancel/apply. 
	#otherwise, set the focus back to entry widget. 
	def ok(self, event=None):

		if not self.validate():
			self.initial_focus.focus_set() # put focus back
			return

		self.withdraw()
		self.update_idletasks()

		self.apply()

		self.cancel()


	#destroys the dialog and reset the focus to parent window. 
	def cancel(self, event=None):

		# put focus back to the parent window
		self.parent.focus_set()
		self.destroy()


	#Validates the input in the entry widget: 
	#if not integer or out of range --> returns 0 
	#Otherwise, returns 1. 
	def validate(self):
		return 1

    #The method is called after validate. 
    #Update the numPoints and cancelled fields accordingly.
	def apply(self):
		self.cancelled = False

