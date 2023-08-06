import yaml
import os




_file = os.path.join(os.path.split(__file__)[0],
                     'styles.yml')

STYLES = yaml.safe_load(open(_file))

SELECTED = 'selected'
NORMAL = 'normal'
DEFAULT = 'default'
DISABLED = 'disabled'
