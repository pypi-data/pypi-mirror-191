# Copyright (C) 2022 The Software Heritage developers
# See the AUTHORS file at the top-level directory of this distribution
# License: GNU General Public License version 3, or any later version
# See top-level LICENSE file for more information

from typing import TYPE_CHECKING, Optional, Union

from swh.model.model import Directory

from .base_node import BaseSWHNode


class BaseDirectoryNode(BaseSWHNode):
    """
    Base resolver for all the directory nodes
    """

    def is_type_of(self):
        return "Directory"


class DirectoryNode(BaseDirectoryNode):
    """
    Node resolver for a directory requested directly with its SWHID
    """

    def _get_node_data(self):
        swhid = self.kwargs.get("swhid")
        return self.archive.get_directory(directory_id=swhid.object_id, verify=True)


class TargetDirectoryNode(BaseDirectoryNode):
    """
    Node resolver for a directory requested as a target
    """

    if TYPE_CHECKING:  # pragma: no cover
        from .target import BranchTargetNode, TargetNode

        obj: Union[
            BranchTargetNode,
            TargetNode,
        ]
    _can_be_null = True

    def _get_node_data(self) -> Optional[Directory]:
        # existing directory in the archive, hence verify is False
        return self.archive.get_directory(
            directory_id=self.obj.target_hash, verify=False
        )
