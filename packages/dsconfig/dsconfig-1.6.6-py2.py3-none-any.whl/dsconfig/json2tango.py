"""
Reads a JSON file in the right format, compares it with the current
state of the Tango DB, and generates the set of DB API commands needed
to get to the state described by the file. These commands can also
optionally be run.
"""
from __future__ import absolute_import
from __future__ import print_function

import json
import sys
import time
from optparse import OptionParser
from tempfile import NamedTemporaryFile

import tango
from dsconfig.appending_dict.caseless import CaselessDictionary
from dsconfig.configure import configure
from dsconfig.dump import get_db_data
from dsconfig.filtering import filter_config
from dsconfig.formatting import (CLASSES_LEVELS, SERVERS_LEVELS, load_json,
                                 normalize_config, validate_json,
                                 clean_metadata)
from dsconfig.output import show_actions
from dsconfig.tangodb import summarise_calls, get_devices_from_dict
from dsconfig.utils import SUCCESS, ERROR, CONFIG_APPLIED, CONFIG_NOT_APPLIED
from dsconfig.utils import green, red, yellow, progressbar, no_colors


def prepare_config(config, validate=False, include=False, exclude=False,
                   include_classes=False, exclude_classes=False):
    """
    Do various cleaning and validation, as well as filtering on the config.
    """

    # Normalization - making the config conform to standard
    config = normalize_config(config)

    # remove any metadata at the top level (should we use this for something?)
    config = clean_metadata(config)

    # Optional validation of the JSON file format.
    if validate:
        validate_json(config)

    # filtering
    try:
        if include:
            config["servers"] = filter_config(
                config.get("servers", {}), include, SERVERS_LEVELS)
        if exclude:
            config["servers"] = filter_config(
                config.get("servers", {}), exclude, SERVERS_LEVELS, invert=True)
        if include_classes:
            config["classes"] = filter_config(
                config.get("classes", {}), include_classes, CLASSES_LEVELS)
        if exclude_classes:
            config["classes"] = filter_config(
                config.get("classes", {}), exclude_classes, CLASSES_LEVELS,
                invert=True)
    except ValueError as e:
        print(red("Filter error:\n%s" % e), file=sys.stderr)
        raise RuntimeError(ERROR)

    return config


def apply_config(config, db, write=False, update=False, dbdata=None,
                 nostrictcheck=False, case_sensitive=False, sleep=0, verbose=False):
    """
    Takes a config dict, assumed to be valid.

    Find out the operations needed to get from the current DB state
    to one described by the config. Optionally apply them to the DB
    (by using the --write flag).
    """

    if not any(k in config for k in ("devices", "servers", "classes")):
        raise RuntimeError(ERROR)

    # check if there is anything in the DB that will be changed or removed
    if dbdata:
        with open(dbdata) as f:
            original = json.loads(f.read())
        collisions = {}
    else:
        original = get_db_data(db, dservers=True, class_properties=True)
        if "servers" in config:
            devices = CaselessDictionary({
                dev: (srv, inst, cls)
                for srv, inst, cls, dev
                in get_devices_from_dict(config["servers"])
            })
        else:
            devices = CaselessDictionary({})
        orig_devices = CaselessDictionary({
            dev: (srv, inst, cls)
            for srv, inst, cls, dev
            in get_devices_from_dict(original["servers"])
        })
        collisions = {}
        for dev, (srv, inst, cls) in list(devices.items()):
            for odev, (osrv, oinst, ocls) in orig_devices.items():
                if odev.lower() == dev.lower():
                    server = "{}/{}".format(srv, inst)
                    osrv, oinst, ocls = orig_devices[dev]
                    origserver = "{}/{}".format(osrv, oinst)
                    if server.lower() != origserver.lower():
                        collisions.setdefault(origserver, []).append((ocls, dev))

    # get the list of DB calls needed
    dbcalls = configure(config, original,
                        update=update,
                        ignore_case=not case_sensitive,
                        strict_attr_props=not nostrictcheck)

    # perform the db operations (if we're supposed to)
    if write and dbcalls:
        for i, (method, args, kwargs) in enumerate(dbcalls):
            if sleep:
                time.sleep(sleep)
            if verbose:
                progressbar(i, len(dbcalls), 20)
            print(method)
            getattr(db, method)(*args, **kwargs)
        print()

    return config, original, dbcalls, collisions


def show_output(config, original, dbcalls, collisions, db,
                show_colors=True, show_input=False, show_output=False,
                show_dbcalls=False, verbose=False, write=False):
    """
    Takes output from the apply_config function and presents it in human
    readable ways.
    """

    if not show_colors:
        no_colors()

    if show_input:
        print(json.dumps(config, indent=4))
        return

    # Print out a nice diff
    if verbose:
        show_actions(original, dbcalls)

    # optionally dump some information to stdout
    if show_output:
        print(json.dumps(original, indent=4))
    if show_dbcalls:
        print("Tango database calls:", file=sys.stderr)
        for method, args, kwargs in dbcalls:
            print(method, args, file=sys.stderr)

    # Check for moved devices and remove empty servers
    empty = set()
    for srvname, devs in list(collisions.items()):
        if verbose:
            srv, inst = srvname.split("/")
            for cls, dev in devs:
                print(red("MOVED (because of collision):"), dev, file=sys.stderr)
                print("    Server: ", "{}/{}".format(srv, inst), file=sys.stderr)
                print("    Class: ", cls, file=sys.stderr)
        if len(db.get_device_class_list(srvname)) == 2:  # just dserver
            empty.add(srvname)
            if write:
                db.delete_server(srvname)

    # finally print out a brief summary of what was done
    if dbcalls:
        print()
        print("Summary:", file=sys.stderr)
        print("\n".join(summarise_calls(dbcalls, original)), file=sys.stderr)
        if collisions:
            servers = len(collisions)
            devices = sum(len(devs) for devs in list(collisions.values()))
            print(red("Move %d devices from %d servers." %
                      (devices, servers)), file=sys.stderr)
        if empty and verbose:
            print(red("Removed %d empty servers." % len(empty)), file=sys.stderr)

        if write:
            print(red("\n*** Data was written to the Tango DB ***"), file=sys.stderr)
            with NamedTemporaryFile(prefix="dsconfig-", suffix=".json",
                                    delete=False) as f:
                f.write(json.dumps(original, indent=4).encode())
                print(("The previous DB data was saved to %s" %
                       f.name), file=sys.stderr)
            return CONFIG_APPLIED
        else:
            print(yellow(
                "\n*** Nothing was written to the Tango DB (use -w) ***"), file=sys.stderr)
            return CONFIG_NOT_APPLIED

    else:
        print(green("\n*** No changes needed in Tango DB ***"), file=sys.stderr)
        return SUCCESS


def json_to_tango(options, args):
    """
    Note:
    This used to be one big function that contained all the code above. It was bad as an
    entry point for library code, since it included output and everything. It is now
    instead recommended to use the more specific functions, as needed.
    """
    db = tango.Database()

    if len(args) == 0:
        config = load_json(sys.stdin)
    else:
        json_file = args[0]
        with open(json_file) as f:
            config = load_json(f)

    try:
        config = prepare_config(config)
        results = apply_config(config, db, write=options.write, update=options.update,
                               dbdata=options.dbdata, nostrictcheck=options.nostrictcheck,
                               case_sensitive=options.case_sensitive, sleep=options.sleep,
                               verbose=options.verbose)
    except RuntimeError as e:
        sys.exit(e.args[0])

    retval = show_output(*results, db=db, show_colors=not options.no_colors,
                         show_input=options.input,
                         show_output=options.output, show_dbcalls=options.dbcalls,
                         verbose=options.verbose, write=options.write)
    sys.exit(retval)


def main():

    usage = "Usage: %prog [options] JSONFILE"
    parser = OptionParser(usage=usage)

    parser.add_option("-w", "--write", dest="write", action="store_true",
                      help="write to the Tango DB", metavar="WRITE")
    parser.add_option("-u", "--update", dest="update", action="store_true",
                      help="don't remove things, only add/update",
                      metavar="UPDATE")
    parser.add_option("-c", "--case-sensitive", dest="case_sensitive",
                      action="store_true",
                      help=("Don't ignore the case of server, device, "
                            "attribute and property names"),
                      metavar="CASESENSITIVE")
    parser.add_option("-q", "--quiet",
                      action="store_false", dest="verbose", default=True,
                      help="don't print actions to stderr")
    parser.add_option("-o", "--output", dest="output", action="store_true",
                      help="Output the relevant DB state as JSON.")
    parser.add_option("-p", "--input", dest="input", action="store_true",
                      help="Output the input JSON (after filtering).")
    parser.add_option("-d", "--dbcalls", dest="dbcalls", action="store_true",
                      help="print out all db calls.")
    parser.add_option("-v", "--no-validation", dest="validate", default=True,
                      action="store_false", help=("Skip JSON validation"))
    parser.add_option("-s", "--sleep", dest="sleep", default=0.01,
                      type="float",
                      help=("Number of seconds to sleep between DB calls"))
    parser.add_option("-n", "--no-colors",
                      action="store_true", dest="no_colors", default=False,
                      help="Don't print colored output")
    parser.add_option("-i", "--include", dest="include", action="append",
                      help=("Inclusive filter on server configutation"))
    parser.add_option("-x", "--exclude", dest="exclude", action="append",
                      help=("Exclusive filter on server configutation"))
    parser.add_option("-a", "--no-strict-check", dest="nostrictcheck",
                      default=False, action="store_true",
                      help="Disable strick attribute property checking")
    parser.add_option("-I", "--include-classes", dest="include_classes",
                      action="append",
                      help=("Inclusive filter on class configuration"))
    parser.add_option("-X", "--exclude-classes", dest="exclude_classes",
                      action="append",
                      help=("Exclusive filter on class configuration"))

    parser.add_option(
        "-D", "--dbdata",
        help="Read the given file as DB data instead of using the actual DB",
        dest="dbdata")

    options, args = parser.parse_args()

    json_to_tango(options, args)


if __name__ == "__main__":
    main()
