from pybuilder.core import init, use_plugin, task
from os import system

use_plugin("python.core")
use_plugin("python.unittest")
use_plugin("python.coverage")
use_plugin("python.install_dependencies")
use_plugin("python.distutils")
use_plugin("python.pycharm")
use_plugin("python.sphinx")

default_task = "publish"

@task("docs", description="Generate documentation")
def generate_docs(project, logger):
    logger.info('Remove _build folder and rst-files in docs, then generate new rst files and execute the pybuilder task: sphinx_generate_documentation')
    system('rm -r docs/_build')
    system('rm docs/kdd*.rst; rm docs/modules.rst')
    system('sphinx-apidoc src/main/python -o docs')
    system('pyb sphinx_generate_documentation')

@init
def initialize(project):
    project.build_depends_on('mockito')
    project.build_depends_on('numpy')
    project.build_depends_on('matplotlib')
    project.build_depends_on('pandas')

    project.set_property("sphinx_config_path", "docs/")
    project.set_property("sphinx_source_dir", "docs/")
    project.set_property("sphinx_output_dir", "docs/_build")

    project.version = "0.1"
