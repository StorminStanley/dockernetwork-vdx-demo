import sys
from ncclient import manager
from ncclient import xml_
import ncclient
from st2actions.runners.pythonrunner import Action
from xml.etree import ElementTree as ET



def _callback(call, handler='edit_config', target='running', source='startup', mgr=None):
    try:
        call = ET.tostring(call)
        if handler == 'get':
            call_element = xml_.to_ele(call)
            return ET.fromstring(str(mgr.dispatch(call_element)))
        if handler == 'edit_config':
            mgr.edit_config(target=target, config=call)
        if handler == 'delete_config':
            mgr.delete_config(target=target)
        if handler == 'copy_config':
            mgr.copy_config(target=target, source=source)
    except (ncclient.transport.TransportError,
            ncclient.transport.SessionCloseError,
            ncclient.transport.SSHError,
            ncclient.transport.AuthenticationError,
            ncclient.transport.SSHUnknownHostError) as error:
        logging.error(error)
        raise DeviceCommError


def interface_vlan_interface_ve_global_ve_shutdown(**kwargs):
    """Auto Generated Code
    """
    config = ET.Element("config")
    interface_vlan = ET.SubElement(config, "interface-vlan", xmlns="urn:brocade.com:mgmt:brocade-interface")
    if kwargs.pop('delete_interface_vlan', False) is True:
        delete_interface_vlan = config.find('.//*interface-vlan')
        delete_interface_vlan.set('operation', 'delete')
        
    interface = ET.SubElement(interface_vlan, "interface")
    if kwargs.pop('delete_interface', False) is True:
        delete_interface = config.find('.//*interface')
        delete_interface.set('operation', 'delete')
        
    ve = ET.SubElement(interface, "ve")
    if kwargs.pop('delete_ve', False) is True:
        delete_ve = config.find('.//*ve')
        delete_ve.set('operation', 'delete')
        
    gve_name_key = ET.SubElement(ve, "gve-name")
    gve_name_key.text = kwargs.pop('gve_name')
    if kwargs.pop('delete_gve_name', False) is True:
        delete_gve_name = config.find('.//*gve-name')
        delete_gve_name.set('operation', 'delete')
            
    global_ve_shutdown = ET.SubElement(ve, "global-ve-shutdown")
    if kwargs.pop('delete_global_ve_shutdown', False) is True:
        delete_global_ve_shutdown = config.find('.//*global-ve-shutdown')
        delete_global_ve_shutdown.set('operation', 'delete')
        

    callback = kwargs.pop('callback', _callback)
    return callback(config, mgr=kwargs.pop('mgr'))

class interface_vlan_interface_ve_global_ve_shutdown_act(Action):
    def run(self, delete_global_ve_shutdown, gve_name, delete_interface_vlan, delete_ve, delete_interface, delete_gve_name, host, username, password):
        mgr = manager.connect(host=host,
                              port=22,
                              username=username,
                              password=password,
                              hostkey_verify=False)

        mgr.agtimeout = 600
        interface_vlan_interface_ve_global_ve_shutdown(delete_global_ve_shutdown=delete_global_ve_shutdown, delete_gve_name=delete_gve_name, gve_name=gve_name, delete_interface_vlan=delete_interface_vlan, host=host, delete_ve=delete_ve, delete_interface=delete_interface, username=username, password=password, callback=_callback, mgr=mgr)
        return 0
    