from typing import Type, Tuple, List, Dict
import argparse
import pathlib
import yaml

from .eaton import Eaton

def list_outlet_status(eaton):

    overview = eaton.get_overview()

    outlets = overview["data"][0]

    for outlet in outlets:
        name = outlet[0]

        state = "ON"
        if outlet[1] == 0:
            state = "OFF"
        print(f"{name}: {state}")

def show_current_power(eaton):

    overview = eaton.get_overview()

    power_info = overview["data"][4][0]
    active_power = power_info[8][2]

    print(f"{active_power[0]}: {active_power[1]}")


def list_devices(eaton: Type[Eaton]):
    devs = eaton.get_devices()

    for dev in devs:
        dev_name = dev[0][1]
        outlets_indices = [x[0] for x in dev[1]]

        outlet_names = [eaton.get_outlet_by_index(x) for x in outlets_indices]
        outlet_names = [x[0] for x in outlet_names]
        outlet_names_str = [f"\t{x}" for x in outlet_names]
        outlet_names_str = "\n".join(outlet_names_str)

        print(f"{dev_name} connected to:\n{outlet_names_str}")

def control_device(eaton: Type[Eaton], device : str, action: str, delay=0):

    devs = eaton.get_devices()
    dev = []
    for x in devs:
        dev_name = x[0][1]

        if dev_name == device:
            dev = x
            break

    if dev == []:
        print(f"Couldn't find device {device}")
        exit(-1)

    outlets_indices = [x[0] for x in dev[1]]
    outlet_names = [eaton.get_outlet_by_index(x) for x in outlets_indices]
    outlet_names = [x[0] for x in outlet_names]

    print(f"Turning {action} {device} via {outlet_names} with delay {delay}")

    eaton.control_outlets(outlet_names, action=action.upper(), delay=delay)


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("--config", "-c", required=False,
        help="Configuration file")
    
    parser.add_argument("--host", "-H", required=False,
        help="Host, example: 'http://pdu.local'")
    parser.add_argument("--user", "-u", required=False,
        help="Username")
    parser.add_argument("--passwd", "-p", required=False,
        help="Password")

    subparsers = parser.add_subparsers(dest="action", required=True)
    subparsers.add_parser("overview")
    parser_list = subparsers.add_parser("list")
    parser_list.add_argument("target", choices=["outlets", "devices"])

    parser_show = subparsers.add_parser("show")
    parser_show.add_argument("target", choices=["power"])

    parser_device = subparsers.add_parser("device")
    parser_device.add_argument("device_name", help="Device to act on")
    parser_device.add_argument("dev_action", choices=["on", "off"])
    parser_device.add_argument("delay", type=int, default=0, nargs='?',
        help="Delay for the action, in minutes")
    parser_device.add_argument("--yes-i-am-sure", required=True, action="store_true")


    parser_outlet = subparsers.add_parser("outlet")
    parser_outlet.add_argument("outlet_name", help="Device to act on")
    parser_outlet.add_argument("outlet_action", choices=["on", "off"])
    parser_outlet.add_argument("delay", type=int, default=0, nargs='?',
        help="Delay for the action, in minutes")
    parser_outlet.add_argument("--yes-i-am-sure", required=True, action="store_true")



    args = parser.parse_args()

    config = {}
    if args.config:
        configpath = pathlib.Path(args.config)
        with open(configpath) as f:
            configloaded = yaml.safe_load(f)
            config.update(configloaded)
    
    if args.passwd:
        config["passwd"] = args.passwd
    if args.user:
        config["user"] = args.user
    if args.host:
        config["host"] = args.host

    eaton = Eaton(
        host = config["host"],
        user=config["user"],
        passwd=config["passwd"]
    )

    # print(args)

    # Via with, to make sure sessions are always ended
    with eaton:
        if args.action == "overview":
            overview = eaton.get_overview()
            print(overview)

        if args.action == "list" and args.target == "outlets":
            list_outlet_status(eaton)
        if args.action == "list" and args.target == "devices":
            list_devices(eaton)

        if args.action == "show" and args.target == "power":
            show_current_power(eaton)

        if args.action == "outlet":
            eaton.control_outlets(
                outlets=[args.outlet_name],
                action=args.outlet_action.upper(),
                delay=args.delay)
        
        if args.action == "device":
            control_device(
                eaton=eaton,
                device=args.device_name,
                action=args.dev_action,
                delay=args.delay
            )



