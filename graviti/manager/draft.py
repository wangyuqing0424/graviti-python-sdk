#!/usr/bin/env python3
#
# Copyright 2022 Graviti. Licensed under MIT License.
#

"""The implementation of the Draft and DraftManager."""

from typing import TYPE_CHECKING, Generator, Optional

from graviti.manager.lazy import LazyPagingList
from graviti.manager.sheets import Sheets
from graviti.openapi import create_draft, get_draft, list_drafts, update_draft

if TYPE_CHECKING:
    from graviti.manager.dataset import Dataset


class Draft(Sheets):  # pylint: disable=too-many-instance-attributes
    """The basic structure of the Graviti draft.

    Arguments:
        dataset: Class :class:`~graviti.dataset.dataset.Dataset` instance.
        number: The number of the draft.
        title: The title of the draft.
        branch_name: The branch name.
        state: The draft state which includes "OPEN", "CLOSED", "COMMITTED".
        parent_commit_id: The parent commit id.
        creator: The creator of the draft.
        created_at: The time when the draft is created.
        updated_at: The time of last update.
        description: The draft description.

    """

    def __init__(
        self,
        dataset: "Dataset",
        number: int,
        *,
        title: str,
        branch: str,
        state: str,
        parent_commit_id: str,
        creator: str,
        created_at: str,
        updated_at: str,
        description: str = "",
    ) -> None:
        self._dataset = dataset
        self.number = number
        self.title = title
        self.branch = branch
        self.state = state
        self.parent_commit_id = parent_commit_id
        self.creator = creator
        self.created_at = created_at
        self.updated_at = updated_at
        self.description = description

    def edit(self, title: Optional[str] = None, description: Optional[str] = None) -> None:
        """Update title and description of the draft.

        Arguments:
            title: The title of the draft.
            description: The description of the draft.

        """
        update_draft(
            self._dataset.access_key,
            self._dataset.url,
            self._dataset.owner,
            self._dataset.name,
            draft_number=self.number,
            title=title,
            description=description,
        )
        if title is not None:
            self.title = title
        if description is not None:
            self.description = description
        # TODO: update the draft.updated_at

    def close(self) -> None:
        """Close the draft."""
        update_draft(
            self._dataset.access_key,
            self._dataset.url,
            self._dataset.owner,
            self._dataset.name,
            draft_number=self.number,
            state="CLOSED",
        )
        self.state = "CLOSED"
        # TODO: update the draft.updated_at

    def commit(self, title: str, description: str = "") -> None:
        """Commit the current draft.

        Arguments:
            title: The commit title.
            description: The commit description.

        """

    def upload(self, jobs: int = 1) -> None:
        """Upload the local dataset to Graviti.

        Arguments:
            jobs: The number of the max workers in multi-thread upload.

        """


class DraftManager:
    """This class defines the operations on the draft in Graviti.

    Arguments:
        dataset: :class:`~graviti.manager.dataset.Dataset` instance.

    """

    def __init__(self, dataset: "Dataset") -> None:
        self._dataset = dataset

    def _generate(
        self,
        state: Optional[str] = None,
        branch: Optional[str] = None,
        offset: int = 0,
        limit: int = 128,
    ) -> Generator[Draft, None, int]:
        response = list_drafts(
            self._dataset.access_key,
            self._dataset.url,
            self._dataset.owner,
            self._dataset.name,
            state=state,
            branch=branch,
            offset=offset,
            limit=limit,
        )

        for item in response["drafts"]:
            yield Draft(self._dataset, **item)

        return response["totalCount"]  # type: ignore[no-any-return]

    def create(
        self, title: str, description: Optional[str] = None, branch: Optional[str] = None
    ) -> Draft:
        """Create a draft.

        Arguments:
            title: The draft title.
            description: The draft description.
            branch: The branch name.

        Returns:
            The :class:`.Draft` instance with the given title and description.

        """
        response = create_draft(
            self._dataset.access_key,
            self._dataset.url,
            self._dataset.owner,
            self._dataset.name,
            title=title,
            branch=branch,
            description=description,
        )
        return Draft(self._dataset, **response)

    def get(self, draft_number: int) -> Draft:
        """Get the certain draft with the given draft number.

        Arguments:
            draft_number: The required draft number.

        Returns:
            The :class:`.Draft` instance with the given number.

        """
        response = get_draft(
            self._dataset.access_key,
            self._dataset.url,
            self._dataset.owner,
            self._dataset.name,
            draft_number=draft_number,
        )
        return Draft(self._dataset, **response)

    def list(
        self, state: Optional[str] = None, branch: Optional[str] = None
    ) -> LazyPagingList[Draft]:
        """List all the drafts.

        Arguments:
            state: The draft state which includes "OPEN", "CLOSED", "COMMITTED", "ALL" and None.
                    None means listing open drafts.
            branch: The branch name. None means listing drafts from all branches.

        Returns:
            The LazyPagingList of :class:`drafts<.Draft>` instances.

        """
        return LazyPagingList(
            lambda offset, limit: self._generate(state, branch, offset, limit),
            128,
        )
