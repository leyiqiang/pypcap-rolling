from config_parser import ConfigParser
import argparse
import logging
from packet_sniffer import PacketSniffer
from addDevices import add_device
from db_rolling import DBRolling
from constants import ADDING_DEVICE_MODE, DELETE_AGGREGATED_DATA_MODE, AGGREGATE_MODE, SNIFFING_MODE

if __name__ == '__main__':
    # parsing user inputs
    arg_parser = argparse.ArgumentParser(description='Arg parser')
    arg_parser.add_argument('-c', '--config',
                            help='YAML configuration file name',
                            required=True)
    arg_parser.add_argument('-d', '--debug',
                            help='Debug mode',
                            type=bool,
                            required=False,
                            default=False)
    input_args = arg_parser.parse_args()
    config_filename = input_args.config
    is_debug = input_args.debug
    # setting debug logging level
    if is_debug:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)

    parser = ConfigParser(config_filename)
    database_class_name = parser.db_class_name
    database_host = parser.db_host
    database_port = parser.db_port
    mode = parser.mode
    logging.debug('DB class name: ' + database_class_name)
    logging.debug('DB host: ' + database_host)
    logging.debug('DB port: ' + database_port)
    logging.debug('mode: ' + mode)

    if mode == SNIFFING_MODE:
        # packet sniffer needs iface and filter info
        logging.info('Program start running in sniffing mode')
        sniff_config = parser.sniff_config
        logging.debug(sniff_config)
        packet_sniffer = PacketSniffer(database_class_name, database_host, database_port, sniff_config)
        packet_sniffer.start_sniffing()
    elif mode == AGGREGATE_MODE:
        time_before = parser.time_before
        db_rolling = DBRolling(database_class_name, database_host, database_port)
        db_rolling.aggregate(time_before)
        logging.info('Program start running in aggregate mode')
    elif mode == DELETE_AGGREGATED_DATA_MODE:
        time_before = parser.time_before
        db_rolling = DBRolling(database_class_name, database_host, database_port)
        db_rolling.delete_aggregated_data(time_before)
        logging.info('Program start deleting aggregated data')
    elif mode == ADDING_DEVICE_MODE:
        add_device(database_class_name, database_host, database_port)
        logging.info('Program start adding devices')
    else:
        logging.warning('Program not running in any mode')
