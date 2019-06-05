#imports
import pdg
import hou

import time
import os

import pdg_mutagen_ui


#info
__author__ = "Adrian Meyer"
__copyright__ = "2019 All rights reserved. See LICENSE for more details."
__status__ = "Prototype"





#create pdg setup / creates template pdg graph to be used with PDG mutagen viewer
def createMutagenSetup():

	#topnet_glob
	hou_parent = hou.node("obj/")
	hou_node = hou_parent.createNode("topnet", "topnet_glob")
	topnet_name = hou_node.name()
	topnet_path = hou_node.path()

	hou_parm = hou_node.parm("topscheduler")
	hou_parm.set("localscheduler")
	hou_parent = hou_node

	#topnet_glob/localscheduler
	hou_node = hou_parent.node(hou_parent.path()+"/localscheduler")
	hou_node.move(hou.Vector2(0, 6))

	
	#topnet_glob/CTRL_WEDGES
	hou_node = hou_parent.createNode("null", "CTRL_WEDGES")
	hou_node.move(hou.Vector2(0, 4))
	hou_node.setColor(hou.Color([0, 0, 0]))
	hou_node.setExpressionLanguage(hou.exprLanguage.Hscript)

	hou_parm_template_group = hou.ParmTemplateGroup()
	# Code for parameter template
	hou_parm_template = hou.StringParmTemplate("wedge_expr", "Wedge IDX Exp.Python", 1, default_value=([""]), naming_scheme=hou.parmNamingScheme.Base1, string_type=hou.stringParmType.Regular, menu_items=([]), menu_labels=([]), icon_names=([]), item_generator_script="", item_generator_script_language=hou.scriptLanguage.Python, menu_type=hou.menuType.Normal)
	hou_parm_template_group.append(hou_parm_template)
	hou_node.setParmTemplateGroup(hou_parm_template_group)

	hou_parm = hou_node.parm("wedge_expr")
	hou_parm.set("")
	hou_parm.setAutoscope(True)

	hou_keyframe = hou.StringKeyframe()
	hou_keyframe.setTime(0)
	hou_keyframe.setExpression("import pdg\n\nwork_item = pdg.workItem()\nwdg_idx_l = pdg.intDataArray(work_item, \"wedgenum\")\n\nwdg_idx_s = \"\"\nfor wdg_idx in wdg_idx_l:\n    wdg_idx_s += str(wdg_idx) + \"_\"\n    \nwdg_idx_s = wdg_idx_s[0:-1]\n\n\n#print wdg_idx_s\nreturn wdg_idx_s\n    \n", hou.exprLanguage.Python)
	hou_parm.setKeyframe(hou_keyframe)

	hou_node.setColor(hou.Color([0, 0, 0]))
	hou_node.setExpressionLanguage(hou.exprLanguage.Hscript)

	
	#topnet_glob/wedge_root
	hou_node = hou_parent.createNode("wedge", "wedge_root")
	hou_node.move(hou.Vector2(0, 0.42))
	hou_parm = hou_node.parm("wedgecount")
	hou_parm.set(2)
	hou_parm = hou_node.parm("seed")
	hou_parm.set(2042)
	hou_parm = hou_node.parm("preservenum")
	hou_parm.set(1)
	hou_parm = hou_node.parm("previewselection")
	hou_parm.set(1)
	
	
	#topnet_glob/wedge_var1
	hou_node = hou_parent.createNode("wedge", "wedge_var1")
	hou_node.move(hou.Vector2(0, -1.2))
	hou_parm = hou_node.parm("wedgecount")
	hou_parm.set(2)
	hou_parm = hou_node.parm("seed")
	hou_parm.set(8215)
	hou_parm = hou_node.parm("preservenum")
	hou_parm.set(1)
	hou_parm = hou_node.parm("previewselection")
	hou_parm.set(1)
	
	
	#topnet_glob/wedge_var2
	hou_node = hou_parent.createNode("wedge", "wedge_var2")
	hou_node.move(hou.Vector2(0, -2.9))
	hou_parm = hou_node.parm("wedgecount")
	hou_parm.set(2)
	hou_parm = hou_node.parm("seed")
	hou_parm.set(8215)
	hou_parm = hou_node.parm("preservenum")
	hou_parm.set(1)
	hou_parm = hou_node.parm("previewselection")
	hou_parm.set(1)    
	
	hou_node.setColor(hou.Color([0.306, 0.306, 0.306]))

	
	#topnet_glob/ropfetch_geo
	hou_node = hou_parent.createNode("ropfetch", "ropfetch_geo")
	hou_node.move(hou.Vector2(0, -6.14))
	hou_parm = hou_node.parm("roppath")
	hou_parm.set(topnet_path+"/ropnet/geometry_rop")
	hou_parm = hou_node.parm("framegeneration")
	hou_parm.set("1")

	hou_parm = hou_node.parm("batchall")
	hou_parm.set(1)
	hou_node.setColor(hou.Color([1, 0.529, 0.624]))
	

	#topnet_glob/ropfetch_render
	hou_node = hou_parent.createNode("ropfetch", "ropfetch_render")
	hou_node.move(hou.Vector2(0, -8.64618))
	hou_parm = hou_node.parm("roppath")
	hou_parm.set(topnet_path+"/ropnet/mantra_rop")

	hou_parm = hou_node.parm("framesperbatch")
	hou_parm.set(5)
	hou_node.setColor(hou.Color([0.624, 0.329, 0.396]))

	
	#topnet_glob/partitionbyframe
	hou_node = hou_parent.createNode("partitionbyframe", "partitionbyframe")
	hou_node.move(hou.Vector2(0, -11.3))


	#topnet_glob/im_montage_p0
	hou_node = hou_parent.createNode("imagemagick", "im_montage_p0")
	hou_node.move(hou.Vector2(0, -14.16))
	hou_parm = hou_node.parm("overlayexpr")
	hou_parm.setAutoscope(True)
	hou_parm = hou_node.parm("usecustomcommand")
	hou_parm.set(1)
	hou_parm = hou_node.parm("customcommand")
	hou_parm.set("{imagemagick} -fill grey -label '%t' -background \"rgb(20,20,20)\" -mode concatenate {input_images} -geometry 256x256+2+2 \"{output_image}\"")
	hou_parm = hou_node.parm("filename")
	hou_parm.set("$HIP/img/$HIPNAME/$OS/$HIPNAME.$OS.$F4.jpg")
	hou_node.setColor(hou.Color([0.451, 0.369, 0.796]))

	
	#topnet_glob/waitforall
	hou_node = hou_parent.createNode("waitforall", "waitforall")
	hou_node.move(hou.Vector2(0, -17.1))

	
	#topnet_glob/ffmpeg_montage_p0
	hou_node = hou_parent.createNode("ffmpegencodevideo", "ffmpeg_montage_p0")
	hou_node.move(hou.Vector2(0, -20.0))
	hou_parm = hou_node.parm("fps")
	hou_keyframe = hou.Keyframe()
	hou_keyframe.setTime(0)
	hou_keyframe.setExpression("$FPS", hou.exprLanguage.Hscript)
	hou_parm.setKeyframe(hou_keyframe)
	hou_parm = hou_node.parm("outputfilename")
	hou_parm.set("$HIP/img/$HIPNAME/$OS/$HIPNAME.$OS.webm")
	hou_parm = hou_node.parm("customcommand")
	hou_parm.set(1)
	hou_parm = hou_node.parm("expr")
	hou_parm.set("\"{ffmpeg}\" -y -r {frames_per_sec}/1 -f concat -safe 0 -apply_trc iec61966_2_1 -i \"{frame_list_file}\" -c:v libvpx-vp9 -crf 32 -b:v 0 -vf \"fps={frames_per_sec},format=yuv420p\" -movflags faststart \"{output_file}\"")
	hou_parm = hou_node.parm("topscheduler")
	hou_parm.set("../localscheduler")

	hou_node.setColor(hou.Color([0.188, 0.529, 0.459]))

	hou_node.setSelected(True, clear_all_selected=True)

	
	#topnet_glob/ropnet
	hou_node = hou_parent.createNode("ropnet", "ropnet")
	hou_node.move(hou.Vector2(-3.29748, -7.22574))
	hou_node.setColor(hou.Color([0.996, 0.682, 0.682]))
	# Update the parent node.
	hou_parent = hou_node
	
	#topnet_glob/ropnet/geometry_rop
	hou_node = hou_parent.createNode("geometry", "geometry_rop")
	hou_node.move(hou.Vector2(1.4, -8.0))
	hou_parm = hou_node.parm("trange")
	hou_parm.set("normal")
	hou_parm = hou_node.parm("sopoutput")
	hou_parm.set("$HIP/geo/$HIPNAME/$OS/wdg_`chs('"+topnet_path+"/CTRL_WEDGES/wedge_expr')`/wdg_`chs('"+topnet_path+"/CTRL_WEDGES/wedge_expr')`.$F4.bgeo.sc")
	hou_node.setColor(hou.Color([1, 0.529, 0.624]))

	# Restore the parent and current nodes.
	hou_parent = hou_node.parent()


	#topnet_glob/ropnet/mantra_rop
	hou_node = hou_parent.createNode("ifd", "mantra_rop")
	hou_node.move(hou.Vector2(1.4, -12.5))
	hou_parm = hou_node.parm("trange")
	hou_parm.set("normal")
	hou_parm = hou_node.parm("override_camerares")
	hou_parm.set(1)
	hou_parm = hou_node.parm("res_fraction")
	hou_parm.set("specific")
	hou_parm_tuple = hou_node.parmTuple("res_override")
	hou_parm_tuple.set((512, 512))
	hou_parm = hou_node.parm("vm_picture")
	hou_parm.set("$HIP/render/$HIPNAME/$OS/wdg_`chs('"+topnet_path+"/CTRL_WEDGES/wedge_expr')`/wdg_`chs('"+topnet_path+"/CTRL_WEDGES/wedge_expr')`.$F4.jpg")
	hou_node.setColor(hou.Color([0.624, 0.329, 0.396]))

	# Restore the parent and current nodes.
	hou_parent = hou_node.parent().parent()
	

	# Code to establish connections for /obj/topnet_glob/wedge_var1
	hou_node = hou_parent.node("wedge_var1")
	hou_node.setInput(0, hou_parent.node("wedge_root"), 0)
	# Code to establish connections for /obj/topnet_glob/wedge_var2
	hou_node = hou_parent.node("wedge_var2")
	hou_node.setInput(0, hou_parent.node("wedge_var1"), 0)
	# Code to establish connections for /obj/topnet_glob/ropfetch_geo
	hou_node = hou_parent.node("ropfetch_geo")
	hou_node.setInput(0, hou_parent.node("wedge_var2"), 0)
	# Code to establish connections for /obj/topnet_glob/ropfetch_render
	hou_node = hou_parent.node("ropfetch_render")
	hou_node.setInput(0, hou_parent.node("ropfetch_geo"), 0)
	# Code to establish connections for /obj/topnet_glob/partitionbyframe
	hou_node = hou_parent.node("partitionbyframe")
	hou_node.setInput(0, hou_parent.node("ropfetch_render"), 0)
	# Code to establish connections for /obj/topnet_glob/im_montage_p0
	hou_node = hou_parent.node("im_montage_p0")
	hou_node.setInput(0, hou_parent.node("partitionbyframe"), 0)
	# Code to establish connections for /obj/topnet_glob/waitforall
	hou_node = hou_parent.node("waitforall")
	hou_node.setInput(0, hou_parent.node("im_montage_p0"), 0)
	# Code to establish connections for /obj/topnet_glob/ffmpeg_montage_p0
	hou_node = hou_parent.node("ffmpeg_montage_p0")
	hou_node.setInput(0, hou_parent.node("waitforall"), 0)
	


	#sticky notes

	#topnet_glob/__stickynote1
	hou_sticky = hou_parent.createStickyNote("__stickynote1")
	hou_sticky.setText("Important to set Geo Ropfetch Node to 'All Frames in One Batch' for Simulations.")
	hou_sticky.setTextSize(0)
	hou_sticky.setTextColor(hou.Color((0, 0, 0)))
	hou_sticky.setDrawBackground(True)
	hou_sticky.setPosition(hou.Vector2(4.3129, -6.62927))
	hou_sticky.setSize(hou.Vector2(8.17024, 0.922362))
	hou_sticky.setColor(hou.Color([1, 0.529, 0.624]))


	#topnet_glob/__stickynote2
	hou_sticky = hou_parent.createStickyNote("__stickynote2")
	hou_sticky.setText("The 'Preserve Wedge Numbers' option is important to be turned on.\nThis will append each @wedgenum in an array and allow for explicit mapping.\n\n'Overwrite Target Parm on Item Selection' (Push Refrences) is optional, but very convinient with the Mutagen Setup opposed to \"Pull References\".\n\nAdd as many Wedges as you like.\n\nUse the Shelf Tool 'Convert Takes to Wedge' from the 'PDG Mutagen' Shelf to convert variations you have set up in the \"classical Take style\" to a single Wedge TOP that holds all the edited parameters. The Takes will be redundant from then\nAppend additional Wedge TOPs as you like to generate further variation.\n")
	hou_sticky.setTextSize(0)
	hou_sticky.setTextColor(hou.Color((0, 0, 0)))
	hou_sticky.setDrawBackground(True)
	hou_sticky.setPosition(hou.Vector2(4.31289, -3.24063))
	hou_sticky.setSize(hou.Vector2(8.17024, 3.99192))
	hou_sticky.setColor(hou.Color([0.6, 0.6, 0.6]))


	#topnet_glob/__stickynote3
	hou_sticky = hou_parent.createStickyNote("__stickynote3")
	hou_sticky.setText("You can add a explicit tiling varibale like: \"-tile 8x8\" or \"-tile 12x\"\nThat would give 8x8 Tiles or 12 Tiles in X and Y calculated automatically.\nChange style variables as you like.\n\nChangeOutput  'Filename' as you like.\n\nIf you inserted a \"Split\" to split up the whole setup in 2 or more  seperate Contact Sheets, use _p0, _p1, ... nodename postfix.")
	hou_sticky.setTextSize(0)
	hou_sticky.setTextColor(hou.Color((0, 0, 0)))
	hou_sticky.setDrawBackground(True)
	hou_sticky.setPosition(hou.Vector2(4.31289, -15.8599))
	hou_sticky.setSize(hou.Vector2(8.17024, 2.7729))
	hou_sticky.setColor(hou.Color([0.451, 0.369, 0.796]))


	#topnet_glob/__stickynote4
	hou_sticky = hou_parent.createStickyNote("__stickynote4")
	hou_sticky.setText("Important to export as .webm video. Only supported format in Mutagen Viewer Panel. If you need another format, just split off another branch with another FFmpeg TOP:\n\nExplicitly set to LocalScheduler, mostly faster then on the farm.\n\nIf you inserted a \"Split\" to split up the whole setup in 2 or more  seperate Contact Sheets, use _p0, _p1, ... nodename postfix.")
	hou_sticky.setTextSize(0)
	hou_sticky.setTextColor(hou.Color((0, 0, 0)))
	hou_sticky.setDrawBackground(True)
	hou_sticky.setPosition(hou.Vector2(4.31289, -21.0536))
	hou_sticky.setSize(hou.Vector2(8.17024, 2.34767))
	hou_sticky.setColor(hou.Color([0.145, 0.667, 0.557]))


	#topnet_glob/__stickynote5
	hou_sticky = hou_parent.createStickyNote("__stickynote5")
	hou_sticky.setText("Node just grabs the current wedgenum array as string in Python Expression, should be referenced in all Output Paths in ROPs. See Example in ROPNET.")
	hou_sticky.setTextSize(0)
	hou_sticky.setTextColor(hou.Color((0.4, 0.4, 0.4)))
	hou_sticky.setDrawBackground(True)
	hou_sticky.setPosition(hou.Vector2(4.31289, 4.05587))
	hou_sticky.setSize(hou.Vector2(8.17024, 1.59761))
	hou_sticky.setColor(hou.Color([0, 0, 0]))


	#topnet_glob/__stickynote6
	hou_sticky = hou_parent.createStickyNote("__stickynote6")
	hou_sticky.setText("Mostly more efficient to set it to render a couple Frames per Batch for very fast and small preview renders. Set to 'Single Frame', as it inherits Frame Range from Geo Ropfetch.")
	hou_sticky.setTextSize(0)
	hou_sticky.setTextColor(hou.Color((0, 0, 0)))
	hou_sticky.setDrawBackground(True)
	hou_sticky.setPosition(hou.Vector2(4.3129, -9.58676))
	hou_sticky.setSize(hou.Vector2(8.17024, 1.39102))
	hou_sticky.setColor(hou.Color([0.624, 0.329, 0.396]))


	#topnet_glob/__stickynote7
	hou_sticky = hou_parent.createStickyNote("__stickynote7")
	hou_sticky.setText("ROP Nodes just as templates for Output Filepath expressions.\nFetch ROPs from wherever you like...")
	hou_sticky.setTextSize(0)
	hou_sticky.setTextColor(hou.Color((0, 0, 0)))
	hou_sticky.setDrawBackground(True)
	hou_sticky.setPosition(hou.Vector2(-9.39003, -7.67198))
	hou_sticky.setSize(hou.Vector2(5.16529, 1.17925))
	hou_sticky.setColor(hou.Color([0.996, 0.682, 0.682]))


	#set hou_parent
	hou_parent = hou.node(hou_parent.path()+"/ropnet")


	#topnet_glob/ropnet/__stickynote1
	hou_sticky = hou_parent.createStickyNote("__stickynote1")
	hou_sticky.setText("The expression\n`chs(\"/obj/topnet_glob/CTRL_WEDGES/wedge_expr\")`\nreferences the unique Wedge Index Array currently used in the variation.\n\nUse \"wdg_\" Prefix, which is needed in Mutagen Viewer.")
	hou_sticky.setTextSize(0)
	hou_sticky.setTextColor(hou.Color((0, 0, 0)))
	hou_sticky.setDrawBackground(True)
	hou_sticky.setPosition(hou.Vector2(6.23358, -9.58655))
	hou_sticky.setSize(hou.Vector2(9.16572, 2.03749))
	hou_sticky.setColor(hou.Color([1, 0.529, 0.624]))


	#topnet_glob/ropnet/__stickynote2
	hou_sticky = hou_parent.createStickyNote("__stickynote2")
	hou_sticky.setText("Load output from Geometry ROP with File Node to read back the disk cached results.\nJust use relative channel reference from \"Geometry ROP\" \"Output File\" Parameter.")
	hou_sticky.setTextSize(0)
	hou_sticky.setTextColor(hou.Color((0, 0, 0)))
	hou_sticky.setDrawBackground(True)
	hou_sticky.setPosition(hou.Vector2(6.23358, -13.2533))
	hou_sticky.setSize(hou.Vector2(9.16572, 1.68094))
	hou_sticky.setColor(hou.Color([0.624, 0.329, 0.396]))










#class to hold PDGGraph data retrieved from setupWizard function
class PDGGraphObject():
	def __init__(self, parent=None):

		pdg_mutagen_ui.setupWizard(self)




def insertGraphSplit():

	print "\n"*2
	print "_"*100
	print "Splitting PDG ImageMagick Montage..."


	#hardcoded to 2 for now
	num_splits = 2

	#analyze PDG Graph and get Nodes into object
	pdg_graph_obj = PDGGraphObject()

	#reassign nodes
	pdgchain_nodes = pdg_graph_obj._pdgchain_nodes

	ffmpeg_node = pdg_graph_obj._ffmpeg_node
	imagemagick_node = pdg_graph_obj._imagemagick_node

	wedge_root_node = pdg_graph_obj._wedge_root_node
	parent_topnet = wedge_root_node.parent()
	render_node = pdg_graph_obj._render_node
	render_node_pdg = pdg_graph_obj._render_node_pdg

	#get wedge count from first root wedge node
	root_wedge_count = wedge_root_node.parm("wedgecount").eval()


	#create new split node and position
	new_split_node = parent_topnet.createNode("split", "split_montage")
	new_split_node.setPosition(render_node_pdg.position())
	new_split_node.move([0, -2])
	new_split_node.setInput(0, render_node_pdg)

	split_expr = new_split_node.parm("splitexpression")
	split_expr.setExpression("@wedgenum<"+str((root_wedge_count/num_splits)))


	#make sure ffmpeg node and image_magick node end with split postfix _p0, _p1
	if not ffmpeg_node.name().endswith("_p0"):
		ffmpeg_node.setName(ffmpeg_node.name()+"_p0")

	if not imagemagick_node.name().endswith("_p0"):
		imagemagick_node.setName(imagemagick_node.name()+"_p0")


	#copy / paste remaining nodechain
	old_nodes = []
	old_nodes.append(ffmpeg_node)
	for node in pdgchain_nodes:
		#break loop before appending rende ropfetch node
		if node == render_node_pdg:
			break
		#append
		old_nodes.append(node)
	


	new_nodes = hou.copyNodesTo(old_nodes, parent_topnet)
	#move new stream
	for node in new_nodes:
		node.move([2, -2])
	#set input
	new_nodes[-1].setInput(0, new_split_node, 1)


	#move old stream
	for node in old_nodes:
		node.move([-2, -2])
	#set input
	old_nodes[-1].setInput(0, new_split_node, 0)


	print "_"*100
	print "Finished splitting PDG ImageMagick Montage successfully"
	print "_"*100
	print "\n"*2
	









#convert takes to wedge ui function
def convertTakesToWedgeUI():

	#create wedge node and add parm setup

	#find topnet to put wedge node in
	sel_node = None
	wedge = None
	try:
		sel_node = hou.selectedNodes()[-1]
		if sel_node.type() == hou.nodeType("Top/wedge"):
			parent = sel_node.parent()
			wedge = sel_node
			print "Selected Wedge Node: {}".format(wedge.name())

		else:
			if sel_node.parent().type() == hou.nodeType("Object/topnet"):
				parent = sel_node.parent()
				pos = sel_node.position()
				print "Parent TOP Network to create Wedge Node in: {}\n".format(parent.name())
				
			elif sel_node.type() == hou.nodeType("Object/topnet"):
				parent = sel_node
				pos = [0, 0]
				print "Parent TOP Network to create Wedge Node in: {}\n".format(parent.name())
		
		
			#create node and set parms    
			wedge = parent.createNode("wedge", "wedge_takes")
			wedge.setPosition(pos)
			wedge.move((0, -3))


	except:
		print "No TOP Node, Wedge TOP, or TOPnet selected. Creating default TOPnet."
		parent = hou.node("obj/").createNode("topnet", "topnet_glob")
		wedge = parent.createNode("wedge", "wedge_takes")
		wedge.move((0, -3))



	
	#call function
	remove_takes = False
	remove_takes_int = hou.ui.selectFromList(["Keep", "Remove"], default_choices=([0, ]), exclusive=True, message="Keep Takes after Conversion?", title="Convert Takes to Wedge", column_header="Choices", num_visible_rows=2, clear_on_cancel=False, width=100, height=20)[0]

	if remove_takes_int == 1:
		remove_takes = True

	convertTakesToWedge(wedge, remove_takes)







#main non ui function
def convertTakesToWedge(wedge_node, remove_takes):


	print "\n\nStarting to convert Takes to TOP Wedge...\n"
	print "_"*100
	print "\n"


	wedge = wedge_node
	rem_takes = remove_takes

	#get current update mode
	update_mode_set = hou.updateModeSetting()
	#set update mode to manual
	hou.setUpdateMode(hou.updateMode.Manual)




	#get takelist and sort, get take number
	roottake = hou.takes.rootTake()
	takes = roottake.children()

	takelist = []
	for take in takes:
		takelist.append(take.name())
	#takelist = sorted(takelist)
	num_takes = len(takelist)


	print "Root Take: {}".format(roottake.name())
	print "Number of Child Takes / Wedge Count: {}".format(num_takes)
	print "Takelist: " + str(takelist) + "\n"



	#check if child takes present
	if num_takes > 0:
		#collect all edited parms in takes
		takeparm_list = []

		for takename in takelist:
			take = hou.takes.findTake(takename)
			#print "Takename: " + take.name()
			
			takeparms = take.parmTuples()
			for takeparm in takeparms:
				if takeparm not in takeparm_list:
					takeparm_list.append(takeparm)
					#print "Take Parameter appended to list: " + str(takeparm)
			
		num_takeparms = len(takeparm_list)
		print "{} edited Parameters found in Takes\n".format(num_takeparms)



		print "\nProcessing all edited Parameters in Takes."
		print "This might take up to a couple of minutes for very complex setups..."
			
		#set inital parms
		parm_wedgecount = wedge.parm("wedgecount")
		parm_wedgecount.set(num_takes)

		parm_wedgeattribs = wedge.parm("wedgeattributes")
		parm_wedgeattribs.set(num_takeparms)

		parm_preservenum = wedge.parm("preservenum")
		parm_preservenum.set(1)

		parm_previewselection = wedge.parm("previewselection")
		parm_previewselection.set(1)


		#edit interface wo hide wedge attribute parms for preformance

		parm_group = wedge.parmTemplateGroup()
		attribs_parm_temp = parm_group.find("wedgeattributes")
		attribs_parm_temp_clone = attribs_parm_temp.clone()

		new_parm_folder = hou.FolderParmTemplate("parent_folder", "Wedge Attributes (Hidden)", folder_type=hou.folderType.Collapsible, default_value=0, ends_tab_group=False)

		parm_group.remove(attribs_parm_temp)
		new_parm_folder.addParmTemplate(attribs_parm_temp_clone)
		parm_group.append(new_parm_folder)

		wedge.setParmTemplateGroup(parm_group)



		#fill in takeparms
		i = 1
		for takeparm in takeparm_list:

			#print takeparm
			#list of parm tuples!!!
			takeparm_path = takeparm.node().path()+"/"+takeparm.name()
			
			takeparm_type = type(takeparm[0].eval())
			takeparm_is_tuple = len(takeparm) > 1
			
			#print takeparm.eval()
			#print takeparm_type
			#print "Is Tuple: " + str(takeparm_is_tuple)
			
			#set
			parm_name = wedge.parm("name"+str(i))
			parm_name.set(takeparm.name()+"_"+str(i))

			
			parm_exportchannel = wedge.parm("exportchannel"+str(i))
			parm_exportchannel.set(1)
			
			parm_channel = wedge.parm("channel"+str(i))
			parm_channel.set(takeparm_path)
			
			parm_type = wedge.parm("type"+str(i))
			if takeparm_type == float and takeparm_is_tuple == False:
				parm_type.set(0)
			if takeparm_type == float and takeparm_is_tuple == True:
				parm_type.set(1)
			if takeparm_type == int and takeparm_is_tuple == False:
				parm_type.set(2)
			if takeparm_type == int and takeparm_is_tuple == True:
				parm_type.set(3)
			if takeparm_type == str:
				parm_type.set(4)
				
			parm_wedgetype = wedge.parm("wedgetype"+str(i))
			parm_wedgetype.set(2)
			
			parm_values = wedge.parm("values"+str(i))
			parm_values.set(num_takes)
			
			#incr
			i += 1
		   
		

		#iterate over takes again, actually set them active and evaluate & set corresponding parms in wedge
		root_take = hou.takes.rootTake()

		t = 1
		for takename in takelist:
			take = hou.takes.findTake(takename)
			#print "Set to Take: " + take.name()
			hou.takes.setCurrentTake(take)
			
			#fill in takeparms again with evalueted values from takes
			i = 1
			for takeparm in takeparm_list:
				
				#takeparm attribs
				takeparm_path = takeparm.node().path()+"/"+takeparm.name()
			
				takeparm_type = type(takeparm[0].eval())
				takeparm_size = len(takeparm)
				takeparm_is_tuple = takeparm_size > 1
				
				#check type and set valname accordingly
				if takeparm_type == float and takeparm_is_tuple == False:
					valname = "floatvalue"
				if takeparm_type == float and takeparm_is_tuple == True:
					valname = "floatvector"
				if takeparm_type == int and takeparm_is_tuple == False:
					valname = "intvalue"
				if takeparm_type == int and takeparm_is_tuple == True:
					valname = "intvector"
				if takeparm_type == str:
					valname = "strvalue"
				
					
				#if tuple and size is 3 append 0 so it matches size of vector4 tuples in wedge node    
				
				parm_val = wedge.parmTuple(valname+str(i)+"_"+str(t))
				
				if takeparm_size == 3:
					val_t = takeparm.eval()
					val_l = list(val_t)
					val_l.append(0)
					val = tuple(val_l)
									
				else:
					val = takeparm.eval()
				
								
				#include parm_val in take so its editable
				take.addParmTuple(parm_val)
				#go back to root take
				hou.takes.setCurrentTake(root_take)
				#set value
				parm_val.set(val)
				#go back to current take
				hou.takes.setCurrentTake(take)
				#exclude parm_val in take to clear
				take.removeParmTuple(parm_val)
						
				
				#incr
				i += 1
				
			#incr
			t += 1


			#remove takes if chosen
			if rem_takes == True:
				#print "Take deleted"
				take.destroy()
			
			
			
		hou.takes.setCurrentTake(root_take)
		#print "\nReset to Root Take"


		#select node
		wedge.setSelected(on=True, clear_all_selected=True)
		wedge.setCurrent(1)

		print "\n"
		print "_"*100
		print "Takes successfully converted to TOP Wedge."
		print "Creating Node UI, this might take another couple seconds."
		print "_"*100
		print "\n"*2


	#exception when no child takes found
	else:
		raise Exception("No Child Takes found.")

	#reset update mode
	hou.setUpdateMode(update_mode_set)









#select wedge index function
def selectWedgeIndexUI():
	
	#get wedge node
	def _isWedgeNode(node):
		#top_type_list = [hou.nodeType("Top/wedge"), hou.nodeType("Top/merge"), hou.nodeType("Top/ropfetch")]
		top_type_list = [hou.nodeType("Top/wedge")]
		if node.type() in top_type_list:
			return True
		else:
			return False
							
	
	node = None
	sel_nodes = hou.selectedNodes()

	if len(sel_nodes) > 0:
		sel_node = sel_nodes[-1]
		if sel_node.type() == hou.nodeType("Top/wedge"):
				node = sel_node
	
	else:
		print "No Wedge TOP selected. Please choose..."
		nodepath = hou.ui.selectNode(title="Select Wedge TOP Node (Last Wedge in Graph Chain)", custom_node_filter_callback=_isWedgeNode)
		node = hou.node(nodepath)
		
		if node == None:
			raise Exception("No Wedge TOP Node selected.")

	
	#enter target idx
	target_wdg_idx = hou.ui.readInput("Please enter Wedge Index. Example: '0_1_4'", buttons=('OK',))[1]
	print "\nTarget Wedge Index: " + target_wdg_idx


	pdgnode = node.getPDGNode()
	#generate static items first to be able to access
	node.generateStaticItems()
	time.sleep(1.5)
	work_items = pdgnode.staticWorkItems


	selectWedgeIndex(target_wdg_idx, node, work_items)


	





def selectWedgeIndex(idx, wedge_node, work_items_in):


	node = wedge_node
	work_items = work_items_in
	target_wdg_idx = idx


	#iterate over work items
	for work_item in work_items:
		wedgenum_l = pdg.intDataArray(work_item, "wedgenum")
		
		wdg_idx = ""
		for wedgenum in wedgenum_l:
			wdg_idx += "_" + str(wedgenum)   
		wdg_idx = wdg_idx[1:]
		

		#select work item
		if wdg_idx == target_wdg_idx:
			work_item_id = work_item.id
			
			node.setSelectedWorkItem(work_item_id)
			print "\nWork Item selected:"
			print "Wedge Index: " + wdg_idx
			#print "ID: " + str(work_item_id)
			
		







#function to create new root wedge node from current mutagen viewer selection
def setupMutationFromMarkedWedges(marked_idx_list, wedge_anchor_node, mode):

	print "\n\nSetup Starting...\n"
	
	idx_list = marked_idx_list
	wedge_node = wedge_anchor_node
	num_wedges = len(idx_list)

	setup_mode = mode


	#print mode
	if setup_mode == 0:
		print "Mode: Convert to Takes (del. existing Takes)\n"
	elif setup_mode == 1:
		print "Mode: Convert to Takes (keep existing Takes)\n"
	elif setup_mode == 2:
		print "Mode: Convert to TOP Wedge (del. existing Takes)\n"



	#get current update mode
	update_mode_set = hou.updateModeSetting()
	#set update mode to manual
	hou.setUpdateMode(hou.updateMode.Manual)
	#set auto takes on
	hou.hscript("takeautomode on")


	#get root take
	roottake = hou.takes.rootTake()
	print "Root Take: {}".format(roottake.name())



	#cook pdg node first
	pdgnode = wedge_node.getPDGNode()
	#generate static items first to be able to access
	wedge_node.generateStaticItems()
	time.sleep(1.5)
	work_items = pdgnode.staticWorkItems


	if setup_mode == 0 or setup_mode == 2:
		#remove all existing takes first
		takes = roottake.children()
		for take in takes:
			take.destroy()



	#convert wedges to takes
	for idx in idx_list:
		take = roottake.addChildTake(idx)
		hou.takes.setCurrentTake(take)

		selectWedgeIndex(idx, wedge_node, work_items)

	#return to root take
	hou.takes.setCurrentTake(roottake)


	#reset update mode
	hou.setUpdateMode(update_mode_set)
	#set auto takes off
	hou.hscript("takeautomode off")


	print "\nSuccessfully converted Wedges to Takes\n"


	

	#if mode is Convert to TOP Wedge
	if setup_mode == 2:

		#create new wedge node in same Topnet as wedge_anchor_node
		topnet = wedge_node.parent()
		new_wedge_node = topnet.createNode("wedge", "wedge_base_from_marked")

		new_wedge_node.setPosition(wedge_node.position())
		new_wedge_node.move([-5, 0])
		#new_wedge_node.setSelected(1, clear_all_selected=True)

		remove_takes = True


		convertTakesToWedge(new_wedge_node, remove_takes)