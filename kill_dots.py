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


@main.command()
@click.argument('dir_with_tif_files', type=click.Path(exists=True))
@click.argument('mdoc_file', type=click.Path(exists=True))
def examine(dir_with_tif_files, mdoc_file):
    folder = pathlib.Path(dir_with_tif_files)
    print(f'folder={folder}')

    tifs = set(folder.glob('*.tif'))

    print(f'{len(tifs)} tif files in {folder}')

    mdoc = pathlib.Path(mdoc_file)

    with open(mdoc, 'r') as input_file:
        mdoc_lines = list(input_file)

    interesting_tifs = []

    for line in mdoc_lines:
        if line.startswith('SubFramePath'):
            tif_file = line.split('=')[1].strip()
            tif_path = pathlib.Path(tif_file)
            if folder / tif_path.name not in tifs:
                print(f'The following file, {tif_path.name}, is not found in the directory yet is mentioned in the mdoc')
            interesting_tifs.append(tif_path.name)

    print(f'The mdoc file refers to {len(interesting_tifs)} tif files')


@main.command()
@click.argument('dir_with_tif_files', type=click.Path(exists=True))
@click.argument('mdoc_file', type=click.Path(exists=True))
@click.argument('target_dir', type=click.Path())
def apply(dir_with_tif_files, mdoc_file, target_dir):
    folder = pathlib.Path(dir_with_tif_files)
    print(f'folder={folder}')

    tifs = set(folder.glob('*.tif'))

    print(f'{len(tifs)} tif files in {folder}')

    mdoc = pathlib.Path(mdoc_file) # folder / 'NA_001.st.mdoc'

    target_folder = pathlib.Path(target_dir)

    with open(mdoc, 'r') as input_file:
        mdoc_lines = list(input_file)

    target_folder.mkdir(exist_ok=True)

    mdoc_lines_renamed = []
    interesting_tifs = []

    for line in mdoc_lines:
        if line.startswith('SubFramePath'):
            tif_file = line.split('=')[1].strip()
            tif_path = pathlib.Path(tif_file)
            if folder / tif_path.name not in tifs:
                print(f'The following file, {tif_path.name}, is not found in the directory yet is mentioned in the mdoc')
            interesting_tifs.append(tif_path.name)
            new_name = rename_file(tif_path.name, target_folder)
            mdoc_lines_renamed.append(f'SubFramePath = {new_name}\n')
        else:
            mdoc_lines_renamed.append(line)  # as is

    print(f'The mdoc file refers to {len(interesting_tifs)} tif files')

    assert len(mdoc_lines) == len(mdoc_lines_renamed)

    with open(target_folder / mdoc.name, 'w') as output_file:
        output_file.write(''.join(mdoc_lines_renamed))

    for tif in interesting_tifs:
        pathlib.Path(rename_file(tif, target_folder)).symlink_to(folder / tif)   
        # shutil.copy(folder / tif, rename_file(tif, target_folder))

    print(f"Please verify, for example with 'ls {target_folder}'")


if __name__ == '__main__':
    main()
