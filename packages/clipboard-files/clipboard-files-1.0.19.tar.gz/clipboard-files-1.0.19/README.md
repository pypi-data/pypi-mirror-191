rm -r build/ dist/
python setup.py sdist bdist_wheel
pip install --force-reinstall dist/clipboard_files-{YOUR0VERSION-HERE}-py3-none-any.whl 