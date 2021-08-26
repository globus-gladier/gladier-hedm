def SetupPayloads(inp):
	common_payload = {
		"paramFileName.$":"$.input.pfname",
		"startLayerNr.$":"$.input.startLayerNr",
		"endLayerNr.$":"$.input.endLayerNr",
		"nFrames.$":"$.input.nFrames",
		"numProcs.$":"$.input.numProcs",
		"numBlocks.$":"$.input.numBlocks",
		"timePath.$":"$.input.timePath",
		"StartNrFirstLayer.$":"$.input.StartFileNrFirstLayer",
		"NrFilesPerSweep.$":"$.input.NrFilesPerSweep",
		"FileStem.$":"$.input.FileStem",
		"SeedFolder.$":"$.input.SeedFolder",
		"StartNr.$":"$.input.StartNr",
		"EndNr.$":"$.input.EndNr"}
	flow_input = {
		"input": {
			"source_endpoint":inp['sourceEP'],
			"source_path":inp['sourcePath'],
			"execute_endpoint":inp['remoteDataEP'],
			"funcx_endpoint_compute":inp['funcx_endpoint_compute'],
			"execute_path":inp['executePath'],
			"execute_result_path":inp['executeResultPath'],
			"result_endpoint":inp['destEP'],
			"result_path":inp['resultPath'],
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
			"StartNr":inp['startNr'],
			"EndNr":inp['endNr'],}
		}
	flow_input['input'].update({'tasks_multiple':[{
			'startLayerNr':'$.input.startLayerNr',
			'endLayerNr':'$.input.endLayerNr',
			'numProcs':'$.input.numProcs',
			'nFrames':'$.input.nFrames',
			'numBlocks':'$.input.numBlocks',
			'blockNr':f'{idx}',
			'timePath':'$.input.timePath',
			'FileStem':'$.input.FileStem',
			'SeedFolder':'$.input.SeedFolder',
			'paramFileName':'$.input.paramFileName',
			}] for idx in range(inp['numBlocks'])})
	flow_input['input'].update({'indexrefine_tasks':[{
			'endpoint.$':'$.input.funcx_endpoint_compute',
			'function.$':'$.input.remote_indexrefine_funcx_id',
			'payload.$':f'$.input.tasks_multiple[{idx}]'
		} for idx in range(inp['numBlocks'])]})
	flow_input['input'].update({'peaksearch_tasks':[{
			'endpoint.$':'$.input.funcx_endpoint_compute',
			'function.$':'$.input.remote_peaksearch_funcx_id',
			'payload.$':f'$.input.tasks_multiple[{idx}]'
		} for idx in range(inp['numBlocks'])]})
	return flow_input
