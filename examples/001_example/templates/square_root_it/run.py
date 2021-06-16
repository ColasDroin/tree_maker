import json
import numpy as np
import ruamel.yaml
import tree_maker

# load the configuration
with open('config.yaml', 'r') as file:
    yaml = ruamel.yaml.YAML()
    cfg = yaml.load(file)
    
with open(cfg['parent']+'/output.yaml', 'r') as file:
    yaml = ruamel.yaml.YAML()
    parent_out = yaml.load(file)
    
tree_maker.tag.tag_it(cfg['log_file'], 'started')
    
# define the function (sqrt of a number)
def my_function(my_x):
    'Just an addition'
    return float(np.sqrt(np.abs(my_x)))

# run the code
result = my_function(parent_out['result'])

with open('output.yaml', 'w') as fp:
    yaml = ruamel.yaml.YAML()
    yaml.dump({'result': result}, fp)

tree_maker.tag.tag_it(cfg['log_file'], 'completed')
    

