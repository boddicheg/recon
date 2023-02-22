from optparse import OptionParser
import logging
import sys

from modules.SyncScanUtils import *

logger = logging.getLogger('recon')
FORMAT = '\x1b[33;20m ->  %(message)s \x1b[0m'
logging.basicConfig(format=FORMAT)
logger.setLevel(logging.DEBUG)

ALLOWED_ACTIONS = ["ip", "waf", "geo", "dirs"]

if __name__ == '__main__':
    actions = ",".join(ALLOWED_ACTIONS)
    target = None

    parser = OptionParser(usage='%prog url1 \r\nexample: %prog -a http://www.victim.org/')
    parser.add_option('-a', '--actions', action='store', dest='actions', default=actions,
                    help='All actions ')
    
    options, args = parser.parse_args()
    
    if options.actions:
        actions = options.actions

    if len(args) > 0:
        target = args[0]
        
    if not target:
        logger.error("No target found!")
        sys.exit(0)
        
    funcs = {
        "ip": host_to_ip,
        "waf": wafwoof,
        "geo": not_impl,
        "dirs": not_impl
    }
    
    for action in actions.split(","):
        if action not in ALLOWED_ACTIONS:
            logger.warning("Skipping action {} because its not allowed!".format(action))
            continue
        
        logger.info("Start processing \"{}\" action...".format(action))
        print(funcs[action](target))
            
        
        
        