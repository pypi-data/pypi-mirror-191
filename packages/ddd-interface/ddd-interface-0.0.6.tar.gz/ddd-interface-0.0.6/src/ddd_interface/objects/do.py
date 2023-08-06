from typing import List, Optional, Dict, Tuple, Union
from pydantic import BaseModel



class DatapipeServerInfoDO(BaseModel):
    id: str
    secret: str
    endpoint: str



class DatapipeDataInfoDO(BaseModel):
    bucket: str
    remote_path: str
    local_path: str
    timeout: int = 3



class ClusterConfigDataDO(BaseModel):
    data_server: DatapipeServerInfoDO
    data: List[DatapipeDataInfoDO]



class ClusterConfigDO(BaseModel):
    cluster_name: str
    region_id: str
    config_data: Optional[ClusterConfigDataDO] = None
    entry_point: Optional[List[str]] = None
    timeout: int = 20



class BootstrapInfoDO(BaseModel):
    cluster_config: ClusterConfigDO
    template: str = 'normal'
    platform: str = 'aliyun'
    patch_setting: Optional[Dict] = None



class RandomTemplateVariablesDO(BaseModel):
    variables: List[str]
    lengths: Optional[List[int]] = None



class FileTemplateVariablesDO(BaseModel):
    variables: Optional[List[str]]
    path: str



class FilesTemplateVariablesDO(BaseModel):
    variables: List[str]
    paths: List[str]