# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['bitcoin_message_tool']

package_data = \
{'': ['*']}

install_requires = \
['base58>=2.1.1,<3.0.0',
 'bech32>=1.2.0,<2.0.0',
 'pytest>=7.2.1,<8.0.0',
 'ripemd-hash>=1.0.0,<2.0.0']

entry_points = \
{'console_scripts': ['bmt = bitcoin_message_tool.bmt:main']}

setup_kwargs = {
    'name': 'bitcoin-message-tool',
    'version': '0.1.4',
    'description': 'Bitcoin message signing/verification tool',
    'long_description': 'Bitcoin Message Tool\n======\n\nBitcoin Message Tool\n\nA lightweight CLI tool for signing and verification of bitcoin messages.\nBitcoin message is the most straightforward and natural way to prove ownership over\na given address without revealing any confidential information.\n\nThis tool closely follows specification described in BIP137:\n\nPlease note that "since this format includes P2PKH keys, it is backwards compatible, \nbut keep in mind some software has checks for ranges of headers and will report the newer \nsegwit header types as errors."\n\nMore info: https://github.com/bitcoin/bips/blob/master/bip-0137.mediawiki\n\nInstallation\n------------\n\nTo install with pip, run:\n\n    pip install bitcoin-message-tool\n\nQuickstart Guide\n----------------\n\n    Usage:\n\n    python -m bitcoin_message_tool -h\n\n    or\n\n    python bmt.py -h\n    usage: python3 bmt.py [-h] {sign,verify} ...\n\n    Bitcoin message signing/verification tool\n\n    positional arguments:\n    {sign,verify}\n\n    options:\n    -h, --help     show this help message and exit\n\nMessage signing:\n\n    python bmt.py sign -h\n    usage: python3 <application> sign [-h] -p -a {p2pkh,p2wpkh-p2sh,p2wpkh} -m [MESSAGE ...] [-d] [-e] [-v]\n\n    options:\n    -h, --help            show this help message and exit\n\n    Sign messsage:\n    -p, --privkey         private key in wallet import format (WIF)\n    -a {p2pkh,p2wpkh-p2sh,p2wpkh}, --addr_type {p2pkh,p2wpkh-p2sh,p2wpkh}\n                            type of bitcoin address\n    -m [MESSAGE ...], --message [MESSAGE ...]\n                            Message to sign\n    -d, --deterministic   sign deterministtically (RFC6979)\n    -e, --electrum        create Electrum-like signature\n    -v, --verbose         print prettified message\n\nExample 1:\nNon-deterministic signature for compressed private key and p2pkh address\n\n    $python bmt.py sign -p -a p2pkh -m ECDSA is the most fun I have ever experienced\n\n    PrivateKey(WIF): <insert private key here>\n\nOutput:\n\n    Bitcoin address: 175A5YsPUdM71mnNCC3i8faxxYJgBonjWL\n    Message: ECDSA is the most fun I have ever experienced\n    Signature: IBuc5GXSJCr6m7KevsBAoCiX8ToOjW2CDZMr6PCEbiHwQJ237LZTj/REbDHI1/yelY6uBWEWXiOWoGnajlgvO/A=\n\nExample 2:\nDeterministic signature for compressed private key and p2pkh address\n\n    $python bmt.py sign -p -a p2pkh -m ECDSA is the most fun I have ever experienced -d\n\n    PrivateKey(WIF): <insert private key here>\n\nOutput:\n\n    Bitcoin address: 175A5YsPUdM71mnNCC3i8faxxYJgBonjWL\n    Message: ECDSA is the most fun I have ever experienced\n    Signature: HyiLDcQQ1p2bKmyqM0e5oIBQtKSZds4kJQ+VbZWpr0kYA6Qkam2MlUeTr+lm1teUGHuLapfa43JjyrRqdSA0pxs=\n\nExample 3:\nDeterministic signature for compressed private key and p2pkh address (verbose mode)\n\n    $python bmt.py sign -p -a p2pkh -m ECDSA is the most fun I have ever experienced -d -v\n\n    PrivateKey(WIF): <insert private key here>\n\nOutput:\n\n    -----BEGIN BITCOIN SIGNED MESSAGE-----\n    ECDSA is the most fun I have ever experienced\n    -----BEGIN BITCOIN SIGNATURE-----\n    175A5YsPUdM71mnNCC3i8faxxYJgBonjWL\n\n    HyiLDcQQ1p2bKmyqM0e5oIBQtKSZds4kJQ+VbZWpr0kYA6Qkam2MlUeTr+lm1teUGHuLapfa43JjyrRqdSA0pxs=\n    -----END BITCOIN SIGNATURE-----\n\nExample 4:\nUncompressed private keys can\'t produce addresses other than \'p2pkh\'\n\n    python bmt.py sign -p -m ECDSA is the most fun I have ever experienced -a \'p2wpkh\'  -d -v\n\n    PrivateKey(WIF): <insert private key here>\n\nOutput:\n\n    Traceback (most recent call last):\n    ...\n    PrivateKeyError: (\'Need WIF-compressed private key for this address type:\', \'p2wpkh\')\n\nMessage verification:\n\n    python bmt.py verify -h\n    usage: python3 <application> verify [-h] -a ADDRESS -m [MESSAGE ...] -s SIGNATURE [-e] [-v] [-r]\n\n    options:\n    -h, --help            show this help message and exit\n\n    Verify messsage:\n    -a ADDRESS, --address ADDRESS\n                            specify bitcoin address\n    -m [MESSAGE ...], --message [MESSAGE ...]\n                            Message to verify\n    -s SIGNATURE, --signature SIGNATURE\n                            bitcoin signature in base64 format\n    -e, --electrum        verify Electrum-like signature\n    -v, --verbose         print full message\n    -r, --recpub          recover public key\n\nExample 1:\nStandard message verification\n\n    python bmt.py verify -a 175A5YsPUdM71mnNCC3i8faxxYJgBonjWL \\\n    > -m ECDSA is the most fun I have ever experienced \\\n    > -s HyiLDcQQ1p2bKmyqM0e5oIBQtKSZds4kJQ+VbZWpr0kYA6Qkam2MlUeTr+lm1teUGHuLapfa43JjyrRqdSA0pxs=\n\nOutput:\n\n    True\n\nExample 2:\nMessage verification in verbose mode\n\n    python bmt.py verify -a 175A5YsPUdM71mnNCC3i8faxxYJgBonjWL \\\n    > -m ECDSA is the most fun I have ever experienced \\\n    > -s HyiLDcQQ1p2bKmyqM0e5oIBQtKSZds4kJQ+VbZWpr0kYA6Qkam2MlUeTr+lm1teUGHuLapfa43JjyrRqdSA0pxs= \\\n    > -v\n\nOutput:\n\n    True\n    Message verified to be from 175A5YsPUdM71mnNCC3i8faxxYJgBonjWL\n\nExample 3:\nDisplay a recovered public key\n\n    python bmt.py verify -a 175A5YsPUdM71mnNCC3i8faxxYJgBonjWL \\\n    > -m ECDSA is the most fun I have ever experienced \\\n    > -s HyiLDcQQ1p2bKmyqM0e5oIBQtKSZds4kJQ+VbZWpr0kYA6Qkam2MlUeTr+lm1teUGHuLapfa43JjyrRqdSA0pxs= \\\n    > --recpub\n\nOutput:\n\n    True\n    024aeaf55040fa16de37303d13ca1dde85f4ca9baa36e2963a27a1c0c1165fe2b1\n\nExample 4:\nError message\n\n    python bmt.py verify -a 175A5YsPUdM71mnNCC3i8faxxYJgBonjWL \\\n    > -m ECDSA is the most fun I have ever experienced \\\n    > -s HyiLDcQQ1p2bKmyqM0e5oIBQtKSZds4kJQ+VbZWpr0kYA6Qkam2MlUeTr+lm1teUGHuLaffa43Jj= -v -r \\\n\nOutput:\n\n    Traceback (most recent call last):\n    ...\n    SignatureError: (\'Signature must be 65 bytes long:\', 57)\n\nContribute\n----------\n\nIf you\'d like to contribute to bitcoin_message_signer, check out https://github.com/shadowy-pycoder/bitcoin_message_tool\n',
    'author': 'shadowy-pycoder',
    'author_email': 'shadowy-pycoder@example.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
