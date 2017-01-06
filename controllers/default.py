# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

# -------------------------------------------------------------------------
# This is a sample controller
# - index is the default action of any application
# - user is required for authentication and authorization
# - download is for downloading files uploaded in the db (does streaming)
# -------------------------------------------------------------------------
from nmapscanner import *
from pycsvasset import *
from pynessusasset import *
from pynmapasset import *


def index():
    """
    example action using the internationalization operator T and flash
    rendered by views/default/index.html or views/generic.html

    if you need a simple wiki simply replace the two lines below with:
    return auth.wiki()
    """
    return dict()


def manage():
    grid = SQLFORM.smartgrid(db.hosts,linked_tables=['ports'])
    return locals()


def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/bulk_register
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    also notice there is http://..../[app]/appadmin/manage/auth to allow administrator to manage users
    """
    return dict(form=auth())


@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)


def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    return service()

@auth.requires_login()
@auth.requires_membership('execute')
def scan_nmap():
    #TODO: Create new execute page for nmap scans
    pass

@auth.requires_login()
@auth.requires_membership('import')
def import_results():
    #TODO: Create a results page for importing csv, nessus, openvas, and nmap
    form = SQLFORM.factory(Field(" ", default=" ", writable=False),
                           Field("User_Name", 'string', required=True, default=auth.user.username, requires=IS_NOT_EMPTY(),writable=False),
                           Field('User_IP','string', required=True, writable=False, default=request.client,requires=IS_IPV4()),
                           Field('Scan_Type', required=True, requires=IS_IN_SET(['NMAP','CSV','NESSUS'], zero=T("Select Scan Type"), error_message=T('Not a valid option. Please see documentation.'))),
                           Field('Task_ID', 'string'),
                           Field('Approver', 'string'),
                           Field('Description','text'),
                           Field('Scanner_IP','string',requires=IS_IPV4()),
                           Field('Justification','text',required=True, requires=IS_NOT_EMPTY()),
                           Field('Results_File','upload',uploadfolder="/tmp",authorize="upload",required=True),
                           submit_button='Import'
                          )
    if form.process().accepted:
        response.flash = T('Import is being processed! Hold tight.')
        if not form.vars.Scan_Type in ['NMAP','CSV','NESSUS']:
            print("Import Results: Critical: Invalid scan type received!!!")
        else:
            pass            
    elif form.errors:
        response.flash = T('form has errors %s' % error_message)
    else:
        response.flash = T('Please fill out the required information.')
    return dict(form=form)

@auth.requires_login()
@auth.requires_membership('auditor')
def review_hostoverview():
    #TODO: Create  a page which shows everything about hosts network footprint (excluding vulns and software)
    pass
@auth.requires_login()
@auth.requires_membership('auditor')
def review_hostvulns():
    #TODO: Create a page which shows vulnerabilities related to hosts
    pass
@auth.requires_login()
@auth.requires_membership('auditor')
def review_hostsoftware():
    #TODO: Create a page which shows all software related to hosts
    pass
def network_map():
    #TODO: Create a network map based on hops database!
    pass
@auth.requires_login()
@auth.requires_membership('auditor')
def review_scans():
    #TODO: Create a page which essentially just dumps the scans database out in a sql smart grid (use web2py built in)
    pass
@auth.requires_login()
@auth.requires_membership('editor')
def edit_hosts():
    # TODO: SQL smartgrid for hosts database
    pass
@auth.requires_login()
@auth.requires_membership('editor')
def edit_vulnerabilities():
    pass
@auth.requires_login()
@auth.requires_membership('editor')
def edit_ports():
    pass
@auth.requires_login()
@auth.requires_membership('editor')
def edit_softauth():
    pass
@auth.requires_login()
@auth.requires_membership('editor')
def edit_software():
    pass
@auth.requires_login()
@auth.requires_membership('editor')
def edit_hops():
    grid = SQLFORM.smartgrid(db.hops, headers={'hops.ip': 'Hop IP', 'hops.hostname': 'Hop Hostname',
                                                  'hops.scanner_ip': 'Origin Host IP',
                                                  'hops.dst_ip': 'Target IP', 'hops.rtt': 'Time to Hop Host (RTT)',
                                                  'hops.ttl': 'Distance from Origin (TTL)'})

    return dict(form=form)
