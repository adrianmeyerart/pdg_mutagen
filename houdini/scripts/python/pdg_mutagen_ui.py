#imports
from PySide2 import QtWidgets, QtCore, QtGui, QtWebEngineWidgets

import hou
import pdg

import time
import math
import codecs
import os
import sys
import errno
import ast
import subprocess
from functools import partial

import pdg_mutagen


#info
__author__ = "Adrian Meyer @Animationsinstitut Filmakademie Baden-Württemberg"
__copyright__ = "2019 All rights reserved. See LICENSE for more details."
__status__ = "Prototype"





#glob user variables
wedge_prefix = "wdg_"


#glob stylesheet
glob_stylesheet = """

				QFrame[FGFrame=true] {
					background-color: rgb(58, 58, 58);
					border: 1px solid #848484;
				}

				QFrame[FGFrameOut=true] {
					background-color: rgb(58, 58, 58);
				}

				QWidget[BGFrame=true] {
					background-color: rgb(48, 48, 48);
				}

				QLabel[HeaderLabel=true] {
					font: 14px;
				}

				QLabel[DescrLabel=true] {
					color: #a2a2a2;
				}


				QPushButton[MarkButton=true] {
					background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 rgba(200, 200, 200, 0%), stop: 1 rgba(175, 175, 175, 2%));
				}

				QPushButton[MarkButton=true]:hover {
					background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 rgba(200, 200, 200, 6%), stop: 1 rgba(175, 175, 175, 6%));
				}

				QPushButton[MarkButton=true]:checked {
					background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 rgba(200, 200, 200, 15%), stop: 1 rgba(175, 175, 175, 15%));
				}


				QPushButton[SelButton=true] {
					background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #484848, stop: 1 #404040);
				}

				QPushButton[SelButton=true]:hover {
					background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #585858, stop: 1 #404040);
				}

				QPushButton[SelButton=true]:checked {
					background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #776134, stop: 1 #57482a);
				}

				"""

#other style variables
bg_color = "background-color: rgb(48, 48, 48)"
fg_color = "background-color: rgb(58, 58, 58)"





#main interface class / called by Houdini
class MutagenInterface(QtWidgets.QWidget):
	def __init__(self, parent=None):
		super(MutagenInterface, self).__init__(parent)


		####initial startup layout            
		
		#create layout for main QWidget
		self._layout = QtWidgets.QVBoxLayout()
		self._layout.setContentsMargins(0,0,0,0)
		self.setLayout(self._layout)


		# Set the stylesheet
		self.setStyleSheet(glob_stylesheet)
		self.setProperty('BGFrame', True)


		#set to startup interface
		self._startup_interface = StartupInterface(self)
		self._layout.addWidget(self._startup_interface)






#startup interface class
class StartupInterface(QtWidgets.QWidget):
	def __init__(self, root_interface, parent=None):
		super(StartupInterface, self).__init__(parent)

		
		self._root_if = root_interface


		# Set the stylesheet
		self.setStyleSheet(glob_stylesheet)
		

		#create layout for main QWidget
		layout = QtWidgets.QVBoxLayout()
		#layout.setAlignment(QtCore.Qt.AlignCenter)
		layout.setContentsMargins(0,0,0,0)
		#self.setStyleSheet(bg_color)
		
		self.setLayout(layout)


		#startup dialoge
		startup_frame_out = QtWidgets.QFrame(self)
		startup_frame_out.setGeometry(QtCore.QRect(0, 0, 550, 660))
		startup_frame_out.setProperty('FGFrameOut', True)


		startup_frame = QtWidgets.QFrame(startup_frame_out)
		startup_frame.setGeometry(QtCore.QRect(20, 20, 510, 620))
		#startup_frame.setStyleSheet(fg_color)
		startup_frame.setProperty('FGFrame', True)

		startup_frame.setFrameStyle(QtWidgets.QFrame.Box | QtWidgets.QFrame.Plain)
		startup_frame.setLineWidth(1)


		#create QScrollArea attached to main QWidget and attach QFrame
		startup_scroll_area = QtWidgets.QScrollArea(self)
		startup_scroll_area.setWidget(startup_frame_out)
		#startup_scroll_area.setAlignment(QtCore.Qt.AlignCenter)

		#add QScrollArea to main layout
		layout.addWidget(startup_scroll_area)



		#layout
		frame_layout = QtWidgets.QVBoxLayout()
		frame_layout.setAlignment(QtCore.Qt.AlignTop)
		frame_layout.setContentsMargins(50,80,50,80)
		startup_frame.setLayout(frame_layout)


		
		#items
		header_label = QtWidgets.QLabel("PDG MUTAGEN TOOLS\n\n")
		header_label.setProperty('HeaderLabel', True)
		
		setup_label_h = QtWidgets.QLabel("\nCreates a new Template Topnet at OBJ Level.\n")
		setup_label = QtWidgets.QLabel("Creates a PDG Graph Template with basic Wedging Setup,\ndesigned to work with the Mutagen Viewer and other Mutagen Tools.\nThis includes Wedge, Geo Ropfetch, Image Render Ropfetch,\nPartition, ImageMagick and FFmpeg TOPs.\n")
		setup_label.setProperty('DescrLabel', True)

		wizard_label_h = QtWidgets.QLabel("\n\n\n\nOpens the Mutagen Viewer\n")
		wizard_label = QtWidgets.QLabel("Displays prerendered Contact Sheet Video of Wedging Variations.\nPromts you to choose FFmpeg Output Top that created the Wedge Contact\nSheet Video (usually last Node in PDG Chain). Then analyses PDG Graph\nto set all necessary Filepaths and Parameters to set up the Mutagen Viewer.\n")
		wizard_label.setProperty('DescrLabel', True)


		setup_wizard_button = QtWidgets.QPushButton("Mutagen Setup")
		setup_wizard_button.clicked.connect(self._setupWizard_ButtonClicked)
		setup_wizard_button.setProperty('SelButton', True)


		view_wizard_button = QtWidgets.QPushButton("Mutagen Viewer")
		view_wizard_button.clicked.connect(self._viewWizard_ButtonClicked)
		view_wizard_button.setProperty('SelButton', True)


		frame_layout.addWidget(header_label)
		frame_layout.addWidget(setup_label_h)
		frame_layout.addWidget(setup_label)
		frame_layout.addWidget(setup_wizard_button)
		frame_layout.addWidget(wizard_label_h)
		frame_layout.addWidget(wizard_label)
		frame_layout.addWidget(view_wizard_button)
		




	def _setupWizard_ButtonClicked(self):
		print "Creating Mutagen PDG Graph Template...\n"

		pdg_mutagen.createMutagenSetup()


	
	def _viewWizard_ButtonClicked(self):
		print "Starting View Wizard...\n"

		#add viewer interface
		viewer_interface = ViewerInterface(self._root_if)
		#self._root_if._layout.addWidget(viewer_interface)









#viewer interface class
class ViewerInterface(QtWidgets.QWidget):
	def __init__(self, root_interface, parent=None):
		super(ViewerInterface, self).__init__(parent)


		self._root_if = root_interface

		
		# Set the stylesheet
		self.setStyleSheet(glob_stylesheet)		

		#create layout for main QWidget
		layout = QtWidgets.QVBoxLayout()
		layout.setContentsMargins(0,0,0,0)
		self.setLayout(layout)


		#call setup wizard to get data from PDG Graph
		setupWizard(self)
		#continue
		setupWizardViewer(self)



		#change interfaces in root interface
		startup_interface_inst = self._root_if._startup_interface

		#hide startup interface
		startup_interface_inst.hide()
		#add viewer interface (self)
		self._root_if._layout.addWidget(self)


		

		####create interface

		#create QFrame with fixed size as container for image and grid table
		self._frame = QtWidgets.QWidget()
		self._frame.setGeometry(QtCore.QRect(0, 0, self._frame_width, self._frame_height))


		####html webview for video playback

		#qt webview for html5 video playback
		self._webview = QtWebEngineWidgets.QWebEngineView(self._frame)
		self._webview.setGeometry(QtCore.QRect(0, 0, self._frame_width, self._frame_height))


		#set html content

		html_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../html/pdg_mutagen_webvideo_temp.html"))
		base_url = QtCore.QUrl.fromLocalFile(html_path)

		html = codecs.open(html_path, 'r')
		html_str = html.read()
		#replace source path placeholder with actual video filepath        
		html_out = html_str.replace('SOURCE_PATH', self._videofile)


		#set html content
		self._webview.setHtml(html_out, base_url)

	

		####further layout

		#create QScrollArea attached to main QWidget and attach QFrame
		scroll_area = QtWidgets.QScrollArea(self)
		scroll_area.setWidget(self._frame)



		#create empty QGridLayout and attach to main QWidget
		self._grid = QtWidgets.QGridLayout(self._frame)
		self._grid.setContentsMargins(0,0,0,0)
		#self._grid.setHorizontalSpacing(self._cell_frame_padding_h)
		#self._grid.setVerticalSpacing(self._cell_frame_padding_v)
		self._grid.setHorizontalSpacing(0)
		self._grid.setVerticalSpacing(0)
		#self._grid.setAlignment(QtCore.Qt.AlignLeft)


		#create cells by iteration and attach to QGridLayout
		
		idx = 0
		#if splits exist set to start index
		if self._num_pdg_splits > 0:
			idx = self._start_idx

		cell_count = 0

		self._cell_dict = {}

		for row in range(self._num_height):
			self._grid.setRowMinimumHeight(row, self._cell_frame_height+self._cell_frame_height_padding)

			for column in range(self._num_width):
				if cell_count < self._num_total:
					#self._grid.setColumnMinimumWidth(row, self._cell_frame_width+self._cell_frame_padding_h)
					#self._grid.setColumnMinimumWidth(row, self._cell_frame_width)

					#get cell_idx from idx
					cell_idx = self._wdg_idx_l[idx]

					#create wedgeCell
					cell = self._wedgeCell(cell_idx)

					#add _wedgeCell instance to cell dictionary
					self._cell_dict[cell_idx] = cell
					#add as widget to grid layout
					self._grid.addWidget(cell, row, column)

					#incr
					idx += 1
					cell_count += 1
					



		#####load marked selection fir grid layout from file and initialize
		marked_file = self._marked_filepath
		if os.path.isfile(marked_file):
			print "Saved Marking State File found:\n{}".format(marked_file)
			print "Initializing UI...\n"

			with open(marked_file, 'r') as f:
				wedge_mark_dict = f.read()

			#convert back to dict
			wedge_mark_dict = ast.literal_eval(wedge_mark_dict)
		
			
			for i in wedge_mark_dict:
				mark_button = self._cell_dict[i].children()[0]
				mark_button.setChecked(wedge_mark_dict[i])

			print "Initializing UI successfull\n"
			
		



		####top shelf button ui

		#button horizontal layout
		button_layout = QtWidgets.QHBoxLayout()
		button_layout.setContentsMargins(0,4,0,0)
		button_layout.setAlignment(QtCore.Qt.AlignLeft)
		
		layout.addLayout(button_layout)
		
		#save marked button
		save_marked_button = QtWidgets.QPushButton("Store Marked Wedges")
		save_marked_button.clicked.connect(self._saveMarkedWedges)
		save_marked_button.setToolTip("This will save the current Marked Wedges to a file.\nWhen reopening Hipfile or Mutagen Viewer, they will be loaded automatically.\nStored seperately for each FFmpeg Root Node.")
		save_marked_button.setFixedWidth(180)

		button_layout.addWidget(save_marked_button)

		#start mutation from marked wedges button
		mutation_from_marked_button = QtWidgets.QPushButton("Setup Mutation from Marked Wedges")
		mutation_from_marked_button.clicked.connect(self._startMutationFromMarkedWedges)
		mutation_from_marked_button.setFixedWidth(280)
		mutation_from_marked_button.setToolTip("This will create a new base Wedge TOP, containing all Parameter Settings from Marked Wedges.\nThis can then be used to generate further Wedge variation based on the Settings you liked,\nby appending further Wedge TOPs.\n\nNote: This will clear all existing Takes in Scene!\nWarning: Depending on number of Takes and edited Parameters this can take quite long,\nplease be patient and let Houdini cook without UI Interaction until the Wedge Node UI is selected.\n(Unfortunately there is currently no faster way to access Take parameters in HOM).")
		button_layout.addWidget(mutation_from_marked_button)




		#add QScrollArea to main layout
		layout.addWidget(scroll_area)

		#refocus webwidget
		self._webview.activateWindow()
		self._webview.setFocus()








	####global mouse and keyboard events

	#key press fucntions
	def keyPressEvent(self, e):

		#print "Key pressed"

		#reset focus to webvoew
		self._webview.activateWindow()
		self._webview.setFocus()



		#zoom
		zoom_incr = 0.05
		zoom_min = 0.4
		zoom_max = 1


		#if e.key() == QtCore.Qt.Key_H:
			#print "Space Key pressed"

			#reset focus to webvoew
			#self._webview.activateWindow()
			#self._webview.setFocus()

	
		if e.key() == QtCore.Qt.Key_I:
			#print "I Key pressed"
			if self._zoom_factor > zoom_min:
				self._zoom_factor -= zoom_incr

				#print self._zoom_factor
				self._zoomChanged()


		if e.key() == QtCore.Qt.Key_O:
			#print "O Key pressed"
			if self._zoom_factor < zoom_max:
				self._zoom_factor += zoom_incr

				#print self._zoom_factor
				self._zoomChanged()



		if e.key() == QtCore.Qt.Key_M:
			#print "M Key pressed"
		
			self._markButtonClear()
			print "\nAll marked Wedges cleared\n"




	

	#zoom function to update interface
	def _zoomChanged(self):

		#resize _webview
		self._webview.setZoomFactor(self._zoom_factor)

		#resize main _frame
		self._frame.setFixedSize(self._frame_width*self._zoom_factor, self._frame_height*self._zoom_factor)
		
		#resize _grid
		#self._grid.setHorizontalSpacing(self._cell_frame_padding_h*self._zoom_factor)
		#self._grid.setVerticalSpacing(self._cell_frame_padding_v*self._zoom_factor)


		#iterate over grid layout / cells
		for idx in self._cell_dict.keys():
			#print (idx, " > ", self._cell_dict[idx])

			mark_button = self._cell_dict[idx].children()[0]
			mark_button.setFixedHeight(self._cell_frame_height * self._zoom_factor)
			mark_button.setFixedWidth((self._cell_frame_width+(self._cell_frame_padding_h)*1) * self._zoom_factor)

			sel_button = self._cell_dict[idx].children()[2]
			sel_button.setFixedWidth((self._cell_frame_width+(self._cell_frame_padding_h*1)) * self._zoom_factor)







	#Wedge Cell function / Button Overlay Cell for Wedge Selection
	def _wedgeCell(self, cell_idx, *args):


		self._cell_idx = cell_idx


		cell_frame = QtWidgets.QWidget()

		cell_layout = QtWidgets.QVBoxLayout()
		#cell_layout.setAlignment(QtCore.Qt.AlignTop)
		cell_layout.setContentsMargins(0,0,0,0)
		#cell_layout.setVerticalSpacing(0)
		cell_frame.setLayout(cell_layout)



		#select button
		self._sel_button = QtWidgets.QPushButton(self._cell_idx, cell_frame)
		self._sel_button.setCheckable(True)
		#self._sel_button.clicked.connect(self._selButtonClicked)
		self._sel_button.clicked.connect(partial(self._selButtonClicked, self._cell_idx, ))
		self._sel_button.setFixedWidth(self._cell_frame_width+(self._cell_frame_padding_h*1))

		
		self._sel_button.setToolTip("Click to select Wedge Work Item in PDG Graph\n\nRight Click to open Wedge Sequence in RV/Explorer\n\n'J/K/L' -> Back / Play-Stop / Forward\n'I/O' -> Zoom In-Out\n'UP/DOWN/LEFT/RIGHT' -> Navigate\n\n'M' -> Clear Marked")
		self._sel_button.setProperty('SelButton', True)



		#mark button
		self._mark_button = QtWidgets.QPushButton(cell_frame)
		self._mark_button.setCheckable(True)
		#self._mark_button.clicked.connect(self._markButtonClicked)
		self._mark_button.clicked.connect(partial(self._markButtonClicked, self._cell_idx, ))
		#self._mark_button.setFixedHeight(self._cell_frame_height - (self._cell_frame_padding_v * 2))
		self._mark_button.setFixedHeight(self._cell_frame_height)
		self._mark_button.setFixedWidth(self._cell_frame_width+(self._cell_frame_padding_h*1))

		self._mark_button.setToolTip("Click to mark Wedge Variation\n\nRight Click to open Wedge Sequence in RV/Explorer\n\n'J/K/L' -> Back / Play-Stop / Forward\n'I/O' -> Zoom In-Out\n'UP/DOWN/LEFT/RIGHT' -> Navigate\n\n'M' -> Clear Marked")
		self._mark_button.setProperty('MarkButton', True)



		#add to layout
		cell_layout.addWidget(self._mark_button, QtCore.Qt.AlignTop)
		cell_layout.addWidget(self._sel_button, QtCore.Qt.AlignBottom)

		#set to lowest z-index
		self._mark_button.lower()




		#add right click menu / open in explorer / open in rv
		cell_frame.setContextMenuPolicy(QtCore.Qt.ActionsContextMenu)

		
		open_sequence = QtWidgets.QAction(cell_frame)
		open_sequence.setText("Open Wedge Sequence in RV")
		open_sequence.triggered.connect(partial(self._openSequence, self._cell_idx, ))
		cell_frame.addAction(open_sequence)

		open_explorer = QtWidgets.QAction(cell_frame)
		open_explorer.setText("Open Wedge Sequence in Explorer")
		open_explorer.triggered.connect(partial(self._openExplorer, self._cell_idx, ))
		cell_frame.addAction(open_explorer)
		

		#return cell
		return cell_frame
		

	


	def _openSequence(self, idx, *args):
		
		path = self._render_outpath
		sender_idx = idx


		path_split = path.split(wedge_prefix)
		path = path_split[0] + wedge_prefix + sender_idx

		print "Open Wedge Sequence {} in RV Player:".format(sender_idx)
		print path
		print "\n"

		
		if os.path.exists(path):
			try:
				subprocess.Popen(["rv", path])
			except:
				print "RV may not be installed on your system or net set in $PATH"
		else:
			print "Path does not exist or you may not have access to it."



	

	def _openExplorer(self, idx, *args):
		
		path = self._render_outpath
		sender_idx = idx

		path_split = path.split(wedge_prefix)
		path = path_split[0] + wedge_prefix + sender_idx

		print "Open Wedge Sequence {} in Explorer:".format(sender_idx)
		print path
		print "\n"


		if os.path.exists(path):
			if sys.platform == "linux2":
				new_env = os.environ
				new_env["LD_LIBRARY_PATH"] = ""
				subprocess.Popen(["xdg-open", path], env=new_env)
			if sys.platform == "win32":
				path = path.replace("/", "\\")
				subprocess.Popen(["explorer", path])
			if sys.platform == "darwin":
				subprocess.Popen(["open", path])

		else:
			print "Path does not exist or you may not have access to it."



	


	
	def _selButtonClicked(self, idx, *args):

		sender_idx = idx
		sender = self._cell_dict[idx].children()[2]
		#print sender
		#print sender.isChecked()
		
		for i in self._cell_dict.keys():
			sel_button = self._cell_dict[i].children()[2]
			if i != sender_idx:
				sel_button.setChecked(False)


		#select work item
		if sender.isChecked():
			for work_item in self._work_items:
				#print work_item
				
				wedgenum_l = pdg.intDataArray(work_item, "wedgenum")
				#print wedgenum_l
				
				wdg_idx = ""
				for wedgenum in wedgenum_l:
					wdg_idx += "_" + str(wedgenum)   
				wdg_idx = wdg_idx[1:]
				#print wdg_idx
				
				
				#select work item
				if wdg_idx == sender_idx:
					work_item_id = work_item.id
					
					self._wedge_anchor_node.setSelectedWorkItem(work_item_id)
					print "\nWork Item selected:"
					print "Wedge Index: " + wdg_idx
					#print "ID: " + str(work_item_id)
		

		#reset focus to webview
		self._webview.activateWindow()
		self._webview.setFocus()





	def _markButtonClicked(self, idx, *args):

		sender_idx = idx
		sender = self._cell_dict[idx].children()[0]

		if sender.isChecked():
			print "Wedge Index marked: {}".format(sender_idx)
		else:
			print "Wedge Index unmarked: {}".format(sender_idx)

		#reset focus to webview
		self._webview.activateWindow()
		self._webview.setFocus()



	

	
	def _markButtonClear(self):
		
		for i in self._cell_dict.keys():
			mark_button = self._cell_dict[i].children()[0]
			mark_button.setChecked(False)



	

	def _saveMarkedWedges(self):

		print "\nSaving all marked Wedges to Disk...\n"


		wedge_mark_dict = {}
		
		for i in self._cell_dict.keys():
			mark_button = self._cell_dict[i].children()[0]

			wedge_mark_dict[i] = mark_button.isChecked()


		#print "\nWedge Mark Dict:"
		#print wedge_mark_dict

		#save to file
		print "Save Filepath: {}".format(self._marked_filepath)

		if not os.path.exists(os.path.dirname(self._marked_filepath)):
			try:
				os.makedirs(os.path.dirname(self._marked_filepath))
			except OSError as exc: # Guard against race condition
				if exc.errno != errno.EEXIST:
					print "Saving failed\n"
					raise

		with open(self._marked_filepath, "w") as f:
			f.write(str(wedge_mark_dict))
			print "Saving successfull\n"





	

	def _startMutationFromMarkedWedges(self):


		mode = hou.ui.selectFromList(["Convert to Takes (del. existing Takes)", "Convert to Takes (keep existing Takes)", "Convert to TOP Wedge (del. existing Takes)"], default_choices=([0]), exclusive=True, message="Please choose how to convert Marked Wedges", title="Conversion Mode", column_header="Choices", num_visible_rows=3, clear_on_cancel=True, width=400, height=180)
		if mode == ():
			raise Exception("Cancelled.")

		mode = mode[0]

		print "\nSetting up new Mutation PDG Graph from marked Wedges...\n"

		marked_idx_list = []
		
		for i in self._cell_dict.keys():
			mark_button = self._cell_dict[i].children()[0]

			if mark_button.isChecked():
				marked_idx_list.append(i)

		
		num_wedges_marked = len(marked_idx_list)

		if num_wedges_marked > 0:
			print "List of Wedges to be used:"
			print marked_idx_list

			pdg_mutagen.setupMutationFromMarkedWedges(marked_idx_list, self._wedge_anchor_node, mode)



		else:
			print "No Wedges marked. Aborting."
			











#setup wizard function to get PDG nodes for pdg input data and wedge selection                
def setupWizard(self):


	print "\n"*4
	print "_"*100
	print "PDG Mutagen Setup Wizard Started..."
	print "_"*100
	print "\n"*2
	

	####initial ui selection

	def isFFmpegNode(node):
		#top_type_list = [hou.nodeType("Top/wedge"), hou.nodeType("Top/merge"), hou.nodeType("Top/ropfetch")]
		top_type_list = [hou.nodeType("Top/ffmpegencodevideo")]
		if node.type() in top_type_list:
			return True
		else:
			return False
		

	ffmpeg_nodepath = hou.ui.selectNode(title="Select FFmpeg TOP Node", custom_node_filter_callback=isFFmpegNode)
	if ffmpeg_nodepath == None:
		raise Exception("No FFmpeg Node selected.")


	self._ffmpeg_node = hou.node(ffmpeg_nodepath)
	print "FFmpeg Node (Root Node): {}".format(self._ffmpeg_node.name())

	#for marked saving...
	ffmpeg_name = self._ffmpeg_node.name()
	self._marked_filepath = hou.expandString("$HIP")+"/mutagen/view_store/"+ffmpeg_name+"/"+"mutagen_view_store."+ffmpeg_name+".py"


	#furher analyse graph...
	self._pdgchain_nodes = self._ffmpeg_node.inputAncestors()


	#find output wedge node
	for pdgnode in self._pdgchain_nodes:
		if pdgnode.type() == hou.nodeType("Top/wedge"):
			self._wedge_anchor_node = pdgnode
			break


	#find root wedge node (first wedge in graph)
	for pdgnode in self._pdgchain_nodes:
		if pdgnode.type() == hou.nodeType("Top/wedge"):
			self._wedge_root_node = pdgnode



	#find render or ropfetch node (last appearance in graph)
	#init
	self._render_node = None
	self._render_outpath = ""

	
	for pdgnode in self._pdgchain_nodes:
		#if mantra TOP present
		if pdgnode.type() == hou.nodeType("Top/ropmantra"):

			self._render_node = pdgnode
			self._render_outpath = pdg_node.parm("vm_picture").evalAtFrame(0)

			break


		#if no mantra TOP present, but linked ROPs over ropfetch
		elif pdgnode.type() == hou.nodeType("Top/ropfetch"):

			render_node = hou.node(pdgnode.parm("roppath").eval())

			#Mantra
			if render_node.type() == hou.nodeType("Driver/ifd"):
				self._render_node = render_node
				self._render_outpath = render_node.parm("vm_picture").evalAtFrame(0)
			#Arnold
			elif render_node.type() == hou.nodeType("Driver/arnold"):
				self._render_node = render_node
				self._render_outpath = render_node.parm("ar_picture").evalAtFrame(0)
			#Redshift
			elif render_node.type() == hou.nodeType("Driver/redshift"):
				self._render_node = render_node
				self._render_outpath = render_node.parm("RS_outputFileNamePrefix").evalAtFrame(0)
					

			self._render_node_pdg = pdgnode
			#print
			print "Render Output Top Node: {}".format(self._render_node_pdg.name())
			break
		
		
	#make abs and print
	self._render_outpath = os.path.abspath(os.path.join(os.path.dirname(__file__), self._render_outpath))
	#change back to forward slashes
	self._render_outpath = self._render_outpath.replace("\\", "/")
	print "Render Output ROP Node: {}".format(self._render_node.name())

		

	#find image magick node
	for pdgnode in self._pdgchain_nodes:
		if pdgnode.type() == hou.nodeType("Top/imagemagick"):
			self._imagemagick_node = pdgnode
			break
  
	
	#find split nodes
	self._num_pdg_splits = 0
	for pdgnode in self._pdgchain_nodes:
		if pdgnode.type() == hou.nodeType("Top/split"):
			self._num_pdg_splits += 1


	#select correct split p
	self._split_p = 0
	if self._num_pdg_splits > 0:
		self._split_p = int(self._ffmpeg_node.name().split("_p")[-1])




	print "Image Magick Node: {}".format(self._imagemagick_node.name())
	print "Wedge Anchor Node: {}".format(self._wedge_anchor_node.name())
	print "Wedge Root Node: {}".format(self._wedge_root_node.name())
	print "{} Nodes found in PDG Chain (Upstream from Root Node)".format(len(self._pdgchain_nodes))
	print "{} Graph Splits found".format(self._num_pdg_splits)
	if self._num_pdg_splits > 0:
		print "Split Part {} selected\n".format(self._split_p)
	print "\n"








#setup wizard function continued only when called from mutagen viewer pypanel
def setupWizardViewer(self):

	
	#get wedge index list
	getWedgeIndexList(self)
	#print self._wdg_idx_l


	self._num_wedges = len(self._wdg_idx_l)
	print "Number of Wedges {}".format(self._num_wedges)

	self._num_wedges_split = self._num_wedges / (self._num_pdg_splits + 1)
	if self._num_pdg_splits > 0:
		print "Number of Wedges per Split {}".format(self._num_wedges_split)
	

	#set start index for cells
	self._start_idx = self._num_wedges_split * self._split_p
	print "Start Index set to: {}".format(self._start_idx)
	print "\n"



	####set variables

	self._videofile = self._ffmpeg_node.parm("outputfilename").eval()
	#make absolute
	self._videofile = os.path.abspath(os.path.join(os.path.dirname(__file__), self._videofile))
	#change back to forward slashes
	self._videofile = self._videofile.replace("\\", "/")


	#check if video file is present
	if os.path.isfile(self._videofile):
		print "Videofile:\n{}\n".format(self._videofile)

	else:
		raise Exception("\n{}\nVideofile does not exist. Make sure the PDG Graph is completely rendered in advance.\nAlso be aware that if you use any versioning in Filepaths, the Mutagen Viewer will only work in the Hipfile version you rendered out when Filepaths are not explicitly expanded.".format(self._videofile))


	print "\nRender Output Path:\n{}\n".format(self._render_outpath)



	self._im_command = self._imagemagick_node.parm("customcommand").eval()
	print "Image Magick Command:\n{}\n".format(self._im_command)

	#geoemtry (sizes)
	geo_str = self._im_command.split("-geometry")[-1]
	geo_str = geo_str.split(" ")
	geo_str = geo_str[1].split("x")

	geo_str_l = []
	geo_str_l.append(geo_str[0])

	for geo_str_s in geo_str[1].split("+"):
		geo_str_l.append(geo_str_s)
	#print geo_str_l


	
	####set initial zoom setup
	self._zoom_factor = 1


	self._cell_frame_width = int(geo_str_l[0])
	print "Cell Width: {}".format(self._cell_frame_width)
	self._cell_frame_height = int(geo_str_l[1])
	print "Cell Height: {}".format(self._cell_frame_height)

	self._cell_frame_height_padding = 18
	print "Cell Text Height Padding: {}".format(self._cell_frame_height_padding)

	self._cell_frame_padding_h = int(geo_str_l[2])
	print "Cell Width Padding: {}".format(self._cell_frame_padding_h)
	self._cell_frame_padding_v = int(geo_str_l[3])
	print "Cell Height Padding: {}".format(self._cell_frame_padding_v)


	
	#tile (tiling if explicitly set in command)

	self._num_total = self._num_wedges_split
	self._num_width = 0
	self._num_height = 0

	print "\n"
	#check if -tile arg is set
	if "-tile " in self._im_command:
		print "Explicit Tiling set in IM Command"
		tile_str = self._im_command.split("-tile")[-1]
		tile_str = tile_str.split(" ")
		tile_str = tile_str[1].split("x")
		#print tile_str

		#check if both x&y are set
		if tile_str[0] and tile_str[1] != "":
			self._num_width = int(tile_str[0])
			self._num_height = int(tile_str[1])
		elif (tile_str[0] != "") and (tile_str[1] == ""):
			print "Only X Tiles set..."
			self._num_width = int(tile_str[0])
			self._num_height = self._num_total / self._num_width
		elif (tile_str[0] == "") and (tile_str[1] != ""):
			print "Only Y Tiles set..."
			self._num_height = int(tile_str[1])
			self._num_width = self._num_total / self._num_height

	#if -tile arg is not set
	else:
		print "No explicit Tiling set in IM Command. Using default Image Magick Tiling Algorithm"

		n = self._num_wedges_split

		sqrt = math.sqrt(n)
		#print "\nRoot: {}".format(sqrt)

		if sqrt%1 >= 0.5:
			x = math.ceil(sqrt)+1
			y = math.floor(sqrt)
		else:
			x = math.ceil(sqrt)
			y = math.floor(sqrt)

		self._num_width = int(x)
		self._num_height = int(y)

		


	#print results
	print "Number of Cells in X: {}".format(self._num_width)
	print "Number of Cells in Y: {}".format(self._num_height)
	print "Total Number of Cells: {}".format(self._num_total)
	print "\n"
	

	self._frame_width = (self._cell_frame_width + (self._cell_frame_padding_h*2)) * self._num_width
	print "Frame Width: {}px".format(self._frame_width)
	self._frame_height = (self._cell_frame_height + (self._cell_frame_padding_v*2) + self._cell_frame_height_padding) * self._num_height
	print "Frame Height: {}px".format(self._frame_height)
	print "\n"
	
	#set colors
	self._bg_color = "background-color: rgb(48, 48, 48)"
	self._fg_color = "background-color: rgb(58, 58, 58)"


	print "_"*100
	print "PDG Mutagen Setup Wizard Complete"
	print "_"*100
	print "\n"*2



	






#get wedge index list function
def getWedgeIndexList(self):

	#generate static items first to be able to access
	self._wedge_anchor_node.generateStaticItems()
	print "Generating Static Work Items..."
	time.sleep(3)

	try:
		self._wedge_anchor_node_pdg = self._wedge_anchor_node.getPDGNode()
		self._work_items = self._wedge_anchor_node_pdg.staticWorkItems


		self._wdg_idx_l = []
		#self._wdg_id_l = []

		for work_item in self._work_items:

			#work_item_id = work_item.id
			#self._wdg_id_l.append( work_item_id)

			wedgenum_l = pdg.intDataArray(work_item, "wedgenum")            
			wdg_idx = ""
			for wedgenum in wedgenum_l:
				wdg_idx += "_" + str(wedgenum)   
			wdg_idx = wdg_idx[1:]
			
			self._wdg_idx_l.append(wdg_idx)
			
		
		#print self._wdg_id_l
		#print self._wdg_idx_l
		#return self._wdg_idx_l

	except Exception as e:
		print e
		print "\nStatic Work Items could not be generated.\nPlease right click 'Generate Node' on last Wedge Node in chain and initialize manually.\nThis only has to be done once after opening Scene. This is a current Limitation.\n"