# bulk
Bulk helps you declare, manage and install dependencies of Python projects.

# Installations
install bulk on python using pip

```shell
    pip install bulk-cli
```

# Bulk commands
```shell
    bulk init
```

init bulk config in a project 
if you have an old project using pip use the flag
``--ancestor=pip`` ( Not necessary if you have requirements.txt in your project)

```shell
bulk install
```

If you have requirements.txt file in your project bulk will add all packages from it to bulk.dependencies 

```shell
bulk install package-name
```

Install a package from pip library

```shell
bulk install --dry
```
Create bulk config from pip packages without installing

```shell
bulk uninstall
```
Uninstall project dependencies

```shell
bulk uninstall package-name
```

Uninstall a package from pip library


```shell
bulk run ...
```

Bulk allows you to run multiple commands one 

```json
    {
        "script": {
            "dev": "python manage.py makemigrations && python manage.py migrate && python manage.py runserver"
        }
    }
```

Note: replace && with ; if you are using windows
run dev 
```shell
    bulk run dev
```

# Documentation
Documentation for the current version of Bulk  is available from github README.


[!["Buy Me A Coffee"](https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png)](https://www.buymeacoffee.com/lyonkvalid)