from typing import Optional, Protocol, Tuple

import sarus_data_spec.typing as st
from sarus_data_spec.manager.typing import Manager


class SDKManager(Manager, Protocol):
    """The Manager of the SDK running on the client side.

    This Manager has two additional functionalities compared to the
    DelegatingManager manager.

    First, it manages the relationship with the remote server using the API
    endpoints.

    Second, this Manager defines a MOCK version for every DataSpec. The MOCK is
    defined as a smaller version of a DataSpec. In practice, it is a sample of
    SYNTHETIC at the source and MOCKs of transformed DataSpecs are the
    transforms of the MOCKs.

    The MOCK is created and its value computed in the `infer_output_type`
    method. This serves two purposes. First, it provides immediate feedback to
    the user in case of erroneous computation. Second, it allows identifying the
    MOCK's value Python type which is then used by the SDK to instantiate the
    correct DataSpecWrapper type (e.g. instantiate a sarus.pandas.DataFrame if
    the value is a pandas.DataFrame).
    """

    def mock(self, dataspec: st.DataSpec) -> st.DataSpec:
        """Returns a mock version of a DataSpec.

        This is a kind of compilation used by this manager to infer the DataSpec type and Python type of an external transform's result.
        """
        ...

    def register_source_mock(self, dataspec: st.DataSpec) -> st.DataSpec:
        """Define what a mock is for source or fetched DataSpecs."""
        ...

    def python_type(self, dataspec: st.DataSpec) -> Optional[str]:
        """Return the Python class name of a DataSpec.

        This is used to instantiate the correct DataSpecWrapper class.
        """
        ...

    def client(self):
        """Return the sarus.Client object used to make API calls."""
        ...

    def _post_dataspec(
        self, dataspec: st.DataSpec, execute: bool = False
    ) -> Tuple[st.DataSpec, str]:
        """Post a dataspec and its graph to the server for execution."""
        ...
