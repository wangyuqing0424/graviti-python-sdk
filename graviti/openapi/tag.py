#!/usr/bin/env python3
#
# Copyright 2022 Graviti. Licensed under MIT License.
#

"""Interfaces about the tag."""

from typing import Any, Dict
from urllib.parse import urljoin

from graviti.openapi.requests import open_api_do


def create_tag(
    access_key: str, url: str, owner: str, dataset: str, *, name: str, revision: str
) -> Dict[str, str]:
    """Execute the OpenAPI `POST /v2/datasets/{owner}/{dataset}/tags`.

    Arguments:
        access_key: User's access key.
        url: The URL of the graviti website.
        owner: The owner of the dataset.
        dataset: Name of the dataset, unique for a user.
        name: The tag name to be created for the specific commit.
        revision: The information to locate the specific commit, which can be the commit id,
            the branch name, or the tag name.

    Returns:
        The response of OpenAPI.

    Examples:
        >>> create_tag(
        ...     "ACCESSKEY-********",
        ...     "https://api.graviti.com/",
        ...     "czhual",
        ...     "MNIST",
        ...     name="tag-2",
        ...     revision="986d8ea00da842ed85dd5d5cd14b5aef"
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
    url = urljoin(url, f"v2/datasets/{owner}/{dataset}/tags")
    post_data = {"name": name, "revision": revision}
    return open_api_do(  # type: ignore[no-any-return]
        "POST", access_key, url, json=post_data
    ).json()


def list_tags(
    access_key: str,
    url: str,
    owner: str,
    dataset: str,
    *,
    offset: int = 0,
    limit: int = 128,
) -> Dict[str, Any]:
    """Execute the OpenAPI `GET /v2/datasets/{owner}/{dataset}/tags`.

    Arguments:
        access_key: User's access key.
        url: The URL of the graviti website.
        owner: The owner of the dataset.
        dataset: Name of the dataset, unique for a user.
        offset: The offset of the page.
        limit: The limit of the page.

    Returns:
        The response of OpenAPI.

    Examples:
        >>> list_tags(
        ...     "ACCESSKEY-********",
        ...     "https://api.graviti.com/",
        ...     "czhual",
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
    url = urljoin(url, f"v2/datasets/{owner}/{dataset}/tags")
    params = {"offset": offset, "limit": limit}
    return open_api_do("GET", access_key, url, params=params).json()  # type: ignore[no-any-return]


def get_tag(access_key: str, url: str, dataset: str, owner: str, *, tag: str) -> Dict[str, str]:
    """Execute the OpenAPI `GET /v2/datasets/{owner}/{dataset}/tags/{tag}`.

    Arguments:
        access_key: User's access key.
        url: The URL of the graviti website.
        owner: The owner of the dataset.
        dataset: Name of the dataset, unique for a user.
        tag: The name of the tag to be got.

    Returns:
        The response of OpenAPI.

    Examples:
        >>> get_tag(
        ...     "ACCESSKEY-********",
        ...     "https://api.graviti.com/",
        ...     "czhual",
        ...     "MNIST",
        ...     tag="tag-2"
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
    url = urljoin(url, f"v2/datasets/{owner}/{dataset}/tags/{tag}")
    return open_api_do("GET", access_key, url).json()  # type: ignore[no-any-return]


def delete_tag(
    access_key: str,
    url: str,
    owner: str,
    dataset: str,
    *,
    tag: str,
) -> None:
    """Execute the OpenAPI `DELETE /v2/datasets/{owner}/{dataset}/tags/{tag}`.

    Arguments:
        access_key: User's access key.
        url: The URL of the graviti website.
        owner: The owner of the dataset.
        dataset: Name of the dataset, unique for a user.
        tag: The name of the tag to be deleted.

    Examples:
        >>> delete_tag(
        ...     "ACCESSKEY-********",
        ...     "https://api.graviti.com/",
        ...     "czhual",
        ...     "MNIST",
        ...     tag="tag-2"
        ... )

    """
    url = urljoin(url, f"v2/datasets/{owner}/{dataset}/tags/{tag}")
    open_api_do("DELETE", access_key, url)
