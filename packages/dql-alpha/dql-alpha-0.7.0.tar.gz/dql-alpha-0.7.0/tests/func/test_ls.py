import re
from datetime import datetime
from struct import pack
from time import sleep

import msgpack
import pytest

from dql.cli import index, ls


def test_ls_no_args(cloud_test_catalog, capsys):
    # These tests re-use the same database for better performance
    conn = cloud_test_catalog.catalog.data_storage.db
    conn.execute("DELETE FROM buckets")
    conn.commit()
    src = str(cloud_test_catalog.src).rstrip("/")
    catalog = cloud_test_catalog.catalog
    conf = cloud_test_catalog.client_config
    index([src], catalog=catalog, client_config=conf)
    ls(
        [],
        catalog=catalog,
        client_config=conf,
    )
    captured = capsys.readouterr()
    assert captured.out == f"{src}\n"


def test_ls_root(cloud_test_catalog, capsys):
    src = str(cloud_test_catalog.src).rstrip("/")
    root = src[: src.find("://") + 3]
    src_name = src.replace(root, "", 1)
    ls(
        [root],
        catalog=cloud_test_catalog.catalog,
        client_config=cloud_test_catalog.client_config,
    )
    captured = capsys.readouterr()
    buckets = captured.out.split("\n")
    assert src_name in buckets


ls_sources_output = """\
cats/
dogs/
description

dogs/others:
dog4

dogs:
dog1
dog2
dog3
"""


def test_ls_sources(cloud_test_catalog, capsys):
    src = str(cloud_test_catalog.src).rstrip("/")
    ls(
        [src, f"{src}/dogs/*"],
        catalog=cloud_test_catalog.catalog,
        client_config=cloud_test_catalog.client_config,
    )
    captured = capsys.readouterr()
    assert captured.out == ls_sources_output


def test_ls_not_found(cloud_test_catalog):
    src = str(cloud_test_catalog.src).rstrip("/")
    with pytest.raises(FileNotFoundError):
        ls(
            [src, f"{src}/cats/bogus*"],
            catalog=cloud_test_catalog.catalog,
            client_config=cloud_test_catalog.client_config,
        )


def test_ls_partial_indexing(cloud_test_catalog, capsys):
    # These tests re-use the same database for better performance
    data_storage = cloud_test_catalog.catalog.data_storage
    data_storage.storages.delete()
    src = str(cloud_test_catalog.src).rstrip("/")

    ls(
        [f"{src}/dogs/others/"],
        catalog=cloud_test_catalog.catalog,
        client_config=cloud_test_catalog.client_config,
    )
    # These sleep calls are here to ensure that capsys can fully capture the output
    # and to avoid any flaky tests due to multithreading generating output out of order
    sleep(0.05)
    captured = capsys.readouterr()
    assert data_storage.partials.col("path_str") == ["dogs/others/"]
    assert "Listing" in captured.err
    assert "dog4" in captured.out

    ls(
        [f"{src}/cats/"],
        catalog=cloud_test_catalog.catalog,
        client_config=cloud_test_catalog.client_config,
    )
    sleep(0.05)
    captured = capsys.readouterr()
    assert data_storage.partials.col("path_str") == ["cats/", "dogs/others/"]
    assert "Listing" in captured.err
    assert "cat1\ncat2" in captured.out

    ls(
        [f"{src}/dogs/"],
        catalog=cloud_test_catalog.catalog,
        client_config=cloud_test_catalog.client_config,
    )
    sleep(0.05)
    captured = capsys.readouterr()
    assert data_storage.partials.col("path_str") == ["cats/", "dogs/"]
    assert "Listing" in captured.err
    assert "others/\ndog1\ndog2\ndog3" in captured.out

    ls(
        [f"{src}/cats/"],
        catalog=cloud_test_catalog.catalog,
        client_config=cloud_test_catalog.client_config,
    )
    sleep(0.05)
    captured = capsys.readouterr()
    assert data_storage.partials.col("path_str") == ["cats/", "dogs/"]
    assert "Listing" not in captured.err
    assert "cat1\ncat2" in captured.out

    ls(
        [f"{src}/"],
        catalog=cloud_test_catalog.catalog,
        client_config=cloud_test_catalog.client_config,
    )
    sleep(0.05)
    captured = capsys.readouterr()
    assert data_storage.partials.col("path_str") == []
    assert "Listing" in captured.err
    assert "cats/\ndogs/\ndescription" in captured.out


class MockResponse:
    def __init__(self, content, ok=True):
        self.content = content
        self.ok = ok


def mock_post(url, data=None, json=None, **kwargs):
    source = json["source"]
    path = re.sub(r"\w+://[^/]+/?", "", source).rstrip("/")
    data = [
        {
            **d,
            "path_str": d["path_str"].format(src=path),
            "path": d["path_str"].format(src=path).split("/"),
        }
        for d in REMOTE_DATA[path]
    ]
    return MockResponse(
        content=msgpack.packb({"data": data}, default=_pack_extended_types)
    )


def _pack_extended_types(obj):
    if isinstance(obj, datetime):
        if obj.tzinfo:
            data = (obj.timestamp(), int(obj.utcoffset().total_seconds()))
            return msgpack.ExtType(42, pack("!dl", *data))
        else:
            data = (obj.timestamp(),)
            return msgpack.ExtType(42, pack("!d", *data))
    raise TypeError(f"Unknown type: {type(obj)}")


ls_remote_sources_output = """\
{src}:
cats/
dogs/
description

{src}/dogs/others:
dog4

{src}/dogs:
dog1
dog2
dog3
"""


def test_ls_remote_sources(cloud_type, capsys, monkeypatch):
    src = f"{cloud_type}://bucket"
    token = "35NmrvSlsGVxTYIglxSsBIQHRrMpi6irSSYcAL0flijOytCHc"
    with monkeypatch.context() as m:
        m.setattr("requests.post", mock_post)
        ls(
            [src, f"{src}/dogs/others", f"{src}/dogs"],
            config={
                "type": "http",
                "url": "http://localhost:8111/api/dql",
                "username": "dql-team",
                "token": f"isat_{token}",
            },
        )
    captured = capsys.readouterr()
    assert captured.out == ls_remote_sources_output.format(src=src)


owner_id = "a13a3ff923430363b098ce9c769e450724e74e646332b08ca6b3ac4f96dae083"
REMOTE_DATA = {
    "": [
        {
            "id": 816,
            "dir_type": 1,
            "parent_id": 773,
            "name": "cats",
            "checksum": "",
            "etag": "",
            "version": "",
            "is_latest": True,
            "last_modified": datetime(2023, 1, 17, 21, 39, 0, 88564),
            "size": 0,
            "owner_name": "",
            "owner_id": "",
            "path_str": "{src}/cats",
            "anno": None,
            "path": [],
        },
        {
            "id": 825,
            "dir_type": 1,
            "parent_id": 773,
            "name": "dogs",
            "checksum": "",
            "etag": "",
            "version": "",
            "is_latest": True,
            "last_modified": datetime(2023, 1, 17, 21, 39, 0, 88567),
            "size": 0,
            "owner_name": "",
            "owner_id": "",
            "path_str": "{src}/dogs",
            "anno": None,
            "path": [],
        },
        {
            "id": None,
            "dir_type": 0,
            "parent_id": 773,
            "name": "description",
            "checksum": "",
            "etag": "20664550afa2654017377ceb266a1f82",
            "version": "",
            "is_latest": True,
            "last_modified": datetime(2022, 2, 10, 3, 39, 9),
            "size": 350496,
            "owner_name": "",
            "owner_id": owner_id,
            "path_str": "{src}/description",
            "anno": None,
            "path": [],
        },
    ],
    "dogs/others": [
        {
            "id": None,
            "dir_type": 0,
            "parent_id": 893,
            "name": "dog4",
            "checksum": "",
            "etag": "c4e42ce24d92bb5b4c4be9a99b237502",
            "version": "",
            "is_latest": True,
            "last_modified": datetime(2022, 6, 28, 22, 39, 1),
            "size": 32975,
            "owner_name": "",
            "owner_id": owner_id,
            "path_str": "{src}/dogs/others/dog4",
            "anno": None,
            "path": [],
        },
    ],
    "dogs": [
        {
            "id": None,
            "dir_type": 0,
            "parent_id": 825,
            "name": "dog1",
            "checksum": "",
            "etag": "44a632238558e0aa4c54bdb901bf9cff",
            "version": "",
            "is_latest": True,
            "last_modified": datetime(2022, 6, 28, 22, 39, 1),
            "size": 101,
            "owner_name": "",
            "owner_id": owner_id,
            "path_str": "{src}/dogs/dog1",
            "anno": None,
            "path": [],
        },
        {
            "id": None,
            "dir_type": 0,
            "parent_id": 825,
            "name": "dog2",
            "checksum": "",
            "etag": "76556c960239c50e5a8f8569daf85355",
            "version": "",
            "is_latest": True,
            "last_modified": datetime(2022, 6, 28, 22, 39, 1),
            "size": 29759,
            "owner_name": "",
            "owner_id": owner_id,
            "path_str": "{src}/dogs/dog2",
            "anno": None,
            "path": [],
        },
        {
            "id": None,
            "dir_type": 0,
            "parent_id": 825,
            "name": "dog3",
            "checksum": "",
            "etag": "b1c99fedcf77bf5fa62984e93db1955c",
            "version": "",
            "is_latest": True,
            "last_modified": datetime(2022, 6, 28, 22, 39, 1),
            "size": 102,
            "owner_name": "",
            "owner_id": owner_id,
            "path_str": "{src}/dogs/dog3",
            "anno": None,
            "path": [],
        },
    ],
}
