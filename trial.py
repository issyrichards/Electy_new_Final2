def get_labour_proportion(issue):
	if mc.get('labour_proportion_{0}').format(issue) == None:
		labour_proportion = float(get_labour_tweets(issue))/float(get_total_tweets(issue))*100
		print 'Labour proportion:',labour_proportion
		mc.set('labour_proportion_{0}'.format(issue), '{0}'.format(labour_proportion), time=900)
		return "{0:.2f}".format(labour_proportion)
	else:
		return mc.get('labour_proportion_{0}'.format(issue))