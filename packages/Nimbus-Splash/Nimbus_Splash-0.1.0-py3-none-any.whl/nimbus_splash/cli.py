import argparse
from . import job


def gen_job_func(uargs):
    """
    Wrapper for CLI gen_job call

    Parameters
    ----------
    uargs : argparser object
        User arguments

    Returns
    -------
    None

    """

    # Decide node type based on number of cores

    core_to_node = {
        1: 'spot-fsv2-1',
        2: 'spot-fsv2-2',
        4: 'spot-fsv2-4',
        16: 'spot-fsv2-16',
        24: 'spot-fsv2-24',
        32: 'spot-fsv2-32',
        36: 'spot-fsv2-36',
    }

    if uargs.node_type:
        node = uargs.node_type
    else:
        node = core_to_node[uargs.n_cores]

    # Write job file
    job.write_file(uargs.input_file, node)

    return


def read_args(arg_list=None):
    """
    Reader for command line arguments. Uses subReaders for individual programs

    Parameters
    ----------
        args : argparser object
            command line arguments

    Returns
    -------
        None

    """

    description = """
    A package for working with Orca on Bath's Cloud HPC service
    """

    epilog = """
    To display options for a specific program, use splash \
    PROGRAMFILETYPE -h
    """
    parser = argparse.ArgumentParser(
        description=description,
        epilog=epilog,
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    subparsers = parser.add_subparsers(dest="prog")

    gen_job = subparsers.add_parser(
        "gen_job",
        description="Generate Nimbus SLURM submission script"
    )
    gen_job.set_defaults(func=gen_job_func)

    gen_job.add_argument(
        "input_file",
        type=str,
        help="Orca input file name"
    )

    node_spec = gen_job.add_mutually_exclusive_group()
    node_spec.add_argument(
        "-n",
        "--n_cores",
        type=str,
        default=16,
        help="Number of cores to use for fsv2 node, default is 16"
    )
    node_spec.add_argument(
        "-nt",
        "--node_type",
        type=str,
        help="Node to run on, default is fsv2 with 16"
    )

    # If arg_list==None, i.e. normal cli usage, parse_args() reads from
    # "sys.argv". The arg_list can be used to call the argparser from the
    # back end.

    # read sub-parser
    parser.set_defaults(func=lambda args: parser.print_help())
    args = parser.parse_args(arg_list)
    args.func(args)

    return args


def interface():
    read_args()
    return
