def SetupPayloads(inp):
	flow_input = {
		"input": {
			"inject_source_endpoint_id":inp['sourceEP'],
			"inject_source_path":inp['sourcePath'],
			"inject_destination_endpoint_id":inp['remoteDataEP'],
			"extract_source_endpoint_id":inp['remoteDataEP'],
			"funcx_endpoint_compute":inp['funcx_endpoint_compute'],
			"inject_destination_path":inp['executePath'],
			"extract_source_path":inp['executeResultPath'],
			"extract_destination_endpoint_id":inp['destEP'],
			"extract_destination_path":inp['resultPath'],
			"paramFileName":inp['pfName'],
			"startLayerNr":inp['startLayerNr'],
			"endLayerNr":inp['endLayerNr'],
			"nFrames":inp['nFrames'],
			"numProcs":inp['numProcs'],
			"numBlocks":inp['numBlocks'],
			"timePath":inp['timePath'],
			"StartFileNrFirstLayer":inp['startNrFirstLayer'],
			"NrFilesPerSweep":inp['nrFilesPerSweep'],
			"FileStem":inp['fileStem'],
			"SeedFolder":inp['seedFolder'],
			"darkFN":inp['darkFN'],
			"StartNr":inp['startNr'],
			"EndNr":inp['endNr'],
			'extract_recursive':False,
			'inject_recursive':True,}
		}
	flow_input['input'].update({'multipletasks':[{
				'startLayerNr':inp['startLayerNr'],
				'endLayerNr':inp['endLayerNr'],
				'numProcs':inp['numProcs'],
				'nFrames':inp['nFrames'],
				'numBlocks':inp['numBlocks'],
				'blockNr':idx,
				'timePath':inp['timePath'],
				'FileStem':inp['fileStem'],
				'SeedFolder':inp['seedFolder'],
				'paramFileName':inp['pfName'],
				} for idx in range(inp['numBlocks'])]})
	return flow_input
