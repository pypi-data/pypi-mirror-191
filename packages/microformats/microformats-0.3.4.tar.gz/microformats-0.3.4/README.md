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

    # TODO >>> dict(doc)
    # TODO >>> doc.json

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

    # TODO >>> doc.representative_card
    # TODO {'name': ['Alice'], 'url': ['https://alice.example']}
    # TODO >>> doc.representative_feed["items"][0]["name"]
    # TODO ['foo']

Based upon [`mf2py`][1] and [`mf2util`][2].

[0]: https://microformats.org/wiki/microformats
[1]: https://github.com/microformats/mf2py
[2]: https://github.com/kylewm/mf2util
