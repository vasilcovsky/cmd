#!/usr/bin/env python
import thrift
import json
from optparse import OptionParser
from concord_cli.utils import *

def generate_options():
    usage = "usage: %prog [options] arg"
    parser = OptionParser(usage)
    parser.add_option("--zookeeper-hosts", dest="zookeeper",
                      action="store", help="i.e: 1.2.3.4:2181,2.3.4.5:2181")
    parser.add_option("--name", dest="name", action="store")
    parser.add_option("--instances", dest="instances", action="store")
    parser.add_option("--zookeeper-path", action="store", dest="zk_path")
    return parser

def validate_options(options, parser):
    if not options.name: parser.error("please specify --name")
    if not options.zk_path: parser.error("please specify --zookeeper-path")
    if not options.zookeeper: parser.error("please specify --zookeeper-hosts")

    if not options.instances: parser.error("please specify --instances")
    else: options.instances = int(options.instances)

def scale(options):
    print "Getting master ip from zookeeper"
    ip = get_zookeeper_master_ip(options.zookeeper, options.zk_path)
    print "Found leader at: ", ip
    (addr, port) = ip.split(":")
    print "Initiating connection to scheduler"
    cli = get_sched_service_client(addr,int(port))
    print "Sending request to scheduler"
    try:
        cli.scaleComputation(options.name, options.instances)
    except BoltError as e:
        print "Error scaling: ", e
    print "Done sending request to server"


def main():
    parser = generate_options()
    (options, args) = parser.parse_args()
    validate_options(options,parser)
    scale(options)

if __name__ == "__main__":
    main()
