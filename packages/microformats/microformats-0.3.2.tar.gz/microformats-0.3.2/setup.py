# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mf', 'mf.parser', 'mf.parser.backcompat', 'mf.parser.prop_util']

package_data = \
{'': ['*']}

install_requires = \
['beautifulsoup4>=4.11.2,<5.0.0',
 'easyuri>=0.1.2',
 'html5lib>=1.1,<2.0',
 'requests>=2.28.2,<3.0.0',
 'txtint>=0.1.2']

entry_points = \
{'console_scripts': ['mf = mf:main']}

setup_kwargs = {
    'name': 'microformats',
    'version': '0.3.2',
    'description': 'tools for Microformats production, consumption and analysis',
    'long_description': '[microformats][0] are the simplest way to openly publish contacts, events,\nreviews, recipes, and other structured information on the web.\n\n>>> import mf\n>>> url = "https://alice.example"\n>>> doc = mf.parse(doc=f\'\'\'\n... <p class=h-card><a href={url}>Alice</a></p>\n... <ul class=h-feed>\n... <li class=h-entry>foo\n... <li class=h-entry>bar\n... </ul>\n... \'\'\', url=url)\n\n# >>> dict(doc)\n# >>> doc.json\n\n>>> card = doc["items"][0]\n>>> card["type"]\n[\'h-card\']\n>>> card["properties"]\n{\'name\': [\'Alice\'], \'url\': [\'https://alice.example\']}\n>>> feed = doc["items"][1]\n>>> feed["children"][0]["properties"]["name"]\n[\'foo\']\n\n>>> mf.util.representative_card(doc, url)\n{\'name\': [\'Alice\'], \'url\': [\'https://alice.example\']}\n>>> mf.util.representative_feed(doc, url)["items"][0]["name"]\n[\'foo\']\n\nBased upon [`mf2py`][1] and [`mf2util`][2].\n\n# TODO >>> doc.representative_card\n# TODO {\'name\': [\'Alice\'], \'url\': [\'https://alice.example\']}\n# TODO >>> doc.representative_feed["items"][0]["name"]\n# TODO [\'foo\']\n\n[0]: https://microformats.org/wiki/microformats\n[1]: https://github.com/microformats/mf2py\n[1]: https://github.com/kylewm/mf2util\n\n## Fork\n\n### mf2py\n\nStarted with commit:\nhttps://github.com/microformats/mf2py/commit/27f13087c1e0060381de9035280d56af5dad8649\n\nTom Morris <tom@tommorris.org> <https://tommorris.org>\nBarnaby Walters <https://waterpigs.co.uk>\nKartik Prabhu <me@kartikprabhu.com> <https://kartikprabhu.com>\nKyle Mahan <kyle@kylewm.com> <https://kylewm.com>\nKevin Marks <kevinmarks@gmail.com> <https://www.kevinmarks.com>\n\nCopyight (c) 2013, 2014 Tom Morris and contributors\n\nPermission is hereby granted, free of charge, to any person obtaining a copy\nof this software and associated documentation files (the "Software"), to deal\nin the Software without restriction, including without limitation the rights\nto use, copy, modify, merge, publish, distribute, sublicense, and/or sell\ncopies of the Software, and to permit persons to whom the Software is\nfurnished to do so, subject to the following conditions:\n\nThe above copyright notice and this permission notice shall be included in\nall copies or substantial portions of the Software.\n\nTHE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR\nIMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,\nFITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE\nAUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER\nLIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,\nOUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN\nTHE SOFTWARE.\n\n### mf2util\n\nStarted with commit:\nhttps://github.com/kylewm/mf2util/commit/b1acda62ea5b0d500dc5a6770b2c681825a01e41\n\nCopyright (c) 2014 Kyle Mahan\n\nRedistribution and use in source and binary forms, with or without\nmodification, are permitted provided that the following conditions are\nmet:\n\n1. Redistributions of source code must retain the above copyright\n   notice, this list of conditions and the following disclaimer.\n\n2. Redistributions in binary form must reproduce the above copyright\n   notice, this list of conditions and the following disclaimer in the\n   documentation and/or other materials provided with the\n   distribution.\n\nTHIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS\n"AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT\nLIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR\nA PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT\nHOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,\nSPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT\nLIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,\nDATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY\nTHEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT\n(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE\nOF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.\n',
    'author': 'Angelo Gladding',
    'author_email': 'angelo@ragt.ag',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://ragt.ag/code/python-microformats',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<3.11',
}


setup(**setup_kwargs)
