import argparse
import json

import pandas as pd

from .pulseeco import PulseEco

help_strings = {
    'sensor': 'the unique ID of the sensor',
    'period': 'the period of the data (day, week, month)',
    'type': 'the type ID of the sensor',
    'from_': 'the start datetime of the data',
    'to': 'the end datetime of the data'
}


def add_print_type_arg_json(parser: argparse._ActionsContainer) -> None:
    parser.add_argument('-J', '--json', action='store_true',
                        help='print data as JSON')


def add_print_type_arg_table(parser: argparse._ActionsContainer) -> None:
    parser.add_argument(
        '-T', '--table', action='store_true',
        help='print data as a table')


def add_print_type_args(parser: argparse.ArgumentParser) -> None:
    exclusive_group = parser.add_mutually_exclusive_group(required=False)
    add_print_type_arg_json(exclusive_group)
    add_print_type_arg_table(exclusive_group)


def add_sensors_subparser(subparsers: argparse._SubParsersAction) -> None:
    parser_sensors = subparsers.add_parser('sensors', help='List sensors')
    parser_sensors.set_defaults(func=sensors)
    add_print_type_args(parser_sensors)


def add_sensor_subparser(subparsers: argparse._SubParsersAction) -> None:
    parser_sensor = subparsers.add_parser('sensor',
                                          help='Get sensor info by ID')
    parser_sensor.set_defaults(func=sensor)
    parser_sensor.add_argument('-s', '--sensor',
                               help=help_strings['sensor'], type=str,
                               required=True)
    add_print_type_arg_json(parser_sensor)


def add_common_args(parser: argparse.ArgumentParser,
                    required_type: bool = False) -> None:
    parser.add_argument('-s', '--sensor', help=help_strings['sensor'],
                        type=str, default='-1')
    parser.add_argument('-t', '--type', help=help_strings['type'], type=str,
                        required=required_type)
    parser.add_argument('-f', '--from', help=help_strings['from_'], type=str)
    parser.add_argument('--to', help=help_strings['to'], type=str)


def add_data_raw_subparser(subparsers: argparse._SubParsersAction) -> None:
    parser_data_raw = subparsers.add_parser('dataRaw',
                                            help='Get raw data')

    parser_data_raw.set_defaults(func=data_raw)
    add_common_args(parser_data_raw)
    add_print_type_args(parser_data_raw)


def add_avg_data_subparser(subparsers: argparse._SubParsersAction) -> None:
    parser_avg_data = subparsers.add_parser('avgData',
                                            help='Get average data')

    parser_avg_data.set_defaults(func=avg_data)
    parser_avg_data.add_argument('-p', '--period', help=help_strings['period'],
                                 type=str)
    add_common_args(parser_avg_data, required_type=True)
    add_print_type_args(parser_avg_data)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description='PulseEco API client',
        prog='pulseeco')
    parser.add_argument(
        '-B', '--base-url', help='PulseEco API base URL', type=str,
        default='https://{city_name}.pulse.eco/rest/{end_point}')
    parser.add_argument('-U', '--user', help='PulseEco API user', type=str,
                        required=True)
    parser.add_argument('-P', '--password', help='PulseEco API password',
                        type=str, required=True)
    parser.add_argument('-C', '--city', help='the city name', type=str,
                        required=True)

    subparsers = parser.add_subparsers(required=True, dest='command')

    add_sensors_subparser(subparsers)
    add_sensor_subparser(subparsers)
    add_data_raw_subparser(subparsers)
    add_avg_data_subparser(subparsers)
    parser_data24h = subparsers.add_parser('data24h', help='Get 24h data')
    parser_data24h.set_defaults(func=data24h)
    add_print_type_args(parser_data24h)
    parser_current = subparsers.add_parser('current', help='Get current data')
    parser_current.set_defaults(func=current)
    add_print_type_args(parser_current)
    parser_overall = subparsers.add_parser('overall', help='Get overall data')
    parser_overall.set_defaults(func=overall)
    add_print_type_arg_json(parser_overall)

    return parser.parse_args()


def get_session(args: argparse.Namespace) -> PulseEco:
    return PulseEco(auth=(args.user, args.password),
                    base_url=args.base_url)


def print_data(data: list, args: argparse.Namespace) -> None:
    if args.json:
        print(json.dumps(data, indent=2))
    elif len(data) > 0 and args.table:
        print(pd.DataFrame(data))
    else:
        print(data)


def sensors(args: argparse.Namespace) -> None:
    pulse_eco = get_session(args)
    sensors = pulse_eco.sensors(args.city)
    print_data(sensors, args)


def sensor(args: argparse.Namespace) -> None:
    pulse_eco = get_session(args)
    sensor = pulse_eco.sensor(args.city, args.sensor)
    if args.json:
        print(json.dumps(sensor, indent=2))
    else:
        print(sensor)


def data_raw(args: argparse.Namespace) -> None:
    pulse_eco = get_session(args)
    data = pulse_eco.data_raw(
        args.city,
        sensor_id=args.sensor,
        type=args.type,
        from_=vars(args)['from'],
        to=args.to
    )
    print_data(data, args)


def avg_data(args: argparse.Namespace) -> None:
    pulse_eco = get_session(args)
    data = pulse_eco.avg_data(
        args.city,
        period=args.period,
        sensor_id=args.sensor,
        type=args.type,
        from_=vars(args)['from'],
        to=args.to
    )
    print_data(data, args)


def data24h(args: argparse.Namespace) -> None:
    pulse_eco = get_session(args)
    data = pulse_eco.data24h(args.city)
    print_data(data, args)


def current(args: argparse.Namespace) -> None:
    pulse_eco = get_session(args)
    data = pulse_eco.current(args.city)
    print_data(data, args)


def overall(args: argparse.Namespace) -> None:
    pulse_eco = get_session(args)
    data = pulse_eco.overall(args.city)
    if args.json:
        print(json.dumps(data, indent=2))
    else:
        print(data)


def main():
    args = parse_args()
    try:
        args.func(args)
    except Exception as e:
        print(e)


if __name__ == '__main__':
    main()
