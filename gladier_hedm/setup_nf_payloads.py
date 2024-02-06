def SetupNFPayloads(inp):
	flow_input = {
		"input": {
			"inject_source_endpoint_id":		inp['sourceEP'],
			"compute_endpoint_noqueue":			inp['sourceNCEP'],
			"proc_endpoint_non_compute":		inp['procNCEP'],
			"inject_source_path":				inp['sourcePath'],
			"inject_destination_endpoint_id":	inp['remoteDataEP'],
			"extract_source_endpoint_id":		inp['remoteDataEP'],
			"compute_endpoint":					inp['compute_endpoint'],
			"inject_destination_path":			inp['executePath'],
			"extract_source_path":				inp['executeResultPath'],
			"extract_destination_endpoint_id":	inp['destEP'],
			"extract_destination_path":			inp['resultPath'],
			"paramFile":						inp['pfName'],
			"startLayerNr":						inp['startLayerNr'],
			"endLayerNr":						inp['endLayerNr'],
			"FF_Seed":							inp['FF_Seed'],
			"numProcs":							inp['numProcs'],
			"numBlocks":						inp['numBlocks'],
			"timePath":							inp['timePath'],
			"TopDataDirectory":					inp['TopDataDirectory'],
			"OrigFileName":						inp['OrigFileName'],
			'extract_recursive':				False,
			'inject_recursive':					True,}
		}
	flow_input['input'].update({
			'multipletasks':[{
				'startLayerNr':inp['startLayerNr'],
				'endLayerNr':inp['endLayerNr'],
				'numProcs':inp['numProcs'],
				'TopDataDirectory':inp['TopDataDirectory'],
				'numBlocks':inp['numBlocks'],
				'blockNr':idx,
				'OrigFileName':inp['OrigFileName'],
				'paramFile':inp['pfName'],
				}
			for idx in range(inp['numBlocks'])
		]
	})
	flow_input['input'].update({
			'mediantasks':[{
				'startLayerNr':inp['startLayerNr'],
				'endLayerNr':inp['endLayerNr'],
				'TopDataDirectory':inp['TopDataDirectory'],
				'distanceNr':idx2,
				'OrigFileName':inp['OrigFileName'],
				'paramFile':inp['pfName'],
				}
			for idx2 in range(1,1+inp['nDistances'])
		]
	})
	return flow_input
