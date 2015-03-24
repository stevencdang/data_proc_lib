import pymongo, json
from os import mkdir, listdir, path


def date_handler(obj):
        return obj.isoformat() if hasattr(obj, 'isoformat') else obj


def write_json_to_file(data='', dir_name='data', file_name='default'):
    print "writing to directory: " + dir_name
    if not path.exists(dir_name):
        mkdir(dir_name, 0774)
    # Create file path
    file_path = path.join(dir_name, file_name + '.json')
    print "writing to: " + file_path
    # Write data to file
    resultsFile = open(file_path,'w')
    resultsFile.write(
        json.dumps(data, indent=2, default=date_handler)
    )
    resultsFile.close()
