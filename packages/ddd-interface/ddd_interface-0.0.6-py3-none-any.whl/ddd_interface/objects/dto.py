from typing import List, Optional, Dict, Tuple, Union
from pydantic import BaseModel



class DatapipeServerInfoDTO(BaseModel):
    id: str
    secret: str
    endpoint: str



class DatapipeDataInfoDTO(BaseModel):
    bucket: str
    remote_path: str
    local_path: str
    timeout: int = 3



class ClusterConfigDataDTO(BaseModel):
    data_server: DatapipeServerInfoDTO
    data: List[DatapipeDataInfoDTO]



class ClusterConfigDTO(BaseModel):
    cluster_name: str
    region_id: str
    config_data: Optional[ClusterConfigDataDTO] = None
    entry_point: Optional[List[str]] = None
    timeout: int = 20



class BootstrapInfoDTO(BaseModel):
    cluster_config: ClusterConfigDTO
    template: str = 'normal'
    platform: str = 'aliyun'
    patch_setting: Optional[Dict] = None



class RandomTemplateVariablesDTO(BaseModel):
    variables: List[str]
    lengths: Optional[List[int]] = None



class FileTemplateVariablesDTO(BaseModel):
    variables: Optional[List[str]]
    path: str



class FilesTemplateVariablesDTO(BaseModel):
    variables: List[str]
    paths: List[str]