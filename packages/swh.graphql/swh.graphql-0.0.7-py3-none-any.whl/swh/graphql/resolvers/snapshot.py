# Copyright (C) 2022 The Software Heritage developers
# See the AUTHORS file at the top-level directory of this distribution
# License: GNU General Public License version 3, or any later version
# See top-level LICENSE file for more information

from typing import TYPE_CHECKING, Optional, Union

from swh.graphql.errors import NullableObjectError
from swh.graphql.utils import utils
from swh.model.model import CoreSWHID, Snapshot

from .base_connection import BaseConnection, ConnectionData
from .base_node import BaseSWHNode
from .origin import OriginNode
from .visit_status import BaseVisitStatusNode


class BaseSnapshotNode(BaseSWHNode):
    """
    Base resolver for all the snapshot nodes
    """

    def is_type_of(self):
        # is_type_of is required only when resolving a UNION type
        # This is for ariadne to return the right type
        return "Snapshot"


class SnapshotNode(BaseSnapshotNode):
    """
    Node resolver for a snapshot requested directly with its SWHID
    """

    def _get_node_data(self) -> Optional[Snapshot]:
        """ """
        swhid = self.kwargs.get("swhid")
        assert isinstance(swhid, CoreSWHID)
        return self.archive.get_snapshot(snapshot_id=swhid.object_id, verify=True)


class VisitSnapshotNode(BaseSnapshotNode):
    """
    Node resolver for a snapshot requested from a visit-status
    """

    _can_be_null = True
    obj: BaseVisitStatusNode

    def _get_node_data(self):
        if self.obj.snapshotSWHID is None:
            raise NullableObjectError()
        snapshot_id = self.obj.snapshotSWHID.object_id
        return self.archive.get_snapshot(snapshot_id=snapshot_id, verify=False)


class TargetSnapshotNode(BaseSnapshotNode):
    """
    Node resolver for a snapshot requested as a target
    """

    if TYPE_CHECKING:  # pragma: no cover
        from .target import BranchTargetNode

        obj: Union[BranchTargetNode]

    _can_be_null = True

    def _get_node_data(self):
        return self.archive.get_snapshot(snapshot_id=self.obj.target_hash, verify=False)


class OriginSnapshotConnection(BaseConnection):
    """
    Connection resolver for the snapshots in an origin
    """

    obj: OriginNode

    _node_class = BaseSnapshotNode

    def _get_connection_data(self) -> ConnectionData:
        results = self.archive.get_origin_snapshots(self.obj.url)
        snapshots = [
            self.archive.get_snapshot(snapshot_id=snapshot, verify=False)
            for snapshot in results
        ]
        # FIXME, using dummy(local) pagination, move pagination to backend
        # To remove localpagination, just drop the paginated call
        # STORAGE-TODO
        return utils.get_local_paginated_data(
            snapshots, self._get_first_arg(), self._get_after_arg()
        )
