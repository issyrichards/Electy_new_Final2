
import bmemcached
import tweepy
import mandrill

from flask import Flask
from flask import render_template
from flask import request
from datetime import timedelta, datetime

mc = bmemcached.Client(('mc5.dev.ec2.memcachier.com:11211', ), '4467c8', '97ab1891e5')

mandrill_client = mandrill.Mandrill('snbNSMMfFG3IE_VzsGGgqg')

auth = tweepy.OAuthHandler("X2nLW6De6Zc6PdSQeAYoFtzYW","CrO0hNqMwOL1oBy97Hioisqc2yROVmCasWrHxXUhkw3eCdpfTa")
auth.set_access_token("1725724472-oy2grBIetHm8AtTPjpKeu21gjk72zcheNubpgLc", "YINkhxK8TMlQpjuueJByoZvOeNpjJp61eCGsgnUISHe2A")

api = tweepy.API(auth)

def get_date():
	now = datetime.now()
	week_ago = now - timedelta(days=7)
	return str(week_ago)[0:10]

app = Flask(__name__)


def get_labour_tweets(issue):
	tweets = api.search(q=['{0}'.format(issue.replace('_',' ')), 'since:{0}'.format(get_date()), 'from:UKLabour'], count=100)
	print 'Labour tweets:', tweets
	return len(tweets)

def get_conservative_tweets(issue):
	tweets = api.search(q=['{0}'.format(issue.replace('_',' ')), 'since:{0}'.format(get_date()), 'from:Conservatives'], count=100)
	print 'Conservative tweets:', tweets
	return len(tweets)

def get_libdem_tweets(issue):
	tweets = api.search(q=['{0}'.format(issue.replace('_',' ')), 'since:{0}'.format(get_date()), 'from:LibDems'], count=100)
	print 'LibDem tweets:', tweets
	return len(tweets)

def get_UKIP_tweets(issue):
	tweets = api.search(q=['{0}'.format(issue.replace('_',' ')), 'since:{0}'.format(get_date()), 'from:UKIP'], count=100)
	print 'UKIP tweets:', tweets
	return len(tweets)

def get_total_tweets(issue):
	total_tweets = get_labour_tweets(issue.replace('_',' ')) + get_conservative_tweets(issue) + get_libdem_tweets(issue) + get_UKIP_tweets(issue)
	print 'Total tweets:', total_tweets
	if total_tweets > 0:
		return total_tweets
	else:
		return 1

def get_labour_proportion(issue):
	if mc.get('labour_proportion_{0}'.format(issue)) == None:
		labour_proportion = float(get_labour_tweets(issue))/float(get_total_tweets(issue))*100
		print 'Labour proportion:',labour_proportion
		mc.set('labour_proportion_{0}'.format(issue), '{0}'.format(labour_proportion), time=900)
		return "{0:.2f}".format(labour_proportion)
	else:
		return mc.get('labour_proportion_{0}'.format(issue))

def get_conservative_proportion(issue):
	if mc.get('conservative_proportion_{0}'.format(issue)) == None:
		conservative_proportion = float(get_conservative_tweets(issue))/float(get_total_tweets(issue))*100
		print 'Conservative proportion:', conservative_proportion
		mc.set('conservative_proportion_{0}'.format(issue), '{0}'.format(conservative_proportion), time=900)
		return "{0:.2f}".format(conservative_proportion)
	else:
		return mc.get('conservative_proportion_{0}'.format(issue))

def get_libdem_proportion(issue):
	if mc.get('libdem_proportion_{0}'.format(issue)) == None:
		libdem_proportion = float(get_libdem_tweets(issue))/float(get_total_tweets(issue))*100
		print 'Lib Dem proportion:', libdem_proportion
		mc.set('libdem_proportion_{0}'.format(issue), '{0}'.format(libdem_proportion), time=900)
		return "{0:.2f}".format(libdem_proportion)
	else:
		return mc.get('libdem_proportion_{0}'.format(issue))

def get_UKIP_proportion(issue):
	if mc.get('UKIP_proportion_{0}'.format(issue)) == None:
		UKIP_proportion = float(get_UKIP_tweets(issue))/float(get_total_tweets(issue))*100
		print 'UKIP proportion:', UKIP_proportion
		mc.set('UKIP_proportion_{0}'.format(issue), '{0}'.format(UKIP_proportion), time=900)
		return "{0:.2f}".format(UKIP_proportion)
	else:
		return mc.get('UKIP_proportion_{0}'.format(issue))


issue_name = []

@app.route("/")
def get_homepage():
	return render_template('Electyupdate3.html')

@app.route("/<issue>")
def get_tweet_info(issue):
	labour_proportion = get_labour_proportion(issue)
	conservative_proportion = get_conservative_proportion(issue)
	libdem_proportion = get_libdem_proportion(issue)
	UKIP_proportion = get_UKIP_proportion(issue)

	issue_name.append(issue)
	print issue_name

	return render_template('issue.html', issue=issue, labour_proportion=labour_proportion, conservative_proportion=conservative_proportion, libdem_proportion=libdem_proportion, UKIP_proportion=UKIP_proportion)

@app.route("/sign_up", methods=['POST'])
def sign_up():
	form_data = request.form
	email = form_data['email']

	mandrill_client.messages.send(message={'subject':'Your Electy results', 'from_email':'results@electy.com', 'to':[{'email':email}], 'html':"<p>Hi there,</p><p>Thanks for using Electy to help you vote.</p><p>You can keep up-to-date with political conversation about the issue you selected - {0} - <a href=\"www.electy.co.uk/{0}\">here</a>.</p><p>Happy voting,</p><p>The Electy Team</p>".format(issue_name[-1])})

	return render_template('Electyupdate3.html')


if __name__ == "__main__":
	app.run(host="0.0.0.0", port=80, debug=True)
