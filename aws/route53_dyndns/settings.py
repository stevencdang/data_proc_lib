from boto.route53 import connection
from boto.pyami import config
import boto
import ConfigParser

import logging

#Setup logging
log_level = logging.DEBUG
logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(log_level)


class Settings(object):

	config = None
	access_key = None
	secret_key = None
	zone_id = 'Z3DDPTYQOOEYGN'
	zone_name = 'scdangit.com.'
	record_name = 'pollenoffice2.scdangit.com.'

	def __init__(self):
		self.get_config()
	
	# Load Configuration paraneters
	def get_config(self):
		self.config =ConfigParser.ConfigParser()
		self.config.read('/etc/boto.cfg')
		self.access_key = self.config.get('Credentials', 'aws_access_key_id')
		self.secret_key = self.config.get('Credentials', 'aws_secret_access_key')



if __name__ == '__main__':

#aws_access_key_id=cfg.access_key,
					   #aws_secret_access_key=cfg.secret_key)
	#aws = boto.connect_route53(cfg.access_key,
				   #cfg.secret_key)
	logger.debug('got connection sith host %s and api version %s' % (aws.DefaultHost, aws.Version))
	zones = aws.get_zones()
	zone = aws.get_hosted_zone(cfg.zone_id)
	logger.debug('number of zones:%d' % len(zones))
					   
