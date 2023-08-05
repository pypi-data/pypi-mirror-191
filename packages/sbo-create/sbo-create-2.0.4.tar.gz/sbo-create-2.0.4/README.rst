.. contents:: Table of Contents:


About
-----

sbo-create it's a tool that creates easy, fast and safe SlackBuilds files scripts.

This tool is for everyone, but package maintainers will be going to love it!

Enjoy!


Features
________

- Preloaded SlackBuilds templates.
- Checking for already SlackBuilds in the repository and the distribution.
- Autocorrect the quote marks for the .info file.
- Auto-importing the SlackBuild script name.
- Auto-importing the description project from the slack-desc file.
- Auto-importing the maintainer data to the .SlackBuild script.
- Auto-importing the version to the .SlackBuild script.
- Auto-importing and checking the checksum signature to the .info file.


Screenshot
__________

.. image:: https://gitlab.com/dslackw/images/raw/master/sbo-create/img_menu.png
    :target: https://gitlab.com/dslackw/sbo-create

.. image:: https://gitlab.com/dslackw/images/raw/master/sbo-create/img_info.png
    :target: https://gitlab.com/dslackw/sbo-create

.. image:: https://gitlab.com/dslackw/images/raw/master/sbo-create/img_slack_desc.png
    :target: https://gitlab.com/dslackw/sbo-create



Install
-------

.. code-block:: bash

    $ tar xvf sbo-create-2.0.4.tar.gz
    $ cd sbo-create-2.0.4
    $ ./install.sh

    or

    $ slpkg install sbo-create


Requirements
------------

- Requires Python 3.9+

- python3-pythondialog >= 3.5.3


Usage
-----

.. code-block:: bash

    Usage: sbo-create <sbo_name>

    Optional arguments:
      -h, --help           Display this message and exit.
      -v, --version        Show version and exit.


For a new project, you should create at first a new folder with the same name as
the project.
For an existing project, come into the folder and start to edit, just run `sbo-create`.

It's good you know before you start, please visit here: `HOWTO <https://slackbuilds.org/howto/>`_


Note
----
The :code:`sbo-create` tool checks before you create a slackbuild and if the package exists in your distribution that
you have installed, you get a warning message before you proceed.


Donate
------

If you feel satisfied with this project and want to thanks me make a donation.

.. image:: https://gitlab.com/dslackw/images/raw/master/donate/paypaldonate.png
   :target: https://www.paypal.me/dslackw


Copyright 
---------

- Copyright © 2015-2022 Dimitris Zlatanidis
- Slackware ® is a Registered Trademark of Patrick Volkerding.
- Linux is a Registered Trademark of Linus Torvalds.
