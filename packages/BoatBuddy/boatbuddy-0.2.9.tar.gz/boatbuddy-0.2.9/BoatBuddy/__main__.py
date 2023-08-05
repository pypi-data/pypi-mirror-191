import logging
import optparse
import os
from logging.handlers import RotatingFileHandler

from BoatBuddy import config, utils
from BoatBuddy.console_manager import ConsoleManager
from BoatBuddy.plugin_manager import PluginManager

if __name__ == '__main__':
    # Create an options list using the Options Parser
    parser = optparse.OptionParser()
    parser.set_usage("python3 -m BoatBuddy OUTPUT_DIRECTORY [options]")
    parser.set_defaults(nmea_port=config.DEFAULT_TCP_PORT, filename=config.DEFAULT_FILENAME_PREFIX,
                        interval=config.DEFAULT_DISK_WRITE_INTERVAL, excel=config.DEFAULT_EXCEL_OUTPUT_FLAG,
                        csv=config.DEFAULT_CSV_OUTPUT_FLAG, gpx=config.DEFAULT_GPX_OUTPUT_FLAG,
                        summary=config.DEFAULT_SUMMARY_OUTPUT_FLAG,
                        summary_filename=config.DEFAULT_SUMMARY_FILENAME_PREFIX,
                        verbose=config.DEFAULT_VERBOSE_FLAG, run_mode=config.DEFAULT_SESSION_RUN_MODE,
                        run_mode_interval=config.DEFAULT_SESSION_INTERVAL, log=config.LOG_LEVEL,
                        no_sound=config.DEFAULT_NO_SOUND)
    parser.add_option('--nmea-server-ip', dest='nmea_server_ip', type='string',
                      help=f'Append NMEA0183 network metrics from the specified device IP')
    parser.add_option('--nmea-server-port', dest='nmea_port', type='int', help=f'NMEA0183 host port. ' +
                                                                               f'Default is: {config.DEFAULT_TCP_PORT}')
    parser.add_option('-i', '--interval', type='int', dest='interval',
                      help=f'Disk write interval (in seconds). Default is: ' +
                           f'{config.DEFAULT_DISK_WRITE_INTERVAL} seconds')
    parser.add_option('--excel', action='store_true', dest='excel', help='Generate an Excel workbook.')
    parser.add_option('--csv', action='store_true', dest='csv', help='Generate a comma separated list (CSV) file.')
    parser.add_option('--gpx', action='store_true', dest='gpx', help=f'Generate a GPX file.')
    parser.add_option('-f', '--file', dest='filename', type='string',
                      help=f'Output filename prefix. Default is: {config.DEFAULT_FILENAME_PREFIX}')
    parser.add_option('--summary', action='store_true', dest='summary',
                      help=f'Generate a trip summary excel workbook at the end of the session.')
    parser.add_option('--summary-filename-prefix', dest='summary_filename', type='string',
                      help=f'Summary filename prefix. Default is: {config.DEFAULT_SUMMARY_FILENAME_PREFIX}')
    parser.add_option('-v', '--verbose', dest='verbose', action='store_true',
                      help=f'Verbose mode. Print debugging messages about captured data. ' +
                           f'This is helpful in debugging connection, and configuration problems.')
    parser.add_option('--victron-server-ip', dest='victron_server_ip', type='string',
                      help=f'Append Victron system metrics from the specified device IP')
    parser.add_option('--run-mode', type='string', dest='run_mode',
                      help=f'Session run modes can be: \'auto-victron\', \'auto-nmea\', \'continuous\', ' +
                           f'\'interval\'. Default is: {config.DEFAULT_SESSION_RUN_MODE}')
    parser.add_option('--run-mode-interval', type='int', dest='run_mode_interval',
                      help=f'Session interval (in seconds) to be applied when run mode \'interval\' is specified.' +
                           f' Default is: {config.DEFAULT_SESSION_INTERVAL}')
    parser.add_option('--log', dest='log', type='string',
                      help=f'Desired log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)')
    parser.add_option('--no-sound', dest='no_sound', action='store_true', help=f'Suppress all application sounds')
    (options, args) = parser.parse_args()

    log_numeric_level = getattr(logging, options.log.upper(), None)
    if not isinstance(log_numeric_level, int):
        print(f'Invalid argument: Log level "{options.log}"')
        parser.print_help()
    elif len(args) == 0:  # If the output directory is not provided
        print(f'Invalid argument: Output directory is required\r\n')
        parser.print_help()
    elif not os.path.exists(args[0]):
        print(f'Invalid argument: Valid output directory is required\r\n')
        parser.print_help()
    elif not options.excel and not options.gpx and not options.csv and not options.summary:
        print(f'Invalid argument: At least one output medium needs to be specified\r\n')
        parser.print_help()
    elif not options.nmea_server_ip and not options.victron_server_ip:
        print(f'Invalid argument: At least one system metric needs to be specified (NMEA0183, Victron...)\r\n')
        parser.print_help()
    elif str(options.run_mode).lower() == config.SESSION_RUN_MODE_AUTO_NMEA and not options.nmea_server_ip:
        print(f'Invalid argument: Cannot use the \'auto-nmea\' session run mode ' +
              f'without providing NMEA0183 configuration parameters\r\n')
        parser.print_help()
    elif str(options.run_mode).lower() == config.SESSION_RUN_MODE_AUTO_VICTRON and not options.victron_server_ip:
        print(f'Invalid argument: Cannot use the \'auto-victron\' session run mode ' +
              f'without providing victron server configuration parameters\r\n')
        parser.print_help()
    elif options.interval < config.INITIAL_SNAPSHOT_INTERVAL:
        print(f'Invalid argument: Specified disk write interval cannot be less than ' +
              f'{config.INITIAL_SNAPSHOT_INTERVAL} seconds')
    elif options.run_mode_interval < options.interval:
        print(f'Invalid argument: Specified run mode interval time cannot be less than the value chosen for ' +
              f'disk write interval which is {options.interval} seconds')
    else:
        if options.verbose:
            # Initialize the logging module
            log_filename = ''
            if not args[0].endswith('/'):
                log_filename = args[0] + '/' + config.LOG_FILENAME
            else:
                log_filename = args[0] + config.LOG_FILENAME

            formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s', datefmt="%Y-%m-%d %H:%M:%S")
            # Limit log file size
            file_handler = RotatingFileHandler(log_filename, encoding='utf-8', maxBytes=config.LOG_FILE_SIZE,
                                               backupCount=0)
            file_handler.setFormatter(formatter)
            logging.getLogger(config.LOGGER_NAME).setLevel(log_numeric_level)
            logging.getLogger(config.LOGGER_NAME).addHandler(file_handler)

            utils.set_log_filename(log_filename)
        else:
            logging.getLogger(config.LOGGER_NAME).disabled = True

        utils.store_command_line_options(options)

        # Play the application started chime
        utils.play_sound_async('./resources/application_started.mp3')

        plugin_manager = PluginManager(options, args)
        ConsoleManager(options, args, plugin_manager)
