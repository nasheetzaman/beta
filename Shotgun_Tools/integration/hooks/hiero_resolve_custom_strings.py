# Copyright (c) 2014 Shotgun Software Inc.
#
# CONFIDENTIAL AND PROPRIETARY
#
# This work is provided "AS IS" and subject to the Shotgun Pipeline Toolkit
# Source Code License included in this distribution package. See LICENSE.
# By accessing, using, copying or modifying this work you indicate your
# agreement to the Shotgun Pipeline Toolkit Source Code License. All rights
# not expressly granted therein are reserved by Shotgun Software Inc.

from tank import Hook

class HieroResolveCustomStrings(Hook):
	"""Translates a keyword string into its resolved value for a given task."""
	
	RESOLUTION_TOKEN_NAME = "{resolution}"
	TYPE_TOKEN_NAME = "{stype}"
	CLIENT_TOKEN_NAME = "{client}"

	# cache of shots that have already been pulled from shotgun
	_sg_lookup_cache = {}

	def execute(self, task, keyword, **kwargs):
		"""
		"""
		self.parent.log_debug("attempting to resolve custom keyword: %s" % keyword)
		if keyword == self.RESOLUTION_TOKEN_NAME:
			translated_value = self._clip_resolution_string(task)
		elif keyword == self.TYPE_TOKEN_NAME:
			translated_value = self._clip_type_string(task)
		elif keyword == self.CLIENT_TOKEN_NAME:
			translated_value = self._client_name_string(task)
		else:
			raise RuntimeError("No translation handler found for custom_template_field: %s" % keyword)

		self.parent.log_debug("Custom resolver: %s -> %s" % (keyword, translated_value))
		return translated_value

	# {resolution}
	def _clip_resolution_string(self, task): 
		""" returns sequence resolution or task format override""" 
		width = "" 
		height = ""

		sequence_format = task._sequence.format()

		width = sequence_format.width() 
		height = sequence_format.height()

		if "reformat" in task._preset.properties(): 
			task_reformat_settings = task._preset.properties()["reformat"] 
			if task_reformat_settings['to_type'] != "None": 
				width = task_reformat_settings['width'] 
				height = task_reformat_settings['height']

		return "%sx%s" % (width, height)

	# {stype}
	def _clip_type_string(self, task):
		""" returns current task name""" 
		shot_code = task._item.name()
		filters = [["project", "is", self.parent.context.project],
					["code", "is", shot_code],
					]
		return result

	# {client}
	def _client_name_string(self, task):
		""" returns current pipeline step""" 
		filters = [["project", "is", self.parent.context.project]]
		name = self.parent.shotgun.find_one("Project", filters, ["sg_client"])
		return name["sg_client"]
