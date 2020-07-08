#!/usr/bin/env python
# coding: utf-8

import pathlib
import shutil
import click


@click.group()
def main():
    pass


def rename_file(name: str, target_folder: pathlib.Path) -> str:
    return str(target_folder / name.replace('.', '_').replace('_tif', '.tif'))


PATTERN_OF_TIF_FILE = "*.tif"
PATTERN_OF_MDOC_FILE = "*.mdoc"
RESULTS_FOLDER_NAME = "4motcor"


@main.command()
@click.argument('dir_with_tif_files', type=click.Path(exists=True))
def examine(dir_with_tif_files):
    folder = pathlib.Path(dir_with_tif_files)
    print(f'tifs folder={folder}')

    tifs = set(folder.glob(PATTERN_OF_TIF_FILE))

    print(f'{len(tifs)} tif files in {folder}')

    parent_folder = folder.resolve().parent

    for mdoc in parent_folder.glob(PATTERN_OF_MDOC_FILE):

        print()
        print(mdoc)

        with open(mdoc, 'r') as input_file:
            mdoc_lines = list(input_file)

        interesting_tifs = []

        for line in mdoc_lines:
            if line.startswith('SubFramePath'):
                tif_file = line.split('=')[1].strip()
                # tif_path = pathlib.Path(tif_file)
                tif_path = pathlib.PureWindowsPath(tif_file)  # it was written with DOS conventions
                if folder / tif_path.name not in tifs:
                    print(f'The following file, {tif_path.name}, is not found in the directory yet is mentioned in the mdoc')
                interesting_tifs.append(tif_path.name)

        print(f'The mdoc file {mdoc} refers to {len(interesting_tifs)} tif files')


@main.command()
@click.argument('dir_with_tif_files', type=click.Path(exists=True))
def apply(dir_with_tif_files):
    folder = pathlib.Path(dir_with_tif_files)
    print(f'tifs folder={folder}')

    tifs = set(folder.glob(PATTERN_OF_TIF_FILE))

    print(f'{len(tifs)} tif files in {folder}')

    parent_folder = folder.resolve().parent  # where to find 'mdoc' files

    target_folder = folder / RESULTS_FOLDER_NAME  # name for the folder with the outputs

    target_folder.mkdir(exist_ok=True)

    for mdoc in parent_folder.glob(PATTERN_OF_MDOC_FILE):

        print()
        print(mdoc)

        with open(mdoc, 'r') as input_file:
            mdoc_lines = list(input_file)

        mdoc_lines_renamed = []
        interesting_tifs = []

        for line in mdoc_lines:
            if line.startswith('SubFramePath'):
                tif_file = line.split('=')[1].strip()
                # tif_path = pathlib.Path(tif_file)
                tif_path = pathlib.PureWindowsPath(tif_file)  # it was written with DOS conventions
                if folder / tif_path.name not in tifs:
                    print(f'The following file, {tif_path.name}, is not found in the directory yet is mentioned in the mdoc')
                interesting_tifs.append(tif_path.name)
                new_name = pathlib.Path(rename_file(tif_path.name, target_folder)).name
                mdoc_lines_renamed.append(f'SubFramePath = {new_name}\n')
            else:
                mdoc_lines_renamed.append(line)  # as is

        print(f'The mdoc file {mdoc} refers to {len(interesting_tifs)} tif files')

        assert len(mdoc_lines) == len(mdoc_lines_renamed)

        with open(target_folder / mdoc.name, 'w') as output_file:
            output_file.write(''.join(mdoc_lines_renamed))

        for tif in interesting_tifs:
            pathlib.Path(rename_file(tif, target_folder)).symlink_to((folder / tif).absolute())   
            # shutil.copy(folder / tif, rename_file(tif, target_folder))

    print(f"Please verify, for example with 'ls {target_folder}'")


if __name__ == '__main__':
    main()
