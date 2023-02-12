======
zipind
======


.. image:: https://img.shields.io/pypi/v/zipind.svg
        :target: https://pypi.python.org/pypi/zipind

.. image:: https://readthedocs.org/projects/zipind/badge/?version=latest
        :target: https://zipind.readthedocs.io/en/latest/?version=latest
        :alt: Documentation Status

zipind - From a folder, make a splitted ZIP with INDependent parts


* Free software: MIT license
* Documentation: https://zipind.readthedocs.io.


Features
--------

- Compact folder to .zip or .rar, dividing it into independent parts, grouping your files in alphanumeric order.
- Preserve the ordering of folders and files.
- Preserve the internal structure of folders.
- If any file exceeds the defined maximum size, the specific file is splitted in dependent mode.
- Set the file types to be ignored in compression (config/ignore_extensions.txt)
- Verify that the file path length is less than the specified limit (default 250 characters).
- Sanitize the folder and file names characters to ensure compatibility with UTF-8 encoding, by auto-renaming.

Requirements
------------

- To compress to Zip format, It is necessary to have 7Zip_ app installed and added in system variables
- To compress to Rar format, It is necessary to have Winrar_ app installed and added in system variables


Usage
-----

Let's zip a folder, with a maximum of 100MB per file, in zip mode and ignoring 'ISO' extension files.

**Through python script importation**

.. code-block:: python

    import zipind

    path_folder = r'c://my_project'

    zipind.run(path_folder, mode='zip', mb_perfile=100, mode='zip', ignore_extensions=['iso'])


**Through terminal in chatbot-like style**


.. code-block:: text

    $ zipind

Zipind will start by responding:

.. code-block:: text

    Zipind - From a folder, make a splitted ZIP with INDependent parts
    >> github.com/apenasrr/zipind <<

    Paste the folder path to be compressed:


Now paste the folder path to be compressed:

.. code-block:: text

    Paste the folder path to be compressed: c://my_project

Answer the questions to customize the parameters and your project will be processed.

**CLI Mode**

Soon...


We recommend
------------

`mises.org`_ - Educate yourself about economic and political freedom

`lbry.tv`_ - Store files and videos on blockchain ensuring free speech

`A Cypherpunk's Manifesto`_ - How encryption is essential to Free Speech and Privacy


Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
.. _`7Zip`: https://www.7-zip.org/download.html
.. _`Winrar`: https://www.win-rar.com/download.html
.. _`mises.org`: https://mises.org/
.. _`lbry.tv`: http://lbry.tv/
.. _`A Cypherpunk's Manifesto`: https://www.activism.net/cypherpunk/manifesto.html