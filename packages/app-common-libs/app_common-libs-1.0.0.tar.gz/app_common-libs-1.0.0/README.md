Push pip package on gitlab using following commands

Generate package 
    `python3 setup.py sdist bdist_wheel`

Upload package 
    `TWINE_PASSWORD=${GIT_CI_TOKEN} TWINE_USERNAME=gitlab-ci-token python -m twine upload --repository-url https://gitlab.com/api/v4/projects/1050/packages/pypi dist/* --verbose`