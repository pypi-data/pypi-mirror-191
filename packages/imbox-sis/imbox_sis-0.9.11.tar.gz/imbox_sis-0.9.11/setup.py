# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['imbox_sis', 'imbox_sis.vendors']

package_data = \
{'': ['*']}

install_requires = \
['chardet>=5.0.0,<6.0.0']

setup_kwargs = {
    'name': 'imbox-sis',
    'version': '0.9.11',
    'description': '',
    'long_description': "# Imbox - Python IMAP for Humans\n\n![workflow](https://github.com/martinrusev/imbox/actions/workflows/python-app.yml/badge.svg)\n\nPython library for reading IMAP mailboxes and converting email content\nto machine readable data\n\n## Requirements\n\nPython (3.6, 3.7, 3.8, 3.9)\n\n## Installation\n\n`pip install imbox-sis`\n\n## Usage\n\n``` python\nfrom imbox_sis import Imbox\n\n# SSL Context docs https://docs.python.org/3/library/ssl.html#ssl.create_default_context\n\nwith Imbox('imap.gmail.com',\n        username='username',\n        password='password',\n        ssl=True,\n        ssl_context=None,\n        starttls=False) as imbox:\n\n    # Get all folders\n    status, folders_with_additional_info = imbox.folders()\n\n    # Gets all messages from the inbox\n    all_inbox_messages = imbox.messages()\n\n    # Unread messages\n    unread_inbox_messages = imbox.messages(unread=True)\n\n    # Flagged messages\n    inbox_flagged_messages = imbox.messages(flagged=True)\n\n    # Un-flagged messages\n    inbox_unflagged_messages = imbox.messages(unflagged=True)\n\n    # Flagged messages\n    flagged_messages = imbox.messages(flagged=True)\n\n    # Un-flagged messages\n    unflagged_messages = imbox.messages(unflagged=True)\n\n    # Messages sent FROM\n    inbox_messages_from = imbox.messages(sent_from='sender@example.org')\n\n    # Messages sent TO\n    inbox_messages_to = imbox.messages(sent_to='receiver@example.org')\n\n    # Messages received before specific date\n    inbox_messages_received_before = imbox.messages(date__lt=datetime.date(2018, 7, 31))\n\n    # Messages received after specific date\n    inbox_messages_received_after = imbox.messages(date__gt=datetime.date(2018, 7, 30))\n\n    # Messages received on a specific date\n    inbox_messages_received_on_date = imbox.messages(date__on=datetime.date(2018, 7, 30))\n\n    # Messages whose subjects contain a string\n    inbox_messages_subject_christmas = imbox.messages(subject='Christmas')\n\n    # Messages whose UID is greater than 1050\n    inbox_messages_uids_greater_than_1050 = imbox.messages(uid__range='1050:*')\n\n    # Messages from a specific folder\n    messages_in_folder_social = imbox.messages(folder='Social')\n\n    # Some of Gmail's IMAP Extensions are supported (label and raw):\n    all_messages_with_an_attachment_from_martin = imbox.messages(folder='all', raw='from:martin@amon.cx has:attachment')\n    all_messages_labeled_finance = imbox.messages(folder='all', label='finance')\n\n    for uid, message in all_inbox_messages:\n    # Every message is an object with the following keys\n\n        message.sent_from\n        message.sent_to\n        message.subject\n        message.headers\n        message.message_id\n        message.date\n        message.body.plain\n```\n",
    'author': 'zmcoding',
    'author_email': '841699090@qq.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
