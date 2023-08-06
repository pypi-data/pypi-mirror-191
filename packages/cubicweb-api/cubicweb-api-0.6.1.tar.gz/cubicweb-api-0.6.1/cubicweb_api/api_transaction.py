# copyright 2022 LOGILAB S.A. (Paris, FRANCE), all rights reserved.
# contact https://www.logilab.fr -- mailto:contact@logilab.fr
#
# This program is free software: you can redistribute it and/or modify it under
# the terms of the GNU Lesser General Public License as published by the Free
# Software Foundation, either version 2.1 of the License, or (at your option)
# any later version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU Lesser General Public License for more
# details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.
from typing import cast, Dict

from cubicweb.entities.authobjs import CWUser
from cubicweb.server.repository import Repository
from cubicweb.server.session import Connection


class ApiTransaction:
    def __init__(self, repo: Repository, user: CWUser):
        """
        Class defining transactions.
        A transaction allows to make several request which only take effect
        when the changes are committed.

        :param repo: The CubicWeb repository
        :param user: The user initiating the transaction
        """
        self.cnx = Connection(repo, user)
        self.cnx.__enter__()
        self._uuid = cast(str, self.cnx.transaction_uuid(set=True))

    @property
    def uuid(self) -> str:
        """
        :return: The unique identifier for this transaction
        """
        return self._uuid

    def execute(self, rql: str, params: Dict[str, any]):
        """
        Executes the given rql query on this transaction.

        :param rql: The RQL query string
        :param params: The parameters for the RQL query
        :return: The result from executing the query
        """
        return self.cnx.execute(rql, params)

    def commit(self):
        """
        Commits the current transaction to apply all changes.
        """
        self.cnx.commit()

    def rollback(self):
        """
        Rollback the current transaction to cancel all changes.
        """
        self.cnx.rollback()

    def end(self):
        self.cnx.__exit__(None, None, None)


class ApiTransactionsRepository:
    def __init__(self, repo: Repository):
        """
        Class holding all active transactions from all users.

        :param repo: The CubicWeb repository
        """
        self._transactions: Dict[str, ApiTransaction] = dict()
        self._repo = repo

    def begin_transaction(self, user: CWUser) -> str:
        """
        Starts a new transaction for the given user.

        :param user: The user initiating the transaction
        :return: The transaction uuid
        """
        transaction = ApiTransaction(self._repo, user)
        self._transactions[transaction.uuid] = transaction
        return transaction.uuid

    def end_transaction(self, uuid: str):
        """
        Ends a transaction identified by its uuid.

        :param uuid: The id of the transaction to end.
        """
        transaction = self._transactions.pop(uuid)
        transaction.end()

    def __getitem__(self, uuid: str) -> ApiTransaction:
        return self._transactions[uuid]
