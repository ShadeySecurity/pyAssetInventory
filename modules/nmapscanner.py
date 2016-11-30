#!/usr/bin/env python
# Written by ShadeyShades and SpecialK

# Get our imports in!
import traceback
import json
import sys
import re
import time
import untangle



class SuperScan(object):
    def __init__(self):
        self.nm = None


    #-----------------------------#
    # Name: scan
    # Desc: Does a nmap scan and returns results in data structure
    # Input: hosts - What host or network to scan
    #        options - Nmap options
    # Output: 'Host' data structure with scan output
    #-----------------------------#
    def scan(self, hosts, options):
        import nmap

        self.nm = nmap.PortScanner()
        if len(options) < 2:
            options = '--script nbstat.nse -O -Pn -sV -T3'
        self.nm.scan(hosts, arguments=options)


    #----------------------------#
    # Name: out_struct
    # Desc: Returns nmap results in data structure
    # Input: None
    # Output: List of "Host" namedtuples that contain scan info
    #----------------------------#
    def out_struct(self,xmlobj):
        import re
        import warnings

        #bail if no scan has been conducted.
        if not self.nm:
            warnings.warn('No scan found; please perform scan first.', UserWarning)
            scan = xmlobj
        else:
            scan = self.nm

        # Build data structure keyed on ip address.
        outlist = []
        for host in scan.all_hosts():
            host_dict = {}
            host_dict['ip'] = host
            os_string = ''
            if 'osmatch' in scan[host]:
                os_string = ' or '.join([os['name'] for os in scan[host]['osmatch']])
            host_dict['os'] = os_string
            tcp_ports = ['tcp/'+str(port) for port in scan[host].all_tcp()]
            udp_ports = ['udp/'+str(port) for port in scan[host].all_udp()]
            all_ports = sorted(tcp_ports + udp_ports)
            host_dict['ports'] = all_ports
            host_dict['dns'] = scan[host].hostname()
            netbios_string = ''
            if 'hostscript' in scan[host]:
                for x in scan[host]['hostscript']:
                    m = re.search('(?<=NetBIOS name: )[^,]+', x['output'])
                    netbios_string = m.group(0)
            host_dict['netbios'] = netbios_string
            outlist.append(host_dict)

        return outlist


    #----------------------------#
    # Name: out_csv
    # Desc: Returns nmap results in csv string
    # Input: None
    # Output: Csv string containing all scan data
    #----------------------------#
    def out_csv(self):
        return self.nm.csv()


    #-----------------------------#
    # Name: customscan
    # Desc: Runs a customscan and returns results as an object
    # Input: scanhosts - what to scan
    #        scanspeed - how fast to scan
    #        scanopts  - what options to scan with
    # Outputs: xmlobj - object of the results
    #-----------------------------#

    def customscan(self, scanhosts, scanspeed, scanopts):
        # Very important we validate our input as it comes from a web input
        validate = []
        validate.append(re.match(r'^[0-9a-zA-Z\-\.\-]{0,128}$',scanhosts))
        validate.append(re.match(r'^[1-5]$', scanspeed))
        validate.append(re.match(r'^[0-9a-zA-Z\-\.\-]{0,256}$', scanhopts))
        if None in validate or False in validate:
            print("Customscan: CRITICAL: Invalid input received! Dieing now.")
            # Scorch earth if we dont get what we want!
            exit(1)
        # Create unique file for grab by our internal process, we need it to be unique for multiple users
        scanme = "scanme%s" % (time.strftime("%Y%m%d%H%M%S"))
        # Where we writing to
        writelocation = "/tmp/%s" % (scanme)
        # Open the file now
        cronfile = open(writelocation,'w')
        # Now we write to the file the instruction to run in cron, there will be a secondary script to run this!
        xmlfile = "/tmp/%s.xml" % (scanme)
        grepfile = "/tmp/%s.ngrep" % (scanme)
        # Write to cron file
        cronfile.write("nmap -T %s %s %s -oX %s -oG %s" % (scanspeed,scanopts,scanhosts,xmlfile,grepfile))
        cronfile.close()
        #wait 5 for script to start running
        time.sleep(5)
        grepresults = open(grepfile, 'r')
        for line in grepresults:
            print("%s" % line)
        grepresults.close()
        try:
            xmlobj = untangle.parse(xmlfile)
            return xmlobj
        except Exception as err:
            print("Customscan: Error: %s" % err)
            break

    #----------------------------#
    # Name: outscan
    # Desc: Outputs the nmap results to stdout
    # Input: nmap_report - json format of nmap results
    # Output: none
    #----------------------------#

    def outscan(self, nmap_report):
        print("Starting Nmap {0} ( http://nmap.org ) at {1}".format(
            nmap_report.version,
            nmap_report.started))

        for host in nmap_report.hosts:
            if len(host.hostnames):
                tmp_host = host.hostnames.pop()
            else:
                tmp_host = host.address

            print("Nmap scan report for {0} ({1})".format(
                    tmp_host,
                    host.address))
            print("Host is {0}.".format(host.status))
            print("  PORT     STATE         SERVICE")

            for serv in host.services:
                pserv = "{0:>5s}/{1:3s}  {2:12s}  {3}".format(
                    str(serv.port),
                    serv.protocol,
                    serv.state,
                    serv.service)
                if len(serv.banner):
                    pserv += " ({0})".format(serv.banner)
                print(pserv)
        print(nmap_repimport * ort.summary)

    #-----------------------------#
    # Name: scanout
    # Desc: Takes json and outputs it to csv
    # Input: jsonobj - the json to be converted
    #        headers - what headers to actually print
    #        outfile - what file do you write to
    # Output: None
    #----------------------------#

    def scanout(self, jsonobj, headers, outfile):
        parsed_json = json.loads(jsonobj)
        print(parsed_json)
        # TODO actually write the output
