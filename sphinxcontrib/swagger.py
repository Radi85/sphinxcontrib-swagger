import os
import json

import jinja2
import jsonschema
import pkg_resources
import yaml

DIR = os.path.abspath(os.path.dirname(__file__))
ASSETS_DIR = os.path.join(DIR, 'assets')
_OPENAPI_CONF_SCHEMA = {
    'type': 'object',
    'properties': {
        'title': {'type': 'string'},  # document title - Default `OpenAPI Documentation`
        'spec_path': {'type': 'string'},  # path to openapi yaml/json file relative to `config.py` file.
        'page_name': {'type': 'string'},  # rendered standalone openapi page - Default `swagger`
        # name of existing document that swagger to be embedded in. The document must have `{{openapi}}` value inside.
        'swagger_embedded_in': {'type': 'string'},
        # path to openapi html template relative to `config.py` file.
        'template': {'type': 'string'},
    },
    'required': ['spec_path'],
    'additionalProperties': False,
}


def validate_openapi_config(config):
    try:
        jsonschema.validate(config, schema=_OPENAPI_CONF_SCHEMA)
    except jsonschema.ValidationError as exc:
        raise ValueError(
            'Improper configuration for sphinxcontrib-swagger at %s: %s' % (
                '.'.join((str(part) for part in exc.path)),
                exc.message,
            )
        )


def get_openapi_template(app):
    openapi_template = app.config.openapi.get('template')
    if openapi_template and os.path.exists(os.path.join(app.confdir, openapi_template)):
        return os.path.join(app.confdir, openapi_template)
    else:
        return os.path.join(ASSETS_DIR, 'openapi.html')


def get_standalone_page_name(config):
    default_page_name = config.get('page_name', 'swagger')
    if default_page_name == config.get('swagger_embedded_in'):
        return f'_{default_page_name}'
    return default_page_name


def render(app):
    config = app.config.openapi
    validate_openapi_config(config)
    template_path = get_openapi_template(app)

    context = {}

    with open(template_path, encoding='utf-8') as f:
        template = jinja2.Template(f.read())

    yaml_file = os.path.join(app.confdir, config['spec_path'])
    with open(yaml_file, encoding='utf-8') as f:
        try:
            spec_contents = yaml.safe_load(f)
        except ValueError as error:
            raise ValueError('Cannot parse yaml %r: %s' % (config['spec_path'], error))

    context['spec'] = json.dumps(spec_contents)
    context['title'] = config.get('title', 'OpenAPI Documentation')

    yield get_standalone_page_name(config), context, template


def create_embedded_openapi(app, *args):
    config = app.config.openapi
    if not config.get('swagger_embedded_in'):
        return
    template_path = get_file_path(app.outdir, config['swagger_embedded_in'])
    swagger_path = get_file_path(app.outdir, get_standalone_page_name(config))

    with open(swagger_path) as swagger_file:
        swagger = swagger_file.read()

    try:
        with open(template_path, 'r+') as f:
            output = f.read().replace('{{openapi}}', swagger)
            f.seek(0)
            f.write(output)
            f.truncate()
    except TypeError:
        raise FileNotFoundError(
            ('Embedded_in file "%s" does not exist. Make sure you have a document'
             ' for this file and listed in toctree directive'),
            template_path
        )


def get_file_path(out_dir, name):
    path = os.path.join(out_dir, name + '.html')
    if not os.path.exists(path):
        return None
    return os.path.join(out_dir, name + '.html')


def setup(app):
    app.add_config_value('openapi', {}, 'html')

    app.connect('html-collect-pages', render)
    app.connect('build-finished', create_embedded_openapi)

    version = pkg_resources.get_distribution('sphinxcontrib-swagger').version
    return {'version': version, 'parallel_read_safe': True}
