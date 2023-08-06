#!/usr/bin/env python

import io
import pickle
import subprocess
from subprocess import STDOUT
from uuid import UUID

from xpycommon.ui import green, blue, yellow, red, INDENT
from xpycommon.log import Logger

import pkg_resources
from halo import Halo
from bthci import ADDR_TYPE_PUBLIC
from btgatt import Service, CharactValueDeclar, ServiceUuids, GattAttrTypes, bt_base_uuid, \
    GattClient, ReadCharactValueError, ReadCharactDescriptorError, CharactProperties

from .. import BlueScanner, ScanResult
from .ui import LOG_LEVEL
from .gatt_scan_bt_agent import GattScanBtAgent


logger = Logger(__name__, LOG_LEVEL)

service_uuid_file = pkg_resources.resource_stream(__name__, "../res/gatt-service-uuid.txt")
service_uuid_file = io.TextIOWrapper(service_uuid_file)

char_uuid_file = pkg_resources.resource_stream(__name__, '../res/gatt-characteristic-uuid.txt')
char_uuid_file = io.TextIOWrapper(char_uuid_file)

descriptor_uuid_file = pkg_resources.resource_stream(__name__, '../res/gatt-descriptor-uuid.txt')
descriptor_uuid_file = io.TextIOWrapper(descriptor_uuid_file)

services_spec = {}
characteristics_spec = {}
descriptors_spec = {}

BT_BASE_UUID = '00000000-0000-1000-8000-00805F9B34FB'
BT_BASE_UUID_SUFFIX = "-0000-1000-8000-00805F9B34FB"

for line in service_uuid_file:
    items = line.strip().split('\t')
    uuid = items.pop(2)
    services_spec[uuid] = {
        'Name': items[0],
        'Uniform Type Identifier': items[1],
        'Specification': items[2]
    }

for line in char_uuid_file:
    items = line.strip().split('\t')
    uuid = items.pop(2)
    characteristics_spec[uuid] = {
        'Name': items[0],
        'Uniform Type Identifier': items[1],
        'Specification': items[2]
    }

for line in descriptor_uuid_file:
    items = line.strip().split('\t')
    uuid = items.pop(2)
    descriptors_spec[uuid] = {
        'Name': items[0],
        'Uniform Type Identifier': items[1],
        'Specification': items[2]
    }
    

def full_uuid_str_to_16_int(uuid: str):
    """return 16-bit int or original uuid """
    if uuid.startswith("0000") and uuid.endswith(BT_BASE_UUID_SUFFIX):
        uuid = int(uuid.removeprefix('0000').removesuffix(BT_BASE_UUID_SUFFIX), base=16)
    return uuid


def attr_permissions2str(permissions: dict):
    permi_str = ''
    
    read_flags = []
    write_flags = []
    
    if permissions is None:
        return red("Unknown")

    if permissions['read']['enable']:
        permi_str += 'Read'
        
        if permissions['read']['authen'] or permissions['read']['author'] or permissions['read']['higher']:
            permi_str += "("
        
            if permissions['read']['authen']:
                read_flags.append("authen")
        
            if permissions['read']['author']:
                read_flags.append("author")

            if permissions['read']['higher']:
                read_flags.append("higher")
            
            permi_str += ' '.join(read_flags)
            permi_str += ")"
        elif not (permissions['write']['enable'] or permissions['encrypt'] or permissions['higher']):
            return "Read Only, No Authentication, No Authorization"

        permi_str += ' '
        
    if permissions['write']['enable']:
        permi_str += 'Write'
        
        if permissions['write']['authen'] or permissions['write']['author'] or permissions['write']['higher']:
            permi_str += "("
        
            if permissions['write']['authen']:
                write_flags.append("authen")
        
            if permissions['write']['author']:
                write_flags.append("author")

            if permissions['write']['higher']:
                write_flags.append("higher")

            permi_str += ' '.join(write_flags)
            permi_str += ")"
        
        permi_str += ' '
    
    if permissions['encrypt']:
        permi_str += 'Encrypt'
        permi_str += ' '
    
    if permissions['higher']:
        permi_str += 'Higher layer profile or implementation specific'
        permi_str += ' '
        
    return permi_str


class GattScanResult(ScanResult):
    """A series of service definitions constitute the main part of this result."""
    def __init__(self, addr: str = None, addr_type: str = None):
        """
        addr      - Bluetooth address of the scanned device
        addr_type - public or random
        """
        super().__init__('GATT')

        self.addr = addr
        self.addr_type = addr_type
        self.services = []

    def add_service(self, service: Service):
        self.services.append(service)
        
    def uuid2str_for_show(self, uuid: UUID) -> str:
        if uuid.bytes[4:] == bt_base_uuid.bytes[4:]:
            if uuid.bytes[:2] == b'\x00\x00':
                uuid_str_for_show = '{:04X}'.format(int.from_bytes(
                    uuid.bytes[2:4], 'big', signed=False))
            else:
                uuid_str_for_show = '{:08X}'.format(int.from_bytes(
                    uuid.bytes[0:4], 'big', signed=False))
        else:
            uuid_str_for_show = str(uuid).upper()
            
        return uuid_str_for_show

    def print(self):
        if self.addr is None or self.addr_type is None:
            return

        print("Number of services: {}".format(len(self.services)))
        print()
        print() # Two empty lines before Service Group
        
        # Prints each service group
        for service in self.services:
            uuid_str_for_show = self.uuid2str_for_show(service.declar.value)

            try:
                service_name = green(ServiceUuids[service.declar.value].name)
            except KeyError:
                service_name = red("Unknown")

            print(blue("Service"), "(0x{:04x} - 0x{:04x}, {} characteristics)".format(
                service.start_handle, service.end_handle, len(service.get_characts())))
            print(INDENT + blue("Declaration"))
            print(INDENT*2 + "Handle: 0x{:04x}".format(service.start_handle))
            print(INDENT*2 + "Type:   {:04X} ({})".format(service.declar.type.int16, service.declar.type.name))
            print(INDENT*2 + "Value:  {} ({})".format(green(uuid_str_for_show), service_name))
            print(INDENT*2 + "Permissions:", service.declar.permissions_desc)
            print() # An empty line before Characteristic Group
            
            # Prints each Gharacteristic group
            for charact in service.characts:
                uuid_str_for_show = self.uuid2str_for_show(charact.declar.value.uuid)
                
                # if type(uuid) is int:
                #     uuid = "0x{:04X}".format(uuid)
                    
                # value_declar_uuid = charact.value_declar.type
                # if type(value_declar_uuid) is int:
                #     value_declar_uuid = "0x{:04X}".format(value_declar_uuid)
                    
                # if charact.declar.value.uuid != charact.value_declar.type:
                #     pass
                #     logger.warning("charact.declar.value['UUID'] != charact.value_declar.type")
                    
                try:
                    charact_name = green(GattAttrTypes[charact.declar.value.uuid].name)
                    # charact_name = green(charact_names[charact.declar.value.uuid])
                except KeyError:
                    charact_name = red("Unknown")
                    
                print(INDENT + yellow("Characteristic"), '({} descriptors)'.format(len(charact.descriptors)))
                print(INDENT*2 + yellow("Declaration"))
                print(INDENT*3 + "Handle: 0x{:04x}".format(charact.declar.handle))
                print(INDENT*3 + "Type:   {:04X} ({})".format(charact.declar.type.int16, charact.declar.type.name))
                print(INDENT*3 + "Value:")
                print(INDENT*4 + "Properties: {}".format(green(', '.join(charact.declar.get_property_names()))))
                print(INDENT*4 + "Handle:    ", green("0x{:04x}".format(charact.declar.value.handle)))
                print(INDENT*4 + "UUID:       {} ({})".format(green(uuid_str_for_show), charact_name))
                print(INDENT*3 + "Permissions: {}\n".format(charact.declar.permissions_desc))

                if charact.value_declar is not None:
                    try:
                        value_declar_name = GattAttrTypes[charact.value_declar.type].name
                    except KeyError:
                        value_declar_name = "Unknown"
                        
                    type_str_for_show = self.uuid2str_for_show(charact.value_declar.type)
                    
                    error = charact.value_declar.get_read_error()
                    if error != None:
                        value_print = red(error.desc)
                    elif charact.value_declar.value is None:
                        value_print = red('Unknown')
                    else:
                        value_print = green(str(charact.value_declar.value))
                    
                    print(INDENT*2 + yellow("Value"))
                    print(INDENT*3 + "Handle: 0x{:04x}".format(charact.value_declar.handle))
                    print(INDENT*3 + "Type:   {} ({})".format(type_str_for_show, value_declar_name))
                    print(INDENT*3 + "Value:  {}".format(value_print))
                    print(INDENT*3 + "Permissions: {}\n".format(charact.value_declar.permissions_desc))
                
                # Prints each Characteristic Descriptor
                for descriptor in charact.get_descriptors():
                    uuid = descriptor.type
                    if type(uuid) is int:
                        uuid = "0x{:04X}".format(uuid)
                    
                    error = descriptor.get_read_error()
                    if error != None:
                        value_print = red(error.desc)
                    else:
                        if descriptor.value is None:
                            value_print = red('Unknown')
                        else:
                            value_print = green(str(descriptor.value))
                              
                    print(INDENT*2 + yellow("Descriptor"))
                    print(INDENT*3 + "Handle: {}".format(green('0x{:04x}'.format(descriptor.handle))))
                    print(INDENT*3 + "Type:   {} ({})".format(green("{:04X}".format(descriptor.type.int16)), yellow(descriptor.type.name)))
                    print(INDENT*3 + "Value: ", value_print)
                    print(INDENT*3 + "Permissions: {}\n".format(descriptor.permissions_desc))

    def to_dict(self) -> dict:
        j = {
            "Addr": self.addr,
            "Addr_Type": self.addr_type,
            "services": []
        }
        for service in self.services:
            j["services"].append(service.json())

    def to_json(self) -> str:
        self.to_dict()


class GattScanner(BlueScanner):
    """"""
    def __init__(self, iface: str = 'hci0', io_cap: str = 'NoInputNoOutput'):
        super().__init__(iface=iface)
        
        self.result = GattScanResult()
        self.gatt_client = None
        self.spinner = Halo(placement='right')
        self.bt_agent = GattScanBtAgent(io_cap)
        self.bt_agent.register()

    def scan(self, addr: str, addr_type: int = ADDR_TYPE_PUBLIC) -> GattScanResult:
        logger.debug("Entered scan()")

        try:
            self.result.addr = addr.upper()
            self.result.addr_type = addr_type
                    
            self.gatt_client = GattClient(self.iface)
            
            logger.debug("Address:      {}\n".format(self.result.addr) + 
                         "Address type: {}".format(self.result.addr_type))
            
            try:
                self.spinner.start("Connecting")
                self.gatt_client.connect(self.result.addr, self.result.addr_type)
            except TimeoutError:
                self.spinner.fail()
                raise RuntimeError("Failed to connect remote device {}".format(addr))
            
            try:
                self.spinner.text = "Discovering all primary services"
                services = self.gatt_client.discover_all_primary_services()
            except TimeoutError:
                self.spinner.text = "Reconnecting"
                self.gatt_client.reconnect()
                
                try:
                    self.spinner.text = "Discovering all primary services"
                    services = self.gatt_client.discover_all_primary_services()
                except TimeoutError:
                    raise RuntimeError("Can't discover primary service, the remote device may be not connectable")
            
            logger.debug("number of services: {}".format(len(services)))
            for service in services:
                self.result.add_service(service)
                logger.debug("Service\n" +
                             "start_handle: 0x{:04x}\n".format(service.start_handle) + 
                             "end_handle:   0x{:04x}\n".format(service.end_handle) +
                             "UUID:         {}".format(service.uuid))
        
            self.spinner.text = "Discovering all characteristics of each service"
            
            for service in services:
                try:
                    self.spinner.text = "Discovering all characteristics of service 0x{:04x}".format(service.start_handle)
                    characts = self.gatt_client.discover_all_characts_of_a_service(service)
                    logger.debug("characts: {}".format(characts))
                
                    for charact in characts:
                        logger.debug("Found characteristic declaration\n"
                                     "    Handle: 0x{:04x}\n"
                                     "    Type:   {}\n"
                                     "    Value:\n"
                                     "        Properties: 0x{:02X} - {}\n"
                                     "        Handle:     0x{:04x}\n"
                                     "        UUID:       {}".format(
                                         charact.declar.handle, charact.declar.type, 
                                         charact.declar.value.properties, charact.declar.get_property_names(), 
                                         charact.declar.value.handle, charact.declar.value.uuid))
                        service.add_charact(charact)
                except TimeoutError as e:
                    # When discovering all characteristics fo a service encounters a timeout,
                    # reconnect and try once again
                    self.spinner.text = "Reconnecting"
                    self.gatt_client.reconnect()
                    
                    try:
                        characts = self.gatt_client.discover_all_characts_of_a_service(service)
                        for charact in characts:
                            service.add_charact(charact)
                    except TimeoutError as e:     
                        logger.error("scan() \n" +
                                     "{}\n".format(e.__class__.__name__) + 
                                    "Discover all characteristics of a service (start 0x{:04x} - end 0x{:04x}".format(
                                        service.start_handle, service.end_handle))
            
            # 这里如果不重连，wireshark 会显示 server 返回的
            # 第一个 ATT_READ_RSP PDU 为 malformed packet。
            # 但是本身并不是 malformed packet，不知道为什么。
            self.spinner.text = "Reconnecting"
            self.gatt_client.reconnect()

            self.spinner.text = "Reading value of each characteristic"
            
            for service in services:
                for charact in service.get_characts():
                    if CharactProperties.READ.name in charact.declar.get_property_names():
                        try:
                            self.spinner.text = "Reading value of a characteristic, value handle = 0x{:04x}".format(charact.declar.value.handle)
                            value = self.gatt_client.read_charact_value(charact)
                            charact.set_value_declar(CharactValueDeclar(charact.declar.value.handle, charact.declar.value.uuid, value))
                            # logger.info("Characteristics Value")
                            # print("Handle: 0x{:04x}".format(charact.value_declar.handle))
                            # print("Type:   {}".format(charact.value_declar.type))
                            # print("Value:  {}".format(charact.value_declar.value))
                        except TimeoutError:
                            # When reading the characteristic value encounters a timeout,
                            # reconnect and try to read once again
                            self.spinner.text = "Reconnecting"
                            print("reconnect")
                            self.gatt_client.reconnect()
                            
                            try:
                                value = self.gatt_client.read_charact_value(charact)
                                charact.set_value_declar(CharactValueDeclar(charact.declar.value.handle, charact.declar.value.uuid, value))
                            except TimeoutError:
                                value_declar = CharactValueDeclar(charact.declar.value.handle, charact.declar.value.uuid, None)
                                value_declar.set_read_error(ReadCharactValueError("Read Timeout"))
                                charact.set_value_declar(value_declar)
                            except ReadCharactValueError as e:
                                value_declar = CharactValueDeclar(charact.declar.value.handle, charact.declar.value.uuid, None)
                                value_declar.set_read_error(e)
                                charact.set_value_declar(value_declar)
                                
                        except ReadCharactValueError as e:
                            value_declar = CharactValueDeclar(charact.declar.value.handle, charact.declar.value.uuid, None)
                            value_declar.set_read_error(e)
                            charact.set_value_declar(value_declar)
            
            self.spinner.text = "Discovering descriptors of each characteristic"
            
            for service in services:
                characts = service.get_characts()
                if len(characts) == 0:
                    continue
                
                for idx in range(0, len(characts) - 1):
                    start_handle = characts[idx].declar.value.handle + 1
                    end_handle = characts[idx+1].declar.value.handle - 1
                    if end_handle < start_handle:
                        continue
                    
                    try:
                        self.spinner.text = "Discovering all descriptors of characteristic 0x{:04x}".format(characts[idx].declar.handle)
                        descriptors = self.gatt_client.discover_all_charact_descriptors(start_handle, end_handle)
                        logger.debug("Number of discovered descriptors: {}".format(len(descriptors)))
                        for descriptor in descriptors:
                            characts[idx].add_descriptor_declar(descriptor)
                    except TimeoutError:
                        self.spinner.text = "Reconnecting"
                        self.gatt_client.reconnect()
                        
                        try:
                            descriptors = self.gatt_client.discover_all_charact_descriptors(start_handle, end_handle)
                            for descriptor in descriptors:
                                characts[idx].add_descriptor_declar(descriptor)
                        except TimeoutError:
                            pass
                
                # Find descriptor of the last charactertisc in current service.
                start_handle = characts[-1].declar.value.handle + 1
                end_handle = service.end_handle
                if end_handle < start_handle:
                    continue
                
                try:
                    self.spinner.text = "Discovering all descriptors of characteristic 0x{:04x}".format(characts[-1].declar.handle)
                    descriptors = self.gatt_client.discover_all_charact_descriptors(start_handle, end_handle)
                    for descriptor in descriptors:
                        characts[-1].add_descriptor_declar(descriptor)
                except TimeoutError:
                    self.spinner.text = "Reconnecting"
                    self.gatt_client.reconnect()
                    
                    try:
                        self.spinner.text = "Discovering all descriptors of characteristic 0x{:04x}".format(characts[-1].declar.handle)
                        descriptors = self.gatt_client.discover_all_charact_descriptors(start_handle, end_handle)
                        for descriptor in descriptors:
                            characts[-1].add_descriptor_declar(descriptor)
                    except TimeoutError:
                        pass
            
            self.spinner.text = "Reading value of each descriptor"
            
            for service in services:
                for characts in service.get_characts():
                    for descriptor in characts.get_descriptors():
                        try:
                            self.spinner.text = "Reading value of the descriptor 0x{:04x}".format(descriptor.handle)
                            value = self.gatt_client.read_charact_descriptor(descriptor.handle)
                            descriptor.set_value(value)
                        except TimeoutError:
                            # When reading the descriptor encounters a timeout,
                            # reconnect and try to read once again
                            self.spinner.text = "Reconnecting"
                            self.gatt_client.reconnect()

                            try:
                                value = self.gatt_client.read_charact_descriptor(descriptor.handle)
                                descriptor.set_value(value)
                            except TimeoutError:
                                descriptor.set_read_error(ReadCharactDescriptorError("Read Timeout"))
                                descriptor.set_value(None)
                            except ReadCharactDescriptorError as e:
                                descriptor.set_read_error(e)
                                descriptor.set_value(None)
                        except ReadCharactDescriptorError as e:
                            descriptor.set_read_error(e)
                            descriptor.set_value(None)

            # secondary_service_groups = req_groups(addr, addr_type, GattAttrTypes.SECONDARY_SERVICE)
            # include_groups = req_groups(addr, addr_type, GattAttrTypes.INCLUDE)
            
            # print(secondary_service_groups)
            # print(include_groups)
        finally:
            self.spinner.stop()
    
            if self.gatt_client is not None:
                self.gatt_client.close()
            
            if self.bt_agent.registered:
                self.bt_agent.unregister()
            try:
                # Reset and clean bluetooth service
                output = subprocess.check_output(' '.join(['bluetoothctl', 'untrust', addr]), 
                                                stderr=STDOUT, timeout=60, shell=True) # 这个 untrust 用于解决本地自动重连被扫描设备的问题
                logger.debug(output.decode())
            except subprocess.CalledProcessError:
                pass

            output = subprocess.check_output(
                ' '.join(['sudo', 'systemctl', 'stop', 'bluetooth.service']), 
                stderr=STDOUT, timeout=60, shell=True)

            output = subprocess.check_output(
                ' '.join(['sudo', 'rm', '-rf', '/var/lib/bluetooth/' + \
                        self.hci_bd_addr + '/' + addr.upper()]), 
                stderr=STDOUT, timeout=60, shell=True)

            output = subprocess.check_output(
                ' '.join(['sudo', 'systemctl', 'start', 'bluetooth.service']), 
                stderr=STDOUT, timeout=60, shell=True)
        
        return self.result
