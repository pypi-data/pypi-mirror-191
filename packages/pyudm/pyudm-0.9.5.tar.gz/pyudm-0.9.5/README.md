# Unified Dependency Manager

Unified Dependency Manager is a simple yet powerful tool aimed at simplifying dependency handling of nested projects and vcs interoperability.

This tool lets users define the dependencies of each project in a simple and clean fashion inspired by svn:externals syntax and performs all the routine operations needed to checkout, update and track supbrojects.

Dependecies can be defined in the specific file `.deps.udm` as a list of arguments such as destination folder, repository URL and other optional parameters.
Currently, both svn and git repositories can be used as dependencies. Also, udm implements a feature that automatically converts the dependency defenitions for projects that already use svn externals or git submodules (see `convert` command below).

## Usage example

Create a deps file named `.deps.udm` in your main repository root folder, for example:
```yaml
lib/libraryA:
  url: https://gitlab.com/test/libraryA

lib/libraryB:
  url: https://gitlab.com/test/libraryB
  tag: 1.0.0
  path: src/

lib/libraryC:
  url: http://repository.com/svn/projects/libraryC
  branch: release

lib/libraryD:
  url: git@gitlab.com:user/mylib
  commit: 82749DE4
  options:
    - "--sparse"
    - "--depth"
    - 1
```

 Then simply run `udm udpate`: it will create the dependecy subfolders and checkout/clone all the repositories inside as specified in the deps file. Note: this will update/pull the main repository as well, unless the argument `--only-deps` is given.

To later integrate remote changes performed on the depency repositories run `udm udpate` again.

See the list of commands below for more details and advanced uses.

## Installation

```sh
pip install .
```

or run `make` to build a standalone binary with pyinstaller. The binary will be placed in the `dist` folder.

## Main commands

### `clone` (also `checkout` or `co`)
Clone a repository and its dependencies into a new directory. By passing the `--convert` argument, `udm` will automatically create the `.deps.udm` file based on the existing definitions of svn externals or git submodules.

usage:
```sh
udm clone [-h] [--convert] url destination
```

### `update` (also `up`)
Fetch and integrate changes from the remote repository. The update action is also perfomed on dependecy repositories by default.

usage:
```sh
udm update [-h] [--only-deps] [--no-deps] [--convert]
```

### `convert`
Create the .deps.udm file based on the existing definitions of svn externals or git submodules.

usage:
```sh
udm convert [-h]
```

### `status`
Ouput the status of the main repository and its dependencies.

usage:
```sh
udm status [-h]
```

### `edit-deps`
Open the file of dependencies with the default editor or with the specified one.

usage:
```sh
udm edit-deps [-h] [--editor-cmd EDITOR]
```

### `ls-files`
List tracked files of the main repository and its dependencies.

usage:
```sh
udm ls-files [-h]
```

### `local`
Pass additional arguments directly to local repository structure, print local repository type if no argument is specified.

usage:
```sh
udm local [-h]
```

## Release History

* 0.1.0
    * First release (TODO)

## License

Distributed under the GNU GPLv2 license. See ``LICENSE`` for more information.

## Contributing

See `CONTRIBUTING.md`.
