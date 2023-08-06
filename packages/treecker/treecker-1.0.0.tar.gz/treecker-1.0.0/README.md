# Treecker

> What does it mean?

The name "Treecker" comes from the contraction of "tree" and "tracker".

> What is it for?

Treecker is a Python package to control the integrity of a directory.

> Is it hard to use?

Just type one of the available commands in a terminal.

## Background

Have you ever wondered if you had accidentally destroyed or altered a part of the data contained in your favorite directory without realizing it?
Do you want to be able to stamp a part of your data and to control at any time that they are always the state where you had left them?
Do you think that one of your files has been corrupted, but you don't know which one?
If so, this package is for you.

## Features

This Python package is for inspecting and tracking the organization of files in a directory.
A snapshot of the tree structure is saved in a file placed at the root of the tracked directory.
At any time it is possible to compare the current state of the directory with the latest snapshot, and to save the new state.
The program can also check that the file and folder names match a regular expression.
This allows to detect errors in the naming of files.
These features are accessible via the following commands:

* `init`: To create the first snapshot of a directory.
* `status`: To display the changes since last snapshot.
* `commit`: To save the change in a new snapshot.
* `issues`: To display incorrectly named files and directories.

## Installation

Treecker is available on the [Python Package Index](https://pypi.org/project/treecker).
The easiest way to install it is to run the following command:

```bash
pip install treecker
```

## Usage

### Accepted arguments

Run the following commands to display information about the accepted arguments in each of the program features.

```bash
treecker init --help
treecker status --help
treecker commit --help
treecker issues --help
```

To execute the following commands in another directory than the one in which the command is executed, it is possible to use the option `--dir`, followed by the path of the tracked directory.

### Initialization

To initialize a tree tracker in a directory, run the following command.
This will create a file named `treecker.json` in the directory to track.

```bash
treecker init --hash
```

With the option `--hash`, treecker will compute and store a hash value of the tracked files.
If this option is used, the generation time of the snapshot will be strongly lengthened, but it will be possible to detect possible data corruption in the future.
If the option `--no-hash` is given instead, only the size of the files will be saved for future comparisons.
Selecting `--hash` or `--no-hash` in the treecker initialization will determine if hash values are computed in future commits.

### Status

To display the changes made since the last snapshot, execute the following command.

```bash
treecker status --hash
```

With the option `--hash`, treecker will compute the current hash values of the files in tracked directory and compare them to those saved in the latest snapshot.
This option cannot be used if the treecker was initialized without hash values.
With the option `--no-hash`, treecker will only perform file comparisons based on their size.

### Commit

To save the change displayed in the status, run the following command.
This will overwrite the `treecker.json` file.

```bash
treecker commit
```

### Name verification

To display incorrectly nammed files and directories, execute the following command.

```bash
treecker issues
```

The regular expression to be matched can be redefined in a local configuration file.

### Configuration

A special configuration can be set up to track a directory.
For this, add a configuration file called `treecker.conf` at the root of the tracked directory, that is, next to the `treecker.json` file.
It is then possible to choose, among others, which file or directory names will be ignored in the tracking or in the name verification:

```ini
[treecker.core.naming]
ignore = README* LICENSE* CITATION* INSTALL* SETUP* *.php LC_MESSAGES en_US en_GB fr_FR

[treecker.core.snapshot]
ignore = __pycache__ .git
```

For more configuration options, see the default configuration file [`default.conf`](/src/treecker/core/default.conf).

## Credits

* Dunstan Becht

## License

This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with this program. If not, see <https://www.gnu.org/licenses/>.
