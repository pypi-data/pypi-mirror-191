Charlie Brown
!!!!!!!!!!!!!

Charlie Brown is a program for compulsively checking your mail. It waits for notifications of new email via `IMAP IDLE <https://en.wikipedia.org/wiki/IMAP_IDLE>`_ and pops up a `KDialog <https://invent.kde.org/utilities/kdialog>`_ with a preview of each message. The dialog has buttons to dismiss it without taking an action ("Keep"), mark the message as read ("Mark Read"), or move the message to your IMAP trash folder without marking it as read ("Trash").

.. image:: https://i.imgur.com/BYu3cJJ.png
   :alt: An example dialog box

If you have lots of new messages at once (see ``max_itemized_messages`` below), you'll get a single dialog box with just the number of messages, instead of one dialog box per message as usual.

Installation and usage
============================================================

Although Charlie Brown has no programmatic interface, it's distributed as a Python package (written in `Hy <http://hylang.org>`_). Install it via `pip <https://pypi.org/project/pip/>`_ with the command ``pip install charlie_brown`` (the only dependency not automatically installed is KDialog) and run it with ``python3 -m charlie_brown``. Charlie Brown doesn't daemonize itself, but I like to daemonize it with a command like ``nohup python3 -m charlie_brown 2>/tmp/charlie-brown-debug >/dev/null &``.

To run at all, Charlie Brown requires a `JSON <https://www.json.org>`_ configuration file, which you should put in ``$XDG_CONFIG_HOME/charlie_brown.json``. Here's an example::

    {
        "tempfile": "/tmp/charlie-brown",
        "server": "imap.example.com",
        "username": "igelfeldm",
        "password": "hunter2",
        "folder_monitor": "INBOX",
        "folder_trash": "Trash",
        "max_itemized_messages": 10,
        "global_timeout_seconds": 10,
        "idle_timeout_minutes": 5,
        "login_interval_minutes": 10,
        "body_preview_bytes": 256,
        "kdialog_max_word_len": 40
    }

All options are required. Their meaning is as follows:

``tempfile``
  A path to save a temporary file. This is used for recording which messages have already been reported. For Charlie Brown to consider a message new, it has to be neither recorded here nor marked read on the IMAP side.
``server``
  The hostname of your IMAP server.
``username``, ``password``
  Credentials for the server.
``folder_monitor``
  The IMAP folder to monitor for new messages.
``folder_trash``
  The IMAP folder to put files in when you click "Trash".
``max_itemized_messages``
  How many messages to preview. If Charlie Brown has more than this to report at a single time, you just get a count instead of a dialog for each message.
``global_timeout_seconds``
  A general timeout value for IMAP operations.
``idle_timeout_minutes``
  A timeout for IDLE waiting.
``login_interval_minutes``
  A maximum time to wait before logging in again.
``body_preview_bytes``
  How many bytes of each message's body are retrieved for making the preview.
``kdialog_max_word_len``
  The maximum number of sequential non-whitespace characters in the message preview before a newline is inserted, to work around KDialog's behavior of truncating the whole dialog contents if a word is too long. If you don't use big fonts like I do, you can probably set this higher.

Trivia
============================================================

Although the first commit in this repository is from 2023, Charlie Brown is one of my oldest codebases that I still use. It started out as a Perl script no later than 2007.

License
============================================================

This program is copyright 2023 Kodi B. Arfer.

This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the `GNU General Public License`_ for more details.

.. _`GNU General Public License`: http://www.gnu.org/licenses/

