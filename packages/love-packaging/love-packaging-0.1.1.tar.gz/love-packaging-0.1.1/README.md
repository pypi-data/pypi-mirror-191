# Love Packaging
Package your LÖVE games with Python

## Install

````commandline
python -m pip install -U love-packaging
````

## Help

````
python -m love_packaging --help
usage: __main__.py [-h] -g GROUP_NAME -p PROJECT_NAME [-i COMMIT_ID] [-l LOVE_VERSION] [-c | --cleanup | --no-cleanup]

options:
  -h, --help            show this help message and exit
  -g GROUP_NAME, --group-name GROUP_NAME
                        Specify Gitlab group name (e.g. stone-kingdoms)
  -p PROJECT_NAME, --project-name PROJECT_NAME
                        Specify Gitlab project name (e.g. stone-kingdoms)
  -i COMMIT_ID, --commit-id COMMIT_ID
                        Specify which commit id to checkout (e.g. master)
  -l LOVE_VERSION, --love-version LOVE_VERSION
                        Love version to package (e.g. 11.4)
  -c, --cleanup, --no-cleanup
                        Cleanup intermediate directories and files
````

## Example with LÖVE game [stone-kingdoms](https://gitlab.com/stone-kingdoms/stone-kingdoms)

````commandline
python -m love_packaging -g stone-kingdoms -p stone-kingdoms --cleanup
````
