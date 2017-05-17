# Copyright (c) 2016 Shotgun Software Inc.
#
# CONFIDENTIAL AND PROPRIETARY
#
# This work is provided "AS IS" and subject to the Shotgun Pipeline Toolkit
# Source Code License included in this distribution package. See LICENSE.
# By accessing, using, copying or modifying this work you indicate your
# agreement to the Shotgun Pipeline Toolkit Source Code License. All rights
# not expressly granted therein are reserved by Shotgun Software Inc.

"""
Context change hook.
"""

from tank import get_hook_baseclass


class ContextChangeHook(get_hook_baseclass()):
	"""
	Hook that gets executed every single time there is a context change in Toolkit.

		- If an engine **starts up**, the ``current_context`` passed to the hook
		methods will be ``None`` and the ``next_context`` parameter will be set
		to the context that the engine is starting in.

		- If an engine is being **reloaded**, in the context of an engine restart
		for example, the ``current_context`` and ``next_context`` will usually be
		the same.

		- If a **context switch** is requested, for example when a user switches
		from project to shot mode in Nuke Studio, ``current_context`` and ``next_context``
		will contain two different context.

	.. note::

	   These hooks are called whenever the context is being set in Toolkit. It is
	   possible that the new context will be the same as the old context. If
	   you want to trigger some behaviour only when the new one is different
	   from the old one, you'll need to compare the two arguments.
	"""

	def pre_context_change(self, current_context, next_context):
		"""
		Called before the context has changed.

		:param current_context: The context of the engine.
		:param next_context: The context the engine is switching to.
		"""
		pass

	def post_context_change(self, previous_context, current_context):
		"""
		Called after the context has changed.

		:param previous_context: The previous context of the engine.
		:param current_context: The current context of the engine.
		"""
		import sgtk
		engine = sgtk.platform.current_engine()
		if engine.name == 'tk-nuke':
			import nuke
			if nuke.env.get("gui"):
			# running in interactive mode 
				if not nuke.env.get("studio"):
				# running Nuke
					self.__override_nuke_shortcuts(engine, nuke)
				else: 
				# running Nuke Studio
					self.__override_nukestudio_shortcuts(engine, nuke)

	def __override_nuke_shortcuts(self, engine, nuke):
		"""
		Override various shortcut keys in Nuke to run our own commands
		instead

		:param engine: The current engine
		:param nuke: nuke module
		"""
		
		# remove default hotkey from File > Save New Comp Version...
		file_menu = nuke.menu("Nuke").findItem("File")
		save_as_item = file_menu.findItem("Save New Comp Version")
		save_as_item.setShortcut("")
		engine.log_debug("removed default hot key for File > Save Comp As...")
 
		# add new hot key for Shotgun > Shotgun Save As...
		sg_menu = nuke.menu("Nuke").findItem("Shotgun")
		if sg_menu:
			sg_save_as_item = sg_menu.findItem("File Save...")
			if sg_save_as_item:
				sg_save_as_item.setShortcut("Alt+Shift+S")
				engine.log_debug("Set hot key for SG Save...")
			else:
				sg_save_as_item = sg_menu.findItem("Shotgun Workfiles").findItem("File Save...")
				if sg_save_as_item:
					sg_save_as_item.setShortcut("Ctrl+Shift+S")
					engine.log_debug("Set hot key for SG Save Comp As...")

		# remove default hotkey form File > Open Comp...
		open_item = file_menu.findItem("Open Comp...")
		open_item.setShortcut("")
		engine.log_debug("removed default hot key for File > Open...")

		# add new hot key for Shotgun > Shotgun Open...
		if sg_menu:
			sg_open_item = sg_menu.findItem("File Open...")
			if sg_open_item:
				sg_open_item.setShortcut("Ctrl+O")
				engine.log_debug("Set hot key for SG Open Comp...")
			else:
				sg_open_item = sg_menu.findItem("Shotgun Workfiles").findItem("File Open...")
				if sg_opem_item:
					sg_open_item.setShortcut("Ctrl+O")
					engine.log_debug("Set hot key for SG File Open...")
					
		# remove default hotkey for write node
		read_node_item = nuke.menu('Nodes').findItem("Image/Read")
		read_node_item.setShortcut("")
		engine.log_debug("removed default hot key for node Image/Read...")

		# add new hot key for Shotgun Load
		if sg_menu:
			sg_load_item = sg_menu.findItem("Load...")
			if sg_load_item:
				sg_load_item.setShortcut("R")
				engine.log_debug("Set hot key for SG Load...")

	def __override_nukestudio_shortcuts(self, engine, nuke):
		"""
		Override various shortcut keys in Nuke Studio to run our own commands
		instead

		:param engine: The current engine
		:param nuke: nuke module
		"""
		import hiero.ui as ns
		from PySide.QtGui import QKeySequence

		# remove default hotkey from File > Save Project...
		file_save_menu = ns.findMenuAction("Save New Comp Version")
		file_save_menu.setShortcut(QKeySequence(""))
		engine.log_debug("remove default hot key for File > Save Project As...")

		# add new hot key for Shotgun > File Save...
		sg_file_save = ns.findMenuAction("File Save...")
		if sg_file_save:
			#sg_file_save.setShortcut(QKeySequence("Alt+Shift+S"))
			engine.log_debug("set default hot key for File > Shotgun Save Project As...")

		# remove default hotkey from File > Open Project...
		file_open_menu = ns.findMenuAction("Open Project...")
		file_open_menu.setShortcut(QKeySequence(""))
		engine.log_debug("removed default hot key for File > Open Project...")

		# add new hot key for Shotgun > File Open...
		sg_file_open = ns.findMenuAction("File Open...")
		if sg_file_open:
			sg_file_open.setShortcut(QKeySequence('Ctrl+O'))
			engine.log_debug("set default hot key for File > Shotgun Open Project...")