"""Utilities that might be useful"""
import os

# Just a little helper function for the test
def all_files_in_directory(path):
    """ Recursively list all files under a directory """
    file_list = []
    for dirname, _dirnames, filenames in os.walk(path):
        for filename in filenames:
            # Skip OS Files
            if filename != '.DS_Store':
                file_list.append(os.path.join(dirname, filename))
    return file_list

def root_dir(python_file):
    """ Root directory for the python file"""
    return os.path.dirname(os.path.realpath(python_file))

def relative_path(python_file, rel_dir):
    """ Relative path for the python file"""
    return os.path.join(root_dir(python_file), rel_dir)

def test():
    """Test the Utility methods"""
    path = relative_path(__file__, '.')
    print 'Path: %s' % path
    for my_file in all_files_in_directory(path):
        print '\t%s' % my_file
    print 'Success!'

if __name__ == '__main__':
    test()
