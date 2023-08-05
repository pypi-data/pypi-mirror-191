import json
import logging
import os

logger = logging.getLogger('SmartCI')


class PydepsAccessor:
    _LOG_PREFIX = 'PyDepsAccessor'

    @classmethod
    def create_dependencies_graph(cls, project_path: str, package_name: str) -> dict:
        os.chdir(project_path)
        stream = os.popen(f'pydeps {package_name} --cluster --show-deps --no-output')
        output = stream.read()
        if output and '(Did you forget to include an __init__.py?)' not in output:
            return json.loads(output)
        else:
            logger.warning(f'{cls._LOG_PREFIX}: Failed to parse response for {project_path}/{package_name}')
            return {}
