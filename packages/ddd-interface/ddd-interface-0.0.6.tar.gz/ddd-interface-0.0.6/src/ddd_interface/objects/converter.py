from typing import List, Optional, Dict, Tuple, Union
from ..infrastructure.converter import Converter
from .entity import (
    BootstrapInfo,
    ClusterConfig,
    ClusterConfigData,
    DatapipeDataInfo,
    DatapipeServerInfo,
    FileTemplateVariables,
    FilesTemplateVariables,
    RandomTemplateVariables
)
from .do import (
    BootstrapInfoDO,
    ClusterConfigDO,
    ClusterConfigDataDO,
    DatapipeDataInfoDO,
    DatapipeServerInfoDO,
    FileTemplateVariablesDO,
    FilesTemplateVariablesDO,
    RandomTemplateVariablesDO
)
from .value_obj import (
    UDict,
    UInt,
    UStr
)



class DatapipeServerInfoConverter(Converter):
    def to_entity(self, do: DatapipeServerInfoDO):
        return DatapipeServerInfo(
            id = UStr(do.id),
            secret = UStr(do.secret),
            endpoint = UStr(do.endpoint)
        )
    def to_do(self, x:DatapipeServerInfo):
        return DatapipeServerInfoDO(
            id = x.id.get_value(),
            secret = x.secret.get_value(),
            endpoint = x.endpoint.get_value()
        )
datapipe_server_info_converter=DatapipeServerInfoConverter()



class DatapipeDataInfoConverter(Converter):
    def to_entity(self, do: DatapipeDataInfoDO):
        return DatapipeDataInfo(
            bucket = UStr(do.bucket),
            remote_path = UStr(do.remote_path),
            local_path = UStr(do.local_path),
            timeout = UInt(do.timeout)
        )
    def to_do(self, x:DatapipeDataInfo):
        return DatapipeDataInfoDO(
            bucket = x.bucket.get_value(),
            remote_path = x.remote_path.get_value(),
            local_path = x.local_path.get_value(),
            timeout = x.timeout.get_value()
        )
datapipe_data_info_converter=DatapipeDataInfoConverter()



class ClusterConfigDataConverter(Converter):
    def to_entity(self, do: ClusterConfigDataDO):
        return ClusterConfigData(
            data_server = datapipe_server_info_converter.to_entity(do.data_server),
            data = [datapipe_data_info_converter.to_entity(m) for m in do.data]
        )
    def to_do(self, x:ClusterConfigData):
        return ClusterConfigDataDO(
            data_server = datapipe_server_info_converter.to_do(x.data_server),
            data = [datapipe_data_info_converter.to_do(m) for m in x.data]
        )
cluster_config_data_converter=ClusterConfigDataConverter()



class ClusterConfigConverter(Converter):
    def to_entity(self, do: ClusterConfigDO):
        return ClusterConfig(
            cluster_name = UStr(do.cluster_name),
            region_id = UStr(do.region_id),
            config_data = None if do.config_data is None else cluster_config_data_converter.to_entity(do.config_data),
            entry_point = None if do.entry_point is None else [UStr(m) for m in do.entry_point],
            timeout = UInt(do.timeout)
        )
    def to_do(self, x:ClusterConfig):
        return ClusterConfigDO(
            cluster_name = x.cluster_name.get_value(),
            region_id = x.region_id.get_value(),
            config_data = None if x.config_data is None else cluster_config_data_converter.to_do(x.config_data),
            entry_point = None if x.entry_point is None else [m.get_value() for m in x.entry_point],
            timeout = x.timeout.get_value()
        )
cluster_config_converter=ClusterConfigConverter()



class BootstrapInfoConverter(Converter):
    def to_entity(self, do: BootstrapInfoDO):
        return BootstrapInfo(
            cluster_config = cluster_config_converter.to_entity(do.cluster_config),
            template = UStr(do.template),
            platform = UStr(do.platform),
            patch_setting = None if do.patch_setting is None else UDict(do.patch_setting)
        )
    def to_do(self, x:BootstrapInfo):
        return BootstrapInfoDO(
            cluster_config = cluster_config_converter.to_do(x.cluster_config),
            template = x.template.get_value(),
            platform = x.platform.get_value(),
            patch_setting = None if x.patch_setting is None else x.patch_setting.get_value()
        )
bootstrap_info_converter=BootstrapInfoConverter()



class RandomTemplateVariablesConverter(Converter):
    def to_entity(self, do: RandomTemplateVariablesDO):
        return RandomTemplateVariables(
            variables = [UStr(m) for m in do.variables],
            lengths = None if do.lengths is None else [UInt(m) for m in do.lengths]
        )
    def to_do(self, x:RandomTemplateVariables):
        return RandomTemplateVariablesDO(
            variables = [m.get_value() for m in x.variables],
            lengths = None if x.lengths is None else [m.get_value() for m in x.lengths]
        )
random_template_variables_converter=RandomTemplateVariablesConverter()



class FileTemplateVariablesConverter(Converter):
    def to_entity(self, do: FileTemplateVariablesDO):
        return FileTemplateVariables(
            variables = None if do.variables is None else [UStr(m) for m in do.variables],
            path = UStr(do.path)
        )
    def to_do(self, x:FileTemplateVariables):
        return FileTemplateVariablesDO(
            variables = None if x.variables is None else [m.get_value() for m in x.variables],
            path = x.path.get_value()
        )
file_template_variables_converter=FileTemplateVariablesConverter()



class FilesTemplateVariablesConverter(Converter):
    def to_entity(self, do: FilesTemplateVariablesDO):
        return FilesTemplateVariables(
            variables = [UStr(m) for m in do.variables],
            paths = [UStr(m) for m in do.paths]
        )
    def to_do(self, x:FilesTemplateVariables):
        return FilesTemplateVariablesDO(
            variables = [m.get_value() for m in x.variables],
            paths = [m.get_value() for m in x.paths]
        )
files_template_variables_converter=FilesTemplateVariablesConverter()
