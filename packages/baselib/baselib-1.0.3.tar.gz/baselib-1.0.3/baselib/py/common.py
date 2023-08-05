import platform


IS_PY3 = int(platform.python_version_tuple()[0]) == 3

print(IS_PY3)