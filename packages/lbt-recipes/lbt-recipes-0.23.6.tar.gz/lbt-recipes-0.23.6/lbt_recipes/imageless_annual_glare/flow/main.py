"""
This file is auto-generated from a Queenbee recipe. It is unlikely that
you should be editing this file directly. Instead try to edit the recipe
itself and regenerate the code.

Contact the recipe maintainers with additional questions.
    mostapha: mostapha@ladybug.tools
    ladybug-tools: info@ladybug.tools

This file is licensed under "PolyForm Shield License 1.0.0".
See https://polyformproject.org/wp-content/uploads/2020/06/PolyForm-Shield-1.0.0.txt for more information.
"""


import luigi
import os
import pathlib
from queenbee_local import QueenbeeTask
from queenbee_local import load_input_param as qb_load_input_param
from .dependencies.imageless_annual_glare import _ImagelessAnnualGlare_5a4cf8eaOrchestrator as ImagelessAnnualGlare_5a4cf8eaWorkerbee


_default_inputs = {   'cpu_count': 50,
    'glare_threshold': 0.4,
    'grid_filter': '*',
    'luminance_factor': 2000.0,
    'min_sensor_count': 500,
    'model': None,
    'north': 0.0,
    'params_folder': '__params',
    'radiance_parameters': '-ab 2 -ad 5000 -lw 2e-05',
    'schedule': None,
    'simulation_folder': '.',
    'wea': None}


class AnnualImagelessGlareLoop(luigi.Task):
    """No description is provided."""

    # DAG Input parameters
    _input_params = luigi.DictParameter()

    # Task inputs
    @property
    def radiance_parameters(self):
        return self._input_params['radiance_parameters']

    @property
    def grid_name(self):
        return self.item['full_id']

    @property
    def sensor_count(self):
        return self.item['count']

    @property
    def luminance_factor(self):
        return self._input_params['luminance_factor']

    @property
    def octree_file(self):
        value = pathlib.Path(self.input()['CreateOctree']['scene_file'].path)
        return value.as_posix() if value.is_absolute() \
            else pathlib.Path(self.initiation_folder, value).resolve().as_posix()

    @property
    def sensor_grid(self):
        value = pathlib.Path(self.input()['SplitGridFolder']['output_folder'].path, '{item_full_id}.pts'.format(item_full_id=self.item['full_id']))
        return value.as_posix() if value.is_absolute() \
            else pathlib.Path(self.initiation_folder, value).resolve().as_posix()

    @property
    def sky_matrix(self):
        value = pathlib.Path(self.input()['CreateTotalSky']['sky_matrix'].path)
        return value.as_posix() if value.is_absolute() \
            else pathlib.Path(self.initiation_folder, value).resolve().as_posix()

    @property
    def sky_dome(self):
        value = pathlib.Path(self.input()['CreateSkyDome']['sky_dome'].path)
        return value.as_posix() if value.is_absolute() \
            else pathlib.Path(self.initiation_folder, value).resolve().as_posix()

    @property
    def bsdfs(self):
        try:
            pathlib.Path(self.input()['CreateRadFolder']['bsdf_folder'].path)
        except TypeError:
            # optional artifact
            return None
        value = pathlib.Path(self.input()['CreateRadFolder']['bsdf_folder'].path)
        return value.as_posix() if value.is_absolute() \
            else pathlib.Path(self.initiation_folder, value).resolve().as_posix()

    # get item for loop
    try:
        item = luigi.DictParameter()
    except Exception:
        item = luigi.Parameter()

    @property
    def execution_folder(self):
        return pathlib.Path(self._input_params['simulation_folder'], 'initial_results/{item_full_id}'.format(item_full_id=self.item['full_id'])).resolve().as_posix()

    @property
    def initiation_folder(self):
        return pathlib.Path(self._input_params['simulation_folder']).as_posix()

    @property
    def params_folder(self):
        return pathlib.Path(self.execution_folder, self._input_params['params_folder']).resolve().as_posix()

    @property
    def map_dag_inputs(self):
        """Map task inputs to DAG inputs."""
        inputs = {
            'simulation_folder': self.execution_folder,
            'radiance_parameters': self.radiance_parameters,
            'octree_file': self.octree_file,
            'grid_name': self.grid_name,
            'sensor_grid': self.sensor_grid,
            'sensor_count': self.sensor_count,
            'sky_matrix': self.sky_matrix,
            'sky_dome': self.sky_dome,
            'bsdfs': self.bsdfs,
            'luminance_factor': self.luminance_factor
        }
        try:
            inputs['__debug__'] = self._input_params['__debug__']
        except KeyError:
            # not debug mode
            pass

        return inputs

    def run(self):
        yield [ImagelessAnnualGlare_5a4cf8eaWorkerbee(_input_params=self.map_dag_inputs)]
        done_file = pathlib.Path(self.execution_folder, 'annual_imageless_glare.done')
        done_file.parent.mkdir(parents=True, exist_ok=True)
        done_file.write_text('done!')

    def requires(self):
        return {'CreateSkyDome': CreateSkyDome(_input_params=self._input_params), 'CreateOctree': CreateOctree(_input_params=self._input_params), 'CreateTotalSky': CreateTotalSky(_input_params=self._input_params), 'CreateRadFolder': CreateRadFolder(_input_params=self._input_params), 'SplitGridFolder': SplitGridFolder(_input_params=self._input_params)}

    def output(self):
        return {
            'is_done': luigi.LocalTarget(pathlib.Path(self.execution_folder, 'annual_imageless_glare.done').resolve().as_posix())
        }


class AnnualImagelessGlare(luigi.Task):
    """No description is provided."""
    # global parameters
    _input_params = luigi.DictParameter()
    @property
    def sensor_grids(self):
        value = pathlib.Path(self.input()['SplitGridFolder']['sensor_grids'].path)
        return value.as_posix() if value.is_absolute() \
            else pathlib.Path(self.initiation_folder, value).resolve().as_posix()

    @property
    def items(self):
        try:
            # assume the input is a file
            return qb_load_input_param(self.sensor_grids)
        except:
            # it is a parameter
            return self.input()['SplitGridFolder']['sensor_grids'].path

    def run(self):
        yield [AnnualImagelessGlareLoop(item=item, _input_params=self._input_params) for item in self.items]
        done_file = pathlib.Path(self.execution_folder, 'annual_imageless_glare.done')
        done_file.parent.mkdir(parents=True, exist_ok=True)
        done_file.write_text('done!')

    @property
    def initiation_folder(self):
        return pathlib.Path(self._input_params['simulation_folder']).as_posix()

    @property
    def execution_folder(self):
        return pathlib.Path(self._input_params['simulation_folder']).as_posix()

    @property
    def params_folder(self):
        return pathlib.Path(self.execution_folder, self._input_params['params_folder']).resolve().as_posix()

    def requires(self):
        return {'CreateSkyDome': CreateSkyDome(_input_params=self._input_params), 'CreateOctree': CreateOctree(_input_params=self._input_params), 'CreateTotalSky': CreateTotalSky(_input_params=self._input_params), 'CreateRadFolder': CreateRadFolder(_input_params=self._input_params), 'SplitGridFolder': SplitGridFolder(_input_params=self._input_params)}

    def output(self):
        return {
            'is_done': luigi.LocalTarget(pathlib.Path(self.execution_folder, 'annual_imageless_glare.done').resolve().as_posix())
        }


class CopyGridInfo(QueenbeeTask):
    """Copy a file or folder to a destination."""

    # DAG Input parameters
    _input_params = luigi.DictParameter()

    # Task inputs
    @property
    def src(self):
        value = pathlib.Path(self.input()['CreateRadFolder']['sensor_grids_file'].path)
        return value.as_posix() if value.is_absolute() \
            else pathlib.Path(self.initiation_folder, value).resolve().as_posix()

    @property
    def execution_folder(self):
        return pathlib.Path(self._input_params['simulation_folder']).as_posix()

    @property
    def initiation_folder(self):
        return pathlib.Path(self._input_params['simulation_folder']).as_posix()

    @property
    def params_folder(self):
        return pathlib.Path(self.execution_folder, self._input_params['params_folder']).resolve().as_posix()

    def command(self):
        return 'echo copying input path...'

    def requires(self):
        return {'CreateRadFolder': CreateRadFolder(_input_params=self._input_params)}

    def output(self):
        return {
            'dst': luigi.LocalTarget(
                pathlib.Path(self.execution_folder, 'metrics/ga/grids_info.json').resolve().as_posix()
            )
        }

    @property
    def input_artifacts(self):
        return [
            {'name': 'src', 'to': 'input_path', 'from': self.src, 'optional': False}]

    @property
    def output_artifacts(self):
        return [
            {
                'name': 'dst', 'from': 'input_path',
                'to': pathlib.Path(self.execution_folder, 'metrics/ga/grids_info.json').resolve().as_posix(),
                'optional': False,
                'type': 'folder'
            }]


class CopyRedistInfo(QueenbeeTask):
    """Copy a file or folder to a destination."""

    # DAG Input parameters
    _input_params = luigi.DictParameter()

    # Task inputs
    @property
    def src(self):
        value = pathlib.Path(self.input()['SplitGridFolder']['dist_info'].path)
        return value.as_posix() if value.is_absolute() \
            else pathlib.Path(self.initiation_folder, value).resolve().as_posix()

    @property
    def execution_folder(self):
        return pathlib.Path(self._input_params['simulation_folder']).as_posix()

    @property
    def initiation_folder(self):
        return pathlib.Path(self._input_params['simulation_folder']).as_posix()

    @property
    def params_folder(self):
        return pathlib.Path(self.execution_folder, self._input_params['params_folder']).resolve().as_posix()

    def command(self):
        return 'echo copying input path...'

    def requires(self):
        return {'SplitGridFolder': SplitGridFolder(_input_params=self._input_params)}

    def output(self):
        return {
            'dst': luigi.LocalTarget(
                pathlib.Path(self.execution_folder, 'initial_results/dgp/_redist_info.json').resolve().as_posix()
            )
        }

    @property
    def input_artifacts(self):
        return [
            {'name': 'src', 'to': 'input_path', 'from': self.src, 'optional': False}]

    @property
    def output_artifacts(self):
        return [
            {
                'name': 'dst', 'from': 'input_path',
                'to': pathlib.Path(self.execution_folder, 'initial_results/dgp/_redist_info.json').resolve().as_posix(),
                'optional': False,
                'type': 'folder'
            }]


class CreateOctree(QueenbeeTask):
    """Generate an octree from a Radiance folder."""

    # DAG Input parameters
    _input_params = luigi.DictParameter()

    # Task inputs
    black_out = luigi.Parameter(default='default')

    include_aperture = luigi.Parameter(default='include')

    @property
    def model(self):
        value = pathlib.Path(self.input()['CreateRadFolder']['model_folder'].path)
        return value.as_posix() if value.is_absolute() \
            else pathlib.Path(self.initiation_folder, value).resolve().as_posix()

    @property
    def execution_folder(self):
        return pathlib.Path(self._input_params['simulation_folder']).as_posix()

    @property
    def initiation_folder(self):
        return pathlib.Path(self._input_params['simulation_folder']).as_posix()

    @property
    def params_folder(self):
        return pathlib.Path(self.execution_folder, self._input_params['params_folder']).resolve().as_posix()

    def command(self):
        return 'honeybee-radiance octree from-folder model --output scene.oct --{include_aperture}-aperture --{black_out}'.format(include_aperture=self.include_aperture, black_out=self.black_out)

    def requires(self):
        return {'CreateRadFolder': CreateRadFolder(_input_params=self._input_params)}

    def output(self):
        return {
            'scene_file': luigi.LocalTarget(
                pathlib.Path(self.execution_folder, 'resources/scene.oct').resolve().as_posix()
            )
        }

    @property
    def input_artifacts(self):
        return [
            {'name': 'model', 'to': 'model', 'from': self.model, 'optional': False}]

    @property
    def output_artifacts(self):
        return [
            {
                'name': 'scene-file', 'from': 'scene.oct',
                'to': pathlib.Path(self.execution_folder, 'resources/scene.oct').resolve().as_posix(),
                'optional': False,
                'type': 'file'
            }]


class CreateRadFolder(QueenbeeTask):
    """Create a Radiance folder from a HBJSON input file."""

    # DAG Input parameters
    _input_params = luigi.DictParameter()

    # Task inputs
    @property
    def grid_filter(self):
        return self._input_params['grid_filter']

    @property
    def input_model(self):
        value = pathlib.Path(self._input_params['model'])
        return value.as_posix() if value.is_absolute() \
            else pathlib.Path(self.initiation_folder, value).resolve().as_posix()

    @property
    def execution_folder(self):
        return pathlib.Path(self._input_params['simulation_folder']).as_posix()

    @property
    def initiation_folder(self):
        return pathlib.Path(self._input_params['simulation_folder']).as_posix()

    @property
    def params_folder(self):
        return pathlib.Path(self.execution_folder, self._input_params['params_folder']).resolve().as_posix()

    def command(self):
        return 'honeybee-radiance translate model-to-rad-folder model.hbjson --grid "{grid_filter}" --grid-check'.format(grid_filter=self.grid_filter)

    def output(self):
        return {
            
            'model_folder': luigi.LocalTarget(
                pathlib.Path(self.execution_folder, 'model').resolve().as_posix()
            ),
            
            'bsdf_folder': luigi.LocalTarget(
                pathlib.Path(self.execution_folder, 'model/bsdf').resolve().as_posix()
            ),
            
            'sensor_grids_file': luigi.LocalTarget(
                pathlib.Path(self.execution_folder, 'results/grids_info.json').resolve().as_posix()
            ),
            'sensor_grids': luigi.LocalTarget(
                pathlib.Path(
                    self.params_folder,
                    'model/grid/_info.json').resolve().as_posix()
                )
        }

    @property
    def input_artifacts(self):
        return [
            {'name': 'input_model', 'to': 'model.hbjson', 'from': self.input_model, 'optional': False}]

    @property
    def output_artifacts(self):
        return [
            {
                'name': 'model-folder', 'from': 'model',
                'to': pathlib.Path(self.execution_folder, 'model').resolve().as_posix(),
                'optional': False,
                'type': 'folder'
            },
                
            {
                'name': 'bsdf-folder', 'from': 'model/bsdf',
                'to': pathlib.Path(self.execution_folder, 'model/bsdf').resolve().as_posix(),
                'optional': True,
                'type': 'folder'
            },
                
            {
                'name': 'sensor-grids-file', 'from': 'model/grid/_info.json',
                'to': pathlib.Path(self.execution_folder, 'results/grids_info.json').resolve().as_posix(),
                'optional': False,
                'type': 'file'
            }]

    @property
    def output_parameters(self):
        return [{'name': 'sensor-grids', 'from': 'model/grid/_info.json', 'to': pathlib.Path(self.params_folder, 'model/grid/_info.json').resolve().as_posix()}]


class CreateSkyDome(QueenbeeTask):
    """Create a skydome for daylight coefficient studies."""

    # DAG Input parameters
    _input_params = luigi.DictParameter()

    # Task inputs
    sky_density = luigi.Parameter(default='1')

    @property
    def execution_folder(self):
        return pathlib.Path(self._input_params['simulation_folder']).as_posix()

    @property
    def initiation_folder(self):
        return pathlib.Path(self._input_params['simulation_folder']).as_posix()

    @property
    def params_folder(self):
        return pathlib.Path(self.execution_folder, self._input_params['params_folder']).resolve().as_posix()

    def command(self):
        return 'honeybee-radiance sky skydome --name rflux_sky.sky --sky-density {sky_density}'.format(sky_density=self.sky_density)

    def output(self):
        return {
            'sky_dome': luigi.LocalTarget(
                pathlib.Path(self.execution_folder, 'resources/sky.dome').resolve().as_posix()
            )
        }

    @property
    def output_artifacts(self):
        return [
            {
                'name': 'sky-dome', 'from': 'rflux_sky.sky',
                'to': pathlib.Path(self.execution_folder, 'resources/sky.dome').resolve().as_posix(),
                'optional': False,
                'type': 'file'
            }]


class CreateTotalSky(QueenbeeTask):
    """Generate a sun-up sky matrix."""

    # DAG Input parameters
    _input_params = luigi.DictParameter()

    # Task inputs
    @property
    def north(self):
        return self._input_params['north']

    @property
    def sun_up_hours(self):
        return 'sun-up-hours'

    cumulative = luigi.Parameter(default='hourly')

    output_format = luigi.Parameter(default='ASCII')

    output_type = luigi.Parameter(default='visible')

    sky_density = luigi.Parameter(default='1')

    sky_type = luigi.Parameter(default='total')

    @property
    def wea(self):
        value = pathlib.Path(self._input_params['wea'])
        return value.as_posix() if value.is_absolute() \
            else pathlib.Path(self.initiation_folder, value).resolve().as_posix()

    @property
    def execution_folder(self):
        return pathlib.Path(self._input_params['simulation_folder']).as_posix()

    @property
    def initiation_folder(self):
        return pathlib.Path(self._input_params['simulation_folder']).as_posix()

    @property
    def params_folder(self):
        return pathlib.Path(self.execution_folder, self._input_params['params_folder']).resolve().as_posix()

    def command(self):
        return 'honeybee-radiance sky mtx sky.wea --name sky --north {north} --sky-type {sky_type} --{cumulative} --{sun_up_hours} --{output_type} --output-format {output_format} --sky-density {sky_density}'.format(north=self.north, sky_type=self.sky_type, cumulative=self.cumulative, sun_up_hours=self.sun_up_hours, output_type=self.output_type, output_format=self.output_format, sky_density=self.sky_density)

    def output(self):
        return {
            'sky_matrix': luigi.LocalTarget(
                pathlib.Path(self.execution_folder, 'resources/sky.mtx').resolve().as_posix()
            )
        }

    @property
    def input_artifacts(self):
        return [
            {'name': 'wea', 'to': 'sky.wea', 'from': self.wea, 'optional': False}]

    @property
    def output_artifacts(self):
        return [
            {
                'name': 'sky-matrix', 'from': 'sky.mtx',
                'to': pathlib.Path(self.execution_folder, 'resources/sky.mtx').resolve().as_posix(),
                'optional': False,
                'type': 'file'
            }]


class DaylightGlareAutonomy(QueenbeeTask):
    """Calculate annual glare autonomy for imageless annual glare simulation."""

    # DAG Input parameters
    _input_params = luigi.DictParameter()

    # Task inputs
    @property
    def glare_threshold(self):
        return self._input_params['glare_threshold']

    @property
    def folder(self):
        value = pathlib.Path(self.input()['RestructureDaylightGlareProbabilityResults']['output_folder'].path)
        return value.as_posix() if value.is_absolute() \
            else pathlib.Path(self.initiation_folder, value).resolve().as_posix()

    @property
    def schedule(self):
        try:
            pathlib.Path(self._input_params['schedule'])
        except TypeError:
            # optional artifact
            return None
        value = pathlib.Path(self._input_params['schedule'])
        return value.as_posix() if value.is_absolute() \
            else pathlib.Path(self.initiation_folder, value).resolve().as_posix()

    @property
    def execution_folder(self):
        return pathlib.Path(self._input_params['simulation_folder']).as_posix()

    @property
    def initiation_folder(self):
        return pathlib.Path(self._input_params['simulation_folder']).as_posix()

    @property
    def params_folder(self):
        return pathlib.Path(self.execution_folder, self._input_params['params_folder']).resolve().as_posix()

    def command(self):
        return 'honeybee-radiance post-process annual-glare raw_results --schedule schedule.txt --glare-threshold {glare_threshold} --sub_folder ../metrics'.format(glare_threshold=self.glare_threshold)

    def requires(self):
        return {'RestructureDaylightGlareProbabilityResults': RestructureDaylightGlareProbabilityResults(_input_params=self._input_params)}

    def output(self):
        return {
            'annual_metrics': luigi.LocalTarget(
                pathlib.Path(self.execution_folder, 'metrics').resolve().as_posix()
            )
        }

    @property
    def input_artifacts(self):
        return [
            {'name': 'folder', 'to': 'raw_results', 'from': self.folder, 'optional': False},
            {'name': 'schedule', 'to': 'schedule.txt', 'from': self.schedule, 'optional': True}]

    @property
    def output_artifacts(self):
        return [
            {
                'name': 'annual-metrics', 'from': 'metrics',
                'to': pathlib.Path(self.execution_folder, 'metrics').resolve().as_posix(),
                'optional': False,
                'type': 'folder'
            }]


class GenerateSunpath(QueenbeeTask):
    """Generate a Radiance sun matrix (AKA sun-path)."""

    # DAG Input parameters
    _input_params = luigi.DictParameter()

    # Task inputs
    @property
    def north(self):
        return self._input_params['north']

    output_type = luigi.Parameter(default='0')

    @property
    def wea(self):
        value = pathlib.Path(self._input_params['wea'])
        return value.as_posix() if value.is_absolute() \
            else pathlib.Path(self.initiation_folder, value).resolve().as_posix()

    @property
    def execution_folder(self):
        return pathlib.Path(self._input_params['simulation_folder']).as_posix()

    @property
    def initiation_folder(self):
        return pathlib.Path(self._input_params['simulation_folder']).as_posix()

    @property
    def params_folder(self):
        return pathlib.Path(self.execution_folder, self._input_params['params_folder']).resolve().as_posix()

    def command(self):
        return 'gendaymtx -n -D sunpath.mtx -M suns.mod -O{output_type} -r {north} -v sky.wea'.format(output_type=self.output_type, north=self.north)

    def output(self):
        return {
            'sun_modifiers': luigi.LocalTarget(
                pathlib.Path(self.execution_folder, 'resources/suns.mod').resolve().as_posix()
            )
        }

    @property
    def input_artifacts(self):
        return [
            {'name': 'wea', 'to': 'sky.wea', 'from': self.wea, 'optional': False}]

    @property
    def output_artifacts(self):
        return [
            {
                'name': 'sun-modifiers', 'from': 'suns.mod',
                'to': pathlib.Path(self.execution_folder, 'resources/suns.mod').resolve().as_posix(),
                'optional': False,
                'type': 'file'
            }]


class ParseSunUpHours(QueenbeeTask):
    """Parse sun up hours from sun modifiers file."""

    # DAG Input parameters
    _input_params = luigi.DictParameter()

    # Task inputs
    @property
    def sun_modifiers(self):
        value = pathlib.Path(self.input()['GenerateSunpath']['sun_modifiers'].path)
        return value.as_posix() if value.is_absolute() \
            else pathlib.Path(self.initiation_folder, value).resolve().as_posix()

    @property
    def execution_folder(self):
        return pathlib.Path(self._input_params['simulation_folder']).as_posix()

    @property
    def initiation_folder(self):
        return pathlib.Path(self._input_params['simulation_folder']).as_posix()

    @property
    def params_folder(self):
        return pathlib.Path(self.execution_folder, self._input_params['params_folder']).resolve().as_posix()

    def command(self):
        return 'honeybee-radiance sunpath parse-hours suns.mod --name sun-up-hours.txt'

    def requires(self):
        return {'GenerateSunpath': GenerateSunpath(_input_params=self._input_params)}

    def output(self):
        return {
            'sun_up_hours': luigi.LocalTarget(
                pathlib.Path(self.execution_folder, 'results/sun-up-hours.txt').resolve().as_posix()
            )
        }

    @property
    def input_artifacts(self):
        return [
            {'name': 'sun_modifiers', 'to': 'suns.mod', 'from': self.sun_modifiers, 'optional': False}]

    @property
    def output_artifacts(self):
        return [
            {
                'name': 'sun-up-hours', 'from': 'sun-up-hours.txt',
                'to': pathlib.Path(self.execution_folder, 'results/sun-up-hours.txt').resolve().as_posix(),
                'optional': False,
                'type': 'file'
            }]


class RestructureDaylightGlareProbabilityResults(QueenbeeTask):
    """Restructure files in a distributed folder."""

    # DAG Input parameters
    _input_params = luigi.DictParameter()

    # Task inputs
    @property
    def extension(self):
        return 'dgp'

    @property
    def input_folder(self):
        value = pathlib.Path('initial_results/dgp')
        return value.as_posix() if value.is_absolute() \
            else pathlib.Path(self.initiation_folder, value).resolve().as_posix()

    @property
    def execution_folder(self):
        return pathlib.Path(self._input_params['simulation_folder']).as_posix()

    @property
    def initiation_folder(self):
        return pathlib.Path(self._input_params['simulation_folder']).as_posix()

    @property
    def params_folder(self):
        return pathlib.Path(self.execution_folder, self._input_params['params_folder']).resolve().as_posix()

    def command(self):
        return 'honeybee-radiance grid merge-folder ./input_folder ./output_folder  {extension} --dist-info dist_info.json'.format(extension=self.extension)

    def requires(self):
        return {'AnnualImagelessGlare': AnnualImagelessGlare(_input_params=self._input_params)}

    def output(self):
        return {
            'output_folder': luigi.LocalTarget(
                pathlib.Path(self.execution_folder, 'results').resolve().as_posix()
            )
        }

    @property
    def input_artifacts(self):
        return [
            {'name': 'input_folder', 'to': 'input_folder', 'from': self.input_folder, 'optional': False}]

    @property
    def output_artifacts(self):
        return [
            {
                'name': 'output-folder', 'from': 'output_folder',
                'to': pathlib.Path(self.execution_folder, 'results').resolve().as_posix(),
                'optional': False,
                'type': 'folder'
            }]


class SplitGridFolder(QueenbeeTask):
    """Create new sensor grids folder with evenly distributed sensors.

    This function creates a new folder with evenly distributed sensor grids. The folder
    will include a ``_redist_info.json`` file which has the information to recreate the
    original input files from this folder and the results generated based on the grids
    in this folder."""

    # DAG Input parameters
    _input_params = luigi.DictParameter()

    # Task inputs
    @property
    def cpu_count(self):
        return self._input_params['cpu_count']

    @property
    def cpus_per_grid(self):
        return '1'

    @property
    def min_sensor_count(self):
        return self._input_params['min_sensor_count']

    @property
    def input_folder(self):
        value = pathlib.Path(self.input()['CreateRadFolder']['model_folder'].path, 'grid')
        return value.as_posix() if value.is_absolute() \
            else pathlib.Path(self.initiation_folder, value).resolve().as_posix()

    @property
    def execution_folder(self):
        return pathlib.Path(self._input_params['simulation_folder']).as_posix()

    @property
    def initiation_folder(self):
        return pathlib.Path(self._input_params['simulation_folder']).as_posix()

    @property
    def params_folder(self):
        return pathlib.Path(self.execution_folder, self._input_params['params_folder']).resolve().as_posix()

    def command(self):
        return 'honeybee-radiance grid split-folder ./input_folder ./output_folder {cpu_count} --grid-divisor {cpus_per_grid} --min-sensor-count {min_sensor_count}'.format(cpu_count=self.cpu_count, cpus_per_grid=self.cpus_per_grid, min_sensor_count=self.min_sensor_count)

    def requires(self):
        return {'CreateRadFolder': CreateRadFolder(_input_params=self._input_params)}

    def output(self):
        return {
            
            'output_folder': luigi.LocalTarget(
                pathlib.Path(self.execution_folder, 'resources/grid').resolve().as_posix()
            ),
            
            'dist_info': luigi.LocalTarget(
                pathlib.Path(self.execution_folder, 'initial_results/ga/_redist_info.json').resolve().as_posix()
            ),
            'sensor_grids': luigi.LocalTarget(
                pathlib.Path(
                    self.params_folder,
                    'output_folder/_info.json').resolve().as_posix()
                )
        }

    @property
    def input_artifacts(self):
        return [
            {'name': 'input_folder', 'to': 'input_folder', 'from': self.input_folder, 'optional': False}]

    @property
    def output_artifacts(self):
        return [
            {
                'name': 'output-folder', 'from': 'output_folder',
                'to': pathlib.Path(self.execution_folder, 'resources/grid').resolve().as_posix(),
                'optional': False,
                'type': 'folder'
            },
                
            {
                'name': 'dist-info', 'from': 'output_folder/_redist_info.json',
                'to': pathlib.Path(self.execution_folder, 'initial_results/ga/_redist_info.json').resolve().as_posix(),
                'optional': False,
                'type': 'file'
            }]

    @property
    def output_parameters(self):
        return [{'name': 'sensor-grids', 'from': 'output_folder/_info.json', 'to': pathlib.Path(self.params_folder, 'output_folder/_info.json').resolve().as_posix()}]


class _Main_5a4cf8eaOrchestrator(luigi.WrapperTask):
    """Runs all the tasks in this module."""
    # user input for this module
    _input_params = luigi.DictParameter()

    @property
    def input_values(self):
        params = dict(_default_inputs)
        params.update(dict(self._input_params))
        return params

    def requires(self):
        yield [CopyGridInfo(_input_params=self.input_values), CopyRedistInfo(_input_params=self.input_values), DaylightGlareAutonomy(_input_params=self.input_values), ParseSunUpHours(_input_params=self.input_values)]
