class Th2GUIReport:
    """Class for creating gui link by event ID or message ID."""

    def __init__(self, provider_link: str):
        """Th2GUIReport constructor.

        Args:
            provider_link (str): link to provider.
        """
        self._provider_link = self.__normalize_link(provider_link)

    def __normalize_link(self, link: str) -> str:
        """Bringing links to a single form.

        Add 'http://' to the beginning of the link.
        Add slash to the ending of link.

        Args:
            link (str): link for editing.

        Returns:
            Normalize link.
        """
        find_http = link.startswith("http", 0)
        if find_http is False:
            link = "http://" + link

        if link[-1] != "/":
            link = link + "/"

        return link

    def get_event_link(self, event_id: str) -> str:
        """Creates the link with event id.

        Args:
            event_id (str): id for adding in link.

        Returns:
            GUI link to event.
        """
        return f"{self._provider_link}?eventId={event_id}"

    def get_message_link(self, message_id: str) -> str:
        """Creates the link with message id.

        Args:
            message_id (str): id for adding in link.

        Returns:
            GUI link to message.
        """
        return f"{self._provider_link}?messageId={message_id}"

    def dict_to_tree_table(self, d: dict, table_name=None):
        """
        Convert dict to tree-table.

        See what is tree-table here:
        https://exactpro.atlassian.net/wiki/spaces/TH2/pages/63766549/rpt-viewer+supported+event+content#Tree-table
        """

        rd = {}
        for k, v in d.items():
            rd[k] = _get_rows_for_tree_table(v)

        return dict(
            type='treeTable',
            name=table_name,
            rows=rd
        )


    def _get_rows_for_tree_table(self, d: dict, _list=False):
        """Protected recursive function for dict_to_tree_table function."""

        rd = {}
        if isinstance(d, dict):
            for k, v in d.items():
                rd[k] = _get_rows_for_tree_table(v)

            if _list:
                return rd
            else:
                return dict(
                    type='collection',
                    rows=rd
                )

        elif isinstance(d, list):
            rows = {}
            for idx, v in enumerate(d):
                rows[idx] = dict(
                    type='collection',
                    rows=_get_rows_for_tree_table(v, _list=True)
                )
            return dict(
                type='collection',
                rows=rows
            )

        elif isinstance(d, (str, int, float, tuple)) or d is None:
            if isinstance(d, tuple):
                columns = {F'col{idx}': v for idx, v in enumerate(d)}
            else:
                columns = {'col1': d}
            return dict(
                type='row',
                columns=columns
            )

        else:
            return _get_rows_for_tree_table(vars(d))
