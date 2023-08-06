#!/usr/bin/env python

import sys
import subprocess
import socket
import struct
from enum import Enum
import traceback

from bluetooth._bluetooth import hci_filter_new
from bluetooth._bluetooth import hci_filter_clear
from bluetooth._bluetooth import hci_open_dev
from bluetooth._bluetooth import hci_close_dev
from bluetooth._bluetooth import hci_filter_set_ptype
from bluetooth._bluetooth import hci_filter_set_event
from bluetooth._bluetooth import hci_send_cmd
from bluetooth._bluetooth import SOL_HCI
from bluetooth._bluetooth import HCI_EVENT_PKT
from bluetooth._bluetooth import EVT_DISCONN_COMPLETE
from bluetooth._bluetooth import HCI_FILTER
from bluetooth._bluetooth import OGF_LINK_CTL
from bluetooth._bluetooth import OCF_DISCONNECT
from bluetooth._bluetooth import EVT_DISCONN_COMPLETE_SIZE
from bluetooth._bluetooth import EVT_REMOTE_NAME_REQ_COMPLETE
from bluetooth._bluetooth import EVT_REMOTE_NAME_REQ_COMPLETE_SIZE
from bluetooth._bluetooth import EVT_CMD_COMPLETE
from bluetooth._bluetooth import hci_filter_set_opcode
from bluetooth._bluetooth import cmd_opcode_pack

from bluetooth._bluetooth import OGF_INFO_PARAM
from bluetooth._bluetooth import OCF_READ_BD_ADDR
from bluetooth._bluetooth import HCI_MAX_EVENT_SIZE

from xpycommon.log import Logger, DEBUG

from xpycommon.bluetooth import IO_CAPABILITY_NOINPUTNOOUTPUT

from bthci.bluez_hci import HCI_CHANNEL_USER
from bthci import HCI, HciOpcodes, ControllerErrorCodes
from bthci.events import HCI_IO_Capability_Request, HCI_IO_Capability_Response, HCI_Link_Key_Request, HCI_Remote_OOB_Data_Request, HciEvent, HciEventCodes, HCI_Command_Status, HCI_LE_Connection_Complete
from bthci.commands import HCI_Write_Encryption_Mode, HCI_Read_Encryption_Mode

from bthci import LinkTypes

logger = Logger(__name__, DEBUG)

OCF_REMOTE_NAME_REQUEST = 0x0019

HCI_PKT_TYPE_SIZE   = 1
EVT_CODE_SIZE       = 1
PARAM_TOTAL_LEN     = 1
NON_EVT_PARAMS_SIZE = HCI_PKT_TYPE_SIZE + EVT_CODE_SIZE + PARAM_TOTAL_LEN


NEXUS_5_BD_ADDR = '58:3F:54:47:9A:1D'
HUAWEI_MATE_X2_BD_ADDR = 'A0:DE:0F:89:68:93'
LENOVO_1770_BD_ADDR = '4B:58:54:CA:21:AD'


def main():
    hci = HCI('hci0', HCI_CHANNEL_USER)
    
    cmd_complete = hci.write_encryption_mode(0x01)
    cmd_complete = hci.read_encryption_mode()
    print(cmd_complete.enc_mode)
    
    hci.write_encryption_mode(0x01)
    # cmd_complete = hci.write_encryption_mode(0x00)
    # cmd_complete = hci.read_encryption_mode()
    # print(cmd_complete.enc_mode)
    
    # cmd_complete = hci.write_encryption_mode(0x01)
    # cmd_complete = hci.read_encryption_mode()
    # print(cmd_complete.enc_mode)
    # cmd_complete = hci.write_encryption_mode(0x00)
    # cmd_complete = hci.read_encryption_mode()
    # print(cmd_complete.enc_mode)
    
    hci.close()
    
    # hci = HCI('hci0', HCI_CHANNEL_USER)
    # cmd_complete = hci.read_simple_pairing_mode()
    # if cmd_complete.status != ControllerErrorCodes.SUCCESS:
    #     logger.error("Failed to read simple paring mode\n"
    #                 "    connection complete status: 0x{:02x} - {}".format(
    #                     conn_complete.status, ControllerErrorCodes[conn_complete.status].name))
    #     hci.close()
    #     sys.exit(1)
    
    # logger.info("Read simple paring mode: {}".format(cmd_complete.simple_pairing_mode))
    
    # ssp_mode = cmd_complete.simple_pairing_mode
    
    # try:
    #     conn_complete = hci.create_connection(HUAWEI_MATE_X2_BD_ADDR)
    #     if conn_complete.status != ControllerErrorCodes.SUCCESS:
    #         logger.error("Failed to create connection to {} BD/EDR address\n"
    #                     "    connection complete status: 0x{:02x} - {}".format(
    #                         HUAWEI_MATE_X2_BD_ADDR,
    #                         conn_complete.status, ControllerErrorCodes[conn_complete.status].name))
    #         sys.exit(1)
    #     # hci.read_remote_supported_features(conn_complete.conn_handle)
    #     # hci.read_remote_extended_features(conn_complete.conn_handle, 1)
    #     hci.authentication_requested(conn_complete.conn_handle)
    #     if ssp_mode == 0x01:
    #         # Secure Simple Pairing
    #         link_key_req = hci.wait_event(HCI_Link_Key_Request.evt_code)
    #         logger.info("Stored link key for {} BD/EDR address is requested".format(link_key_req.bd_addr))
            
    #         cmd_complete = hci.link_key_request_negative_reply(HUAWEI_MATE_X2_BD_ADDR)
    #         if conn_complete.status != ControllerErrorCodes.SUCCESS:
    #             logger.error("Failed tp link key request negative reply to {} BD/EDR address\n"
    #                          "    connection complete status: 0x{:02x} - {}".format(
    #                              HUAWEI_MATE_X2_BD_ADDR,
    #                              conn_complete.status, ControllerErrorCodes[conn_complete.status].name))
    #         io_capability_req =  hci.wait_event(HCI_IO_Capability_Request.evt_code)
    #         logger.info("IO Capability for {} BD/EDR address is requested".format(io_capability_req.bd_addr))
            
    #         oob_data_present = 0x00
    #         cmd_complete = hci.io_capability_request_reply(HUAWEI_MATE_X2_BD_ADDR, IO_CAPABILITY_NOINPUTNOOUTPUT, oob_data_present, 0x00)
    #         if cmd_complete.status != ControllerErrorCodes.SUCCESS:
    #             logger.error("Failed to io capability request reply\n"
    #                         "    connection complete status: 0x{:02x} - {}".format(
    #                             conn_complete.status, ControllerErrorCodes[conn_complete.status].name))
    #         if oob_data_present != 0x00:
    #             remote_oob_data_req = hci.wait_event(HCI_Remote_OOB_Data_Request.evt_code)
                
    #         io_capability_rsp =  hci.wait_event(HCI_IO_Capability_Response.evt_code)
    #         logger.info("Remote IO Capability: {}".format(io_capability_rsp.io_capability))
            
    #     else:
    #         # legacy pairing
    #         pass
        
    
    #     while True:
    #         data = hci.recv(512)
    #         logger.debug("Received data: {}".format(data.hex()))
    #     # hci.disconnect(conn_complete.conn_handle)
    # except Exception as e:
    #     logger.error("{}: \"{}\"".format(e.__class__.__name__, e))
    #     traceback.print_exc()

    # hci.close()


if __name__ == "__main__":
    main()
