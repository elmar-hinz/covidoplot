from configuration import get as c
import os
import shutil

def copy(source, destination):
    src_files = os.listdir(source)
    for file_name in src_files:
        full_file_name = os.path.join(source, file_name)
        if os.path.isfile(full_file_name):
            shutil.copy(full_file_name, destination)

def export_plots():
    source = c('directories.export.plots')
    destination = c('directories.published.plots')
    copy(source, destination)

def export_data():
    source = c('directories.export.data')
    destination = c('directories.published.data')
    copy(source, destination)

def do():
    export_plots()
    export_data()
