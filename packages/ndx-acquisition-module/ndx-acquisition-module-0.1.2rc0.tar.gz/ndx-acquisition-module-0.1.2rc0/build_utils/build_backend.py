import os
from setuptools import build_meta as _orig
from shutil import copy2


prepare_metadata_for_build_wheel = _orig.prepare_metadata_for_build_wheel
build_wheel = _orig.build_wheel
build_sdist = _orig.build_sdist
get_requires_for_build_sdist = _orig.get_requires_for_build_sdist


def _copy_spec_files(project_dir):
    ns_path = os.path.join(project_dir, 'spec', 'ndx-acquisition-module.namespace.yaml')
    ext_path = os.path.join(project_dir, 'spec', 'ndx-acquisition-module.extensions.yaml')

    dst_dir = os.path.join(project_dir, 'src', 'pynwb', 'ndx_acquisition_module', 'spec')

    if not os.path.exists(dst_dir):
        os.mkdir(dst_dir)

    copy2(ns_path, dst_dir)
    copy2(ext_path, dst_dir)


def get_requires_for_build_wheel(config_settings=None):
    # hijacking this function to copy necessary spec files
    _copy_spec_files(os.path.join(os.path.dirname(__file__), '..'))
    return _orig.get_requires_for_build_wheel(config_settings)
