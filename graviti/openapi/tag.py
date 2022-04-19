#!/usr/bin/env python3
#
# Copyright 2022 Graviti. Licensed under MIT License.
#

"""Interfaces about the tag."""

from typing import Any, Dict
from urllib.parse import urljoin

from graviti.openapi.request import open_api_do


def create_tag(url: str, access_key: str, dataset: str, name: str, revision: str) -> None:
    """Execute the OpenAPI `POST /v2/datasets/{dataset}/tags`.

    Arguments:
        url: The URL of the graviti website.
        access_key: User's access key.
        dataset: Name of the dataset, unique for a user.
        name: The tag name to be created for the specific commit.
        revision: The information to locate the specific commit, which can be the commit id,
            the branch name, or the tag name.

    Examples:
        >>> create_tag(
        ...     "https://api.graviti.com/",
        ...     "ACCESSKEY-********",
        ...     "MNIST",
        ...     "tag-2",
        ...     "986d8ea00da842ed85dd5d5cd14b5aef"
        ... )

    """
    url = urljoin(url, f"v2/datasets/{dataset}/tags")
    post_data = {"name": name, "revision": revision}
    open_api_do("POST", access_key, url, json=post_data)


def list_tags(
    url: str,
    access_key: str,
    dataset: str,
    *,
    offset: int = 0,
    limit: int = 128,
) -> Dict[str, Any]:
    """Execute the OpenAPI `GET /v2/datasets/{dataset}/tags`.

    Arguments:
        url: The URL of the graviti website.
        access_key: User's access key.
        dataset: Name of the dataset, unique for a user.
        offset: The offset of the page.
        limit: The limit of the page.

    Returns:
        The response of OpenAPI.

    Examples:
        >>> list_tags(
        ...     "https://api.graviti.com/",
        ...     "ACCESSKEY-********",
        ...     "MNIST"
        ... )
        {
           "tags": [
               {
                   "name": "tag-2",
                   "commit_id": "986d8ea00da842ed85dd5d5cd14b5aef",
                   "parent_commit_id": "a0d4065872f245e4ad1d0d1186e3d397",
                   "title": "commit-1",
                   "description": "",
                   "committer": "czhual",
                   "committed_at": "2021-03-03T18:58:10Z"
               }
           ],
           "offset": 0,
           "record_size": 1,
           "total_count": 1
        }

    """
    url = urljoin(url, f"v2/datasets/{dataset}/tags")
    params = {"offset": offset, "limit": limit}
    return open_api_do("GET", access_key, url, params=params).json()  # type: ignore[no-any-return]


def get_tag(url: str, access_key: str, dataset: str, tag: str) -> Dict[str, str]:
    """Execute the OpenAPI `GET /v2/datasets/{dataset}/tags/{tag}`.

    Arguments:
        url: The URL of the graviti website.
        access_key: User's access key.
        dataset: Name of the dataset, unique for a user.
        tag: The name of the tag to be got.

    Returns:
        The response of OpenAPI.

    Examples:
        >>> get_tag(
        ...     "https://api.graviti.com/",
        ...     "ACCESSKEY-********",
        ...     "MNIST",
        ...     "tag-2"
        ... )
        {
           "name": "tag-2",
           "commit_id": "986d8ea00da842ed85dd5d5cd14b5aef",
           "parent_commit_id": "a0d4065872f245e4ad1d0d1186e3d397",
           "title": "commit-1",
           "description": "",
           "committer": "czhual",
           "committed_at": "2021-03-03T18:58:10Z"
        }

    """
    url = urljoin(url, f"v2/datasets/{dataset}/tags/{tag}")
    return open_api_do("GET", access_key, url).json()  # type: ignore[no-any-return]


def delete_tag(
    url: str,
    access_key: str,
    dataset: str,
    tag: str,
) -> None:
    """Execute the OpenAPI `DELETE /v2/datasets/{dataset}/tags/{tag}`.

    Arguments:
        url: The URL of the graviti website.
        access_key: User's access key.
        dataset: Name of the dataset, unique for a user.
        tag: The name of the tag to be deleted.

    Examples:
        >>> delete_tag(
        ...     "https://api.graviti.com/",
        ...     "ACCESSKEY-********",
        ...     "MNIST",
        ...     "tag-2"
        ... )

    """
    url = urljoin(url, f"v2/datasets/{dataset}/tags/{tag}")
    open_api_do("DELETE", access_key, url)
