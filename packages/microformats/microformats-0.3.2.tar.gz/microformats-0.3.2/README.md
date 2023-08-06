[microformats][0] are the simplest way to openly publish contacts, events,
reviews, recipes, and other structured information on the web.

>>> import mf
>>> url = "https://alice.example"
>>> doc = mf.parse(doc=f'''
... <p class=h-card><a href={url}>Alice</a></p>
... <ul class=h-feed>
... <li class=h-entry>foo
... <li class=h-entry>bar
... </ul>
... ''', url=url)

# >>> dict(doc)
# >>> doc.json

>>> card = doc["items"][0]
>>> card["type"]
['h-card']
>>> card["properties"]
{'name': ['Alice'], 'url': ['https://alice.example']}
>>> feed = doc["items"][1]
>>> feed["children"][0]["properties"]["name"]
['foo']

>>> mf.util.representative_card(doc, url)
{'name': ['Alice'], 'url': ['https://alice.example']}
>>> mf.util.representative_feed(doc, url)["items"][0]["name"]
['foo']

Based upon [`mf2py`][1] and [`mf2util`][2].

# TODO >>> doc.representative_card
# TODO {'name': ['Alice'], 'url': ['https://alice.example']}
# TODO >>> doc.representative_feed["items"][0]["name"]
# TODO ['foo']

[0]: https://microformats.org/wiki/microformats
[1]: https://github.com/microformats/mf2py
[1]: https://github.com/kylewm/mf2util

## Fork

### mf2py

Started with commit:
https://github.com/microformats/mf2py/commit/27f13087c1e0060381de9035280d56af5dad8649

Tom Morris <tom@tommorris.org> <https://tommorris.org>
Barnaby Walters <https://waterpigs.co.uk>
Kartik Prabhu <me@kartikprabhu.com> <https://kartikprabhu.com>
Kyle Mahan <kyle@kylewm.com> <https://kylewm.com>
Kevin Marks <kevinmarks@gmail.com> <https://www.kevinmarks.com>

Copyight (c) 2013, 2014 Tom Morris and contributors

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.

### mf2util

Started with commit:
https://github.com/kylewm/mf2util/commit/b1acda62ea5b0d500dc5a6770b2c681825a01e41

Copyright (c) 2014 Kyle Mahan

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are
met:

1. Redistributions of source code must retain the above copyright
   notice, this list of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright
   notice, this list of conditions and the following disclaimer in the
   documentation and/or other materials provided with the
   distribution.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
"AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
