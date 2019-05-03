from lxml import etree

# package modules
from .service import Service
from pyorbit.exception import *

"""
System Service
"""

class System(Service):
    """
    Overview of System Service.

    * :meth:`restart`: Restart device to specified image.

    """

    def restart(self, **kwargs):
        """
        Restarts the device to specified image.

        :param str location:
          Specify the image location (1 or 2) that device should use on restart.

        :param str version:
            Specify the image version that device should use on restart.

        :param str type:
            Specify the image type (active or inactive) that device should use on restart.

        For example::
            sys.restart(location=1)
            sys.restart(version="6.7.8")
            sys.restart(type="inactive")

        :returns:
            True

        :raises: SysRestartError: When device restart fails.
        """

        rpc = None

        if 'location' in kwargs:
            location = kwargs['location']
            if location not in [ 1, 2]:
                raise RuntimeError("Invalid location, should be 1 or 2")

            rpc = """
                <system-restart xmlns="com:gemds:mds-system">
                    <image>{}</image>
                </system-restart>
            """.format (location)

        if 'version' in kwargs:
            version = kwargs['version']

            rpc = """
                <system-restart xmlns="com:gemds:mds-system">
                    <version>{}</version>
                </system-restart>
            """.format (version)

        if 'type' in kwargs:
            type = kwargs['type']

            if type == 'active':
                rpc = """
                    <system-restart xmlns="com:gemds:mds-system">
                        <active/>
                    </system-restart>
                """
            elif type == 'inactive':
                rpc = """
                    <system-restart xmlns="com:gemds:mds-system">
                        <inactive/>
                    </system-restart>
                """
            else:
                raise RuntimeError("Invalid type, should be inactive or active")

        if rpc is None:
            rpc = """
                <system-restart xmlns="com:gemds:mds-system">
                    <active/>
                </system-restart>
            """

        try:
            self.dev._conn.rpc(rpc)
        except Exception as err:
            if hasattr(err, 'xml') and isinstance(err.xml, etree._Element):
                raise FwLoadError(rsp=err.xml)
            else:
                raise
        return True

    def create_snapshot(self, **kwargs):
        """
        Creates config snapshot.

        :param str id:
          Specify the identifer for the snapshot.

        For example::
            sys.create_snapshot(id="TEST")

        :returns:
            True

        :raises: RpcError: On failure.
        """

        rpc = None

        if 'id' in kwargs:
            id = kwargs['id']
        else:
            raise ArgError("id must be specified")

        rpc = """
            <snapshot-create xmlns="com:gemds:mds-system">
                <identifier>{}</identifier>
            </snapshot-create>
        """.format (id)

        try:
            self.dev._conn.rpc(rpc)
        except Exception as err:
            if hasattr(err, 'xml') and isinstance(err.xml, etree._Element):
                raise RpcError(rsp=err.xml)
            else:
                raise
        return True

    def delete_snapshot(self, **kwargs):
        """
        Delete config snapshot.

        :param str id:
          Specify the identifer for the snapshot.

        For example::
            sys.delete_snapshot(id="TEST")

        :returns:
            True

        :raises: RpcError: On failure.
        """

        rpc = None

        if 'id' in kwargs:
            id = kwargs['id']
        else:
            raise ArgError("id must be specified")

        rpc = """
            <snapshot-delete xmlns="com:gemds:mds-system">
                <identifier>{}</identifier>
            </snapshot-delete>
        """.format (id)

        try:
            self.dev._conn.rpc(rpc)
        except Exception as err:
            if hasattr(err, 'xml') and isinstance(err.xml, etree._Element):
                raise RpcError(rsp=err.xml)
            else:
                raise
        return True

    def __init__(self, dev, **kwargs):
        """
        .. code-block:: python

           with System(dev) as sys:
               sys.restart()
        """
        Service.__init__(self, dev=dev)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass
