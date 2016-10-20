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

root_package = "kdd"
sphinx_builder = "epub"
sphinx_docs_dir = "docs/"
sphinx_source_dir = "docs/source/"
sphinx_output_dir = "docs/build/"

@task("docs", description="Generate documentation")
def generate_html_docs(project, logger):
    logger.info('Generates api-documentation of package in src/main/python into docs/build/' + sphinx_builder)
    system('rm -r ' + sphinx_output_dir)
    system('rm ' + sphinx_source_dir + root_package + '*.rst; rm ' + sphinx_source_dir + 'modules.rst')
    system('sphinx-apidoc src/main/python -o ' + sphinx_source_dir)
    system('cd ' + sphinx_docs_dir + '; make doctest; make ' + sphinx_builder)

@task("doctest", description="Execute doctests")
def execute_doctests(project, logger):
    logger.info('Executes doctests of project')
    system('cd ' + sphinx_docs_dir + '; make doctest;')
    
@init
def initialize(project):
    project.build_depends_on('mockito')
    project.build_depends_on('numpy')
    project.build_depends_on('matplotlib')
    project.build_depends_on('pandas')
    project.build_depends_on('sphinx')
    project.build_depends_on('cython', '==0.23')
    project.build_depends_on('kivy')
    
    project.version = "0.1"
