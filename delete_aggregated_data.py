from config_parser import ConfigParser
import argparse
import logging
from db_rolling import DBRolling

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
    # get parameters from config file
    parser = ConfigParser(config_filename)
    to_db_class_name = parser.to_db_class_name
    from_db_class_name = parser.from_db_class_name
    from_db_host = parser.from_db_host
    to_db_host = parser.to_db_host
    from_db_port = parser.from_db_port
    to_db_port = parser.to_db_port

    time_before = parser.time_before
    db_rolling = DBRolling(from_db_class_name, to_db_class_name, from_db_host, to_db_host, from_db_port, to_db_port)
    db_rolling.delete_aggregated_data()
    logging.info('Program start deleting aggregated data')
