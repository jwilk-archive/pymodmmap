import sys
import mmap
import os

mmaps = {}

def mmap_file(path):
    fd = os.open(path, os.O_RDONLY)
    try:
        mmaps[path] = mmap.mmap(fd, 0, mmap.MAP_SHARED, 0)
    finally:
        os.close(fd)

def mmap_py(path):
    if not path.endswith(('.py', '.pyc', '.pyo')):
        return
    new_path = path.rstrip('co')
    if path != new_path:
        try:
            st = os.stat(new_path)
        except OSError:
            pass
        else:
            if st.st_size > 0:
                path = new_path
    return mmap_file(path)

for module in sys.modules.values():
    try:
        source = module.__file__
    except AttributeError:
        continue
    mmap_py(source)

if __name__ == '__main__':
    __builtins__ = __builtins__.__dict__
original_import = __builtins__['__import__']

def __import__(*args, **kwargs):
    module = original_import(*args, **kwargs)
    try:
        source = module.__file__
    except AttributeError:
        pass
    else:
        mmap_py(source)
    return module

__builtins__['__import__'] = __import__

# vim:ts=4 sts=4 sw=4 et
