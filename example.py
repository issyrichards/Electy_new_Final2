
import bmemcached
import time

mc = bmemcached.Client(('mc5.dev.ec2.memcachier.com:11211', ), '4467c8', '97ab1891e5')

def get_labour_proportion():
	issue = raw_input('Your issue >')
	if mc.get('labour_proportion_{0}'.format(issue)) == None:
		labour_proportion = float(5)/float(10)*100
		print 'Labour proportion:',labour_proportion
		mc.set('labour_proportion_{0}'.format(issue), '{0}'.format(labour_proportion), time=30)
		return "{0:.2f}".format(labour_proportion)
	else:
		return mc.get('labour_proportion_{0}'.format(issue))

print get_labour_proportion()