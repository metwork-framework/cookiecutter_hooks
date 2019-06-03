import os
import shutil
import autopep8
import re


def test_empty(path):
    try:
        with open(path, 'rb') as f:
            content = f.read().strip()
            if len(content) == 0:
                return True
    except Exception:
        pass
    return False


def safe_delete(path):
    try:
        if os.path.isdir(path):
            shutil.rmtree(path, ignore_errors=True)
        else:
            os.unlink(path)
    except Exception:
        pass


def post_gen_project():
    paths_to_delete = []
    for path in [os.path.join(x[0], y) for x in os.walk('.') for y in x[2]]:
        if path.endswith('.rename'):
            continue
        if test_empty(path):
            paths_to_delete.append(path)
        if path.endswith('.delete'):
            if not test_empty(path):
                paths_to_delete.append(path.replace('.delete', ''))
                paths_to_delete.append(path)
    for path in paths_to_delete:
        if os.path.basename(path) in ['__init__.py']:
            continue
        safe_delete(path)
    paths_to_rename = []
    paths_to_delete = []
    for path in [os.path.join(x[0], y) for x in os.walk('.') for y in x[2]]:
        if path.endswith('.rename'):
            if test_empty(path):
                paths_to_delete.append(path)
                paths_to_delete.append(path.replace('.rename', ''))
                continue
            with open(path, 'rb') as f:
                content = f.read().strip().decode("utf8")
                if len(content.encode('utf8').split(b"\n")) != 1:
                    raise Exception("bad content: [%s] for path=%s" %
                                    (content, path))
                newpath = os.path.join(os.path.dirname(path), content)
                paths_to_rename.append((path.replace('.rename', ''), newpath))
                paths_to_delete.append(path)
    for source, target in paths_to_rename:
        shutil.move(source, target)
    for path in paths_to_delete:
        safe_delete(path)
    for path in [os.path.join(x[0], y) for x in os.walk('.') for y in x[2]]:
        if all([not path.endswith(x) for x in ('.py', '.conf', '.ini',
                                               '.js', '.html', '.json')]):
            continue
        with open(path, 'r') as f:
            # reduce multi blank lines to a single one
            content = f.read()
            content = re.sub(r'\n\s*\n', '\n\n', content)
            content = re.sub(r'^\ns*\n', '\n', content)
            # conform python code to pep8
            if path.endswith('.py'):
                content = autopep8.fix_code(f.read())
        with open(path, 'w') as f:
            f.write(content)
