import os
from os import path

import click

from tomotools.utils import sta_util
from tomotools.utils.tiltseries import (
    convert_input_to_TiltSeries,
    run_ctfplotter,
)


@click.command()
@click.argument('input_files', nargs=-1)
def fit_ctf(input_files):
    """Performs interactive CTF-Fitting.

    Takes tiltseries or folders containing them as input.
    Runs imod ctfplotter interactively.
    Defaults to overwriting previous results. Saves results to folder.

    """
    tiltseries = convert_input_to_TiltSeries(input_files)

    for ts in tiltseries:
        run_ctfplotter(ts, True)


@click.command()
@click.option('-b', '--batch-input', is_flag=True, default=False, show_default=True,
              help="Read input files as text, each line is a tiltseries (folder)")
@click.option('-n', '--name', default='warp', show_default=True,
              help="Warp working directory will be created as project_dir/name.")
@click.argument('input_files', nargs=-1)
@click.argument('project_dir', nargs=1)
def imod2warp(batch_input, name, input_files, project_dir):
    """Prepares Warp/M project.

    Takes as input several tiltseries (folders) or a file listing them (with -b),
    obtained after processing with tomotools batch-prepare-tiltseries
    and reconstructed in subdirectories using imod.

    Provide the root folder for the averaging project and a name for this export.
    This will be the Warp working directory. Both will be created if non-existent.

    Suggested structure is something like this:

    project_dir/
        ./warpdir1/
        ./warpdir2/
        ./warpdir3/
        ./relion/
        ./m/

    """
    out_dir = path.join(project_dir, name)

    if not path.isdir(project_dir):
        os.mkdir(project_dir)

    if path.isdir(out_dir):
        input(f'Exporting to existing directory {out_dir}. Continue?')

    else:
        os.mkdir(out_dir)
        os.mkdir(path.join(out_dir, 'imod'))
        os.mkdir(path.join(out_dir, 'mdoc'))
        print(f"Created Warp folder at {out_dir}.")

    # Parse input files
    ts_list = sta_util.batch_parser(input_files, batch_input)

    print(f'Found {len(ts_list)} TiltSeries to work on. \n')

    for ts in ts_list:
        print(f"Now working on {ts.path.name}")

        sta_util.make_warp_dir(ts, out_dir, imod = True)

        print(f"Warp files prepared for {ts.path.name}. \n")


@click.command()
@click.option('-b', '--batch-input', is_flag=True, default=False, show_default=True,
              help="Read input files as text, each line is a tiltseries (folder)")
@click.option('-n', '--name', default='warp', show_default=True,
              help="Warp working directory will be created as project_dir/name.")
@click.argument('input_files', nargs=-1)
@click.argument('project_dir', nargs=1)
def aretomo2warp(batch_input, name, input_files, project_dir):
    """Prepares Warp/M project.

    Takes as input several tiltseries (folders) or a file listing them (with -b),
    obtained after processing with tomotools batch-prepare-tiltseries
    and reconstructed in subdirectories using AreTomo.

    Provide the root folder for the averaging project and a name for this export.
    This will be the Warp working directory. Both will be created if non-existent.

    Suggested structure is something like this:

    project_dir/
        ./warpdir1/
        ./warpdir2/
        ./warpdir3/
        ./relion/
        ./m/

    """
    out_dir = path.join(project_dir, name)

    if not path.isdir(project_dir):
        os.mkdir(project_dir)

    if path.isdir(out_dir):
        input(f'Exporting to existing directory {out_dir}. Continue?')

    else:
        os.mkdir(out_dir)
        os.mkdir(path.join(out_dir, 'imod'))
        os.mkdir(path.join(out_dir, 'mdoc'))
        print(f"Created Warp folder at {out_dir}.")

    ts_list = sta_util.batch_parser(input_files, batch_input)

    print(f'Found {len(ts_list)} TiltSeries to work on. \n')

    for ts in ts_list:
        print(f"Now working on {ts.path.name}")

        ts_out_imod = sta_util.aretomo_export(ts)

        print(f'Performed AreTomo export of {ts.path.stem}.')

        sta_util.make_warp_dir(ts_out_imod, out_dir)

        print(f"Warp files prepared for {ts.path.name}. \n")

