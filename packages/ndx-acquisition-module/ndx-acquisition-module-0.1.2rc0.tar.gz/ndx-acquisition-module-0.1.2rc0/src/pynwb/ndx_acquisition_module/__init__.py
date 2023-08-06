import os

from hdmf.common import DynamicTable
from hdmf.utils import docval, get_docval, popargs
from pynwb.core import NWBDataInterface
from pynwb.file import MultiContainerInterface
from pynwb.io.core import NWBContainerMapper

from pynwb import get_class, load_namespaces, register_class, register_map

namespace_name = "ndx-acquisition-module"

# Set path of the namespace file to the expected install location
# If the extension has not been installed yet but we are running directly from
# the git repo

namespace_path = os.path.join("spec", namespace_name + ".namespace.yaml")
initfile_path = os.path.dirname(__file__)

namespace_path = os.path.join(initfile_path, namespace_path)
if not os.path.exists(namespace_path):
    namespace_path = os.path.abspath(
        os.path.join(initfile_path, "..", "..", "..", namespace_path)
    )

# Load the namespace
load_namespaces(namespace_path)

# Create API
# very similar to how ProcessingModule is created

AcquisitionModule = get_class("AcquisitionModule", namespace_name)
init_docval = get_docval(AcquisitionModule.__init__, "name", "description")


@register_class("AcquisitionModule", namespace_name)
class AcquisitionModule(MultiContainerInterface):
    __clsconf__ = [
        {
            "attr": "data_interfaces",
            "add": "add",
            "type": (NWBDataInterface, DynamicTable),
            "get": "get",
        }
    ]

    @docval(
        # obtain docval from namespace
        *init_docval,
        {
            "name": "data_interfaces",
            "doc": "NWBDataInterface",
            "type": (list, tuple, dict, NWBDataInterface, DynamicTable),
            "default": None,
        },
    )
    def __init__(self, **kwargs):
        description, data_interfaces = popargs("description", "data_interfaces", kwargs)
        super().__init__(**kwargs)
        self.description = description
        self.data_interfaces = data_interfaces


@register_map(AcquisitionModule)
class ModuleMap(NWBContainerMapper):
    def __init__(self, spec):
        super().__init__(spec)
        containers_spec = self.spec.get_neurodata_type("NWBDataInterface")
        table_spec = self.spec.get_neurodata_type("DynamicTable")
        self.map_spec("data_interfaces", containers_spec)
        self.map_spec("data_interfaces", table_spec)

    @NWBContainerMapper.constructor_arg("name")
    def name(self, builder, manager):
        return builder.name
