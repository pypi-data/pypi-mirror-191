"""The implementation of the metaloop data service."""

import logging
import os.path
import re
import time
from typing import Any, List

from metaloop.client.cloud_storage import CloudClient
from metaloop.client.requests import Client
from metaloop.client.x_api import X_API
from metaloop.dataset import Dataset
from metaloop.exception import *

logger = logging.getLogger(__name__)
DEFAULT_BRANCH = "main"


class MDS:
    """:class:`MDS` defines the initial client to interact with MetaLoop.

    :class:`MDS` provides some operations on dataset level such as
    :meth:`MDS.create_dataset` :meth:`MetaLoop.get_dataset` and :meth:`MetaLoop.delete_dataset`.

    Arguments:
        access_key: User's access key.
        url: The host URL of the MetaLoop website.

    """

    def __init__(self, access_key: str, url: str = 'http://data.deepglint.com/') -> None:
        self._client = Client(access_key, url)
        self._x_api = X_API(self._client)

    @property
    def x_api(self):
        return self._x_api

    def create_dataset(
            self,
            name: str,
            data_type: str,
            tags: List[str],
            space: Optional[str] = "",
            comment: Optional[str] = "",
    ) -> Dataset:
        """Create a MetaLoop dataset with given name.

        Arguments:
            name: Name of the dataset, unique for platform.
            data_type: Type of the dataset, support 'image', 'video' or 'none'.
            tags: Tags of the dataset, used for dataset searching.
            space: Space where the dataset is belonged to, default is empty means personal dataset.
            comment: Comment of the dataset, default is "".

        Returns:
            The created :class:`~metaloop.dataset.dataset.Dataset` instance.

        """
        if len(name) > 35:
            raise InvalidParamsError(message="length of name cannot exceed 35")

        if not re.match("^[A-Za-z0-9-_\u4e00-\u9fa5]+$", name):
            raise InvalidParamsError(message="invalid name, only support A-Z, a-z, 0-9, -, _ and Chinese")

        if data_type not in {"image", "video", "none"}:
            raise InvalidParamsError(param_name="data_type", param_value=data_type)

        try:
            self._x_api.get_dataset_name(name)
            raise NameConflictError(resource="dataset", identification=name)
        except ResourceNotExistError:
            pass

        if space:
            self._x_api.get_space(space)

        tag_ids = []
        for item in tags:
            try:
                tag = self._x_api.get_tag(item)
                tag_ids.append(tag["id"])
            except IndexError:
                pass

        post_data = {
            "name": name,
            "data_type": data_type,
            "project": space,
            "tags": tag_ids,
            "comment": comment,
        }

        info = self._x_api.create_dataset(post_data)
        dataset_id = info["id"]
        version = info["version"]
        created_user = info["created_user"]
        created_time = int(time.time() * 1e3)
        versions = {0: dataset_id}

        return Dataset(
            self,
            name,
            data_type,
            space,
            dataset_id,
            version,
            tags=tags,
            created_user=created_user,
            create_timestamp=created_time,
            versions=versions,
            comment=comment
        )

    def _info_to_dataset(self, info) -> Dataset:
        name = info["name"]
        data_type = info["data_type"]
        space = info["project"]
        tags = info["tag_names"]
        created_user = info["created_user"]
        create_timestamp = info["create_timestamp"]
        versions = info["versions"]
        source = info["source"]
        meta_comment = info["comment"]

        if len(versions) == 0:
            raise InternalServerError

        version_info: Dict[int, str] = {}
        for version in versions:
            version_info[int(version["version"])] = version["id"]

        dataset_info = versions[0]
        dataset_id = dataset_info["id"]
        comment = dataset_info["comment"]
        data_count = dataset_info["data_count"]
        version = dataset_info["version"]
        annotation_status = dataset_info["annotation_status"]
        last_import_status = dataset_info["last_import_status"]
        last_data_clean_status = dataset_info["last_data_clean_status"]
        attachment_url = dataset_info["attachment_url"] if "attachment_url" in dataset_info else ""

        return Dataset(
            self,
            name,
            data_type,
            space,
            dataset_id,
            version,
            tags=tags,
            created_user=created_user,
            create_timestamp=create_timestamp,
            versions=version_info,
            source=source,
            meta_comment=meta_comment,
            comment=comment,
            data_count=data_count,
            annotation_status=annotation_status,
            last_import_status=last_import_status,
            last_data_clean_status=last_data_clean_status,
            attachment_url=attachment_url
        )

    def get_dataset_by_id(self, dataset_id: str) -> Dataset:
        """Get a dataset with given ID.

        Arguments:
            dataset_id: The ID of the requested dataset version.

        Returns:
            The requested :class:`~metaloop.dataset.dataset.Dataset` instance

        """
        info = self._x_api.get_version(dataset_id)

        try:
            dataset = self.get_dataset(info["name"])
        except KeyError as error:
            raise ResourceNotExistError(f"meta data of dataset {dataset_id} doesn't exist") from error

        dataset.checkout(info["version"])
        return dataset

    def get_dataset(self, name: str) -> Dataset:
        """Get a dataset with given name.

        Arguments:
            name: The name of the requested dataset.

        Returns:
            The requested :class:`~metaloop.dataset.dataset.Dataset` instance

        """
        info = self._x_api.get_dataset(name)
        return self._info_to_dataset(info)

    def list_dataset(self, name: Optional[str] = "") -> List[Dataset]:
        """List datasets

        Arguments:
            name: The name of the requested dataset.

        Returns:
            The requested : List[class]:`~metaloop.dataset.dataset.Dataset` instance

        """
        ds = List[Dataset]
        response = self._x_api.list_datasets(name)
        try:
            total_count = response["total_count"]
            count = response["count"]
            for i in range(count):
                ds.append(self._info_to_dataset(response["data"][i]))
        except IndexError as error:
            raise ResourceNotExistError(resource="dataset", identification=name) from error
        return ds

    def delete_dataset(
            self,
            name: str,
            version_number: Optional[int] = None
    ) -> None:
        """Delete a MetaLoop dataset with given name and given version number.
        If the version number is not specified, the whole dataset will be removed.

        Arguments:
            name: Name of the dataset.
            version_number: Version number of the dataset.

        """
        dataset = self.get_dataset(name)
        if version_number:
            dataset.delete_version(version_number)
            return

        for dataset_id in dataset.versions.values():
            self._client.open_api_do("DELETE", "", dataset_id)

        dataset._id = None
        dataset._version = -1

    @staticmethod
    def create_s3_storage_config(
            identifier: str,
            endpoint: str,
            access_key_id: str,
            secret_access_key: str,
            default_bucket: str
    ) -> None:
        """Create a s3 auth storage config.

        Arguments:
            identifier: Custom identifier of the s3 config.
            endpoint: Endpoint of the s3.
            access_key_id: access_key_id of the s3.
            secret_access_key: secret_access_key of the s3.
            default_bucket: The authorized or default bucket of s3.

        """
        CloudClient.set_s3_config(
            identifier,
            endpoint,
            access_key_id,
            secret_access_key,
            default_bucket
        )

    def upload_files_to_s3_storage(
            self,
            bucket: str,
            file_path: str,
            upload_prefix: Optional[str] = "",
            storage_type: Optional[str] = "local",
            identifier: Optional[str] = None
    ):
        if not identifier:
            s3_config = CloudClient.get_cloud_storage_config(self._x_api, "", storage_type=storage_type)
            identifier = s3_config.identifier
        if os.path.isdir(file_path):
            CloudClient.upload_files_parallel(identifier, bucket, file_path, upload_prefix, 1, 8)
        else:
            CloudClient.upload_file(identifier, bucket, file_path, upload_prefix)

    def download_files_from_s3_storage(
            self,
            bucket: str,
            prefix: str,
            file_path: str,
            storage_type: Optional[str] = "local",
            identifier: Optional[str] = None
    ):
        if not identifier:
            s3_config = CloudClient.get_cloud_storage_config(self._x_api, "", storage_type=storage_type)
            identifier = s3_config.identifier
        CloudClient.download_files_parallel(identifier, bucket, prefix, file_path, 1, 8)

    def batch_export(
            self,
            dataset_ids: List[str],
            file_path: str,
            storage_type: Optional[str] = "local"
    ) -> None:
        """export dataset in batch

        Arguments:
            dataset_ids: IDs of dataset to export.
            file_path: File path of exported data.
            storage_type: Source of exported data, includes:

                1. "local": MetaLoop default local object storage;
                2. "external": Tencent Cloud Object Storage (COS).

        """
        if len(dataset_ids) < 1:
            raise InvalidParamsError(message="dataset_ids is empty")

        dataset = self.get_dataset_by_id(dataset_ids[0])
        dataset.export_data(file_path, storage_type, dataset_ids=dataset_ids)

    def export_annotated_data(
            self,
            dataset_ids: List[str],
            file_path: str,
            storage_type: Optional[str] = "local"
    ) -> None:
        """export annotation dataset in batch, only support annotated or pre_annotated data

        Arguments:
            dataset_ids: IDs of dataset to export.
            file_path: File path of exported data.
            storage_type: Source of exported data, includes:

                1. "local": MetaLoop default local object storage;
                2. "external": Tencent Cloud Object Storage (COS).

        """
        if not dataset_ids:
            raise InvalidParamsError(message="dataset_ids is empty")

        annotated_dataset = []
        pre_annotated_dataset = []
        for dataset_id in dataset_ids:
            dataset = self.get_dataset_by_id(dataset_id)
            if dataset.annotation_status == 2:
                annotated_dataset.append(dataset_id)
            elif dataset.annotation_status == 3:
                pre_annotated_dataset.append(dataset_id)
            else:
                raise InvalidParamsError(message=f"dataset '{dataset_id}' has no annotation info")

        if len(pre_annotated_dataset) > 0:
            dataset = self.get_dataset_by_id(pre_annotated_dataset[0])
            dataset.export_data(file_path, storage_type, dataset_ids=pre_annotated_dataset)
            json_file = os.path.join(file_path, 'output.json')
            if os.path.exists(json_file):
                os.rename(json_file, os.path.join(file_path, 'output.json.pre'))

        if len(annotated_dataset) > 0:
            dataset = self.get_dataset_by_id(annotated_dataset[0])
            dataset.export_data(file_path, storage_type, dataset_ids=annotated_dataset)
            pre_json_file = os.path.join(file_path, 'output.json.pre')
            if os.path.exists(pre_json_file):
                json_file = os.path.join(file_path, 'output.json')
                file_out = open(json_file, 'a')
                with open(pre_json_file, 'r') as file_in:
                    for line in file_in.readlines():
                        file_out.write(line)
                file_out.close()
                os.remove(pre_json_file)

    def call_model_convert_path_status(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """callback modelConvert path and status.

        Arguments:
            data: The data of the requested json
                mpid:  模型转换id
                enc_way: 加密方式,
                minio_path: minio模型转换路径,
                ftp_path: ftp模型转换路径,
                status: 转换状态
                is_arm:  是否是arm模型 

        """
        if data.get("mpid") is None:
            raise InvalidParamsError(message="mid not blank")
        info = self._x_api.call_model_convert_path_status(data)
        return info

    def call_model_test_status(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """callback modelTest status.

        Arguments:
            data: The data of the requested json
                mtid:  模型测试id
                result_path: 测试结果路径,
                eval_content: 模型测试eval内容,
                perform_content: 模型测试perform内容,
                status: 转换状态

        """
        if data.get("mtid") is None:
            raise InvalidParamsError(message="mid not blank")
        info = self._x_api.call_model_test_status(data)
        return info

    def call_model_test_result_content(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """callback modelTestResult content..

        Arguments:
            data: The data of the requested json
                tid:  模型测试id
                content: 模型测试内容,

        """
        if data.get("tid") is None:
            raise InvalidParamsError(message="mid not blank")
        info = self._x_api.call_model_test_result_content(data)
        return info

    def send_notice(
            self,
            title: str,
            status: int,
            msg: str,
            usernames: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """Send notice to metaloop users

        Arguments:
            title: notice type.
            status: project status you want to notice, 1 is succeed , 2 is failed , 3 is common.
            msg: the msg you want to notice.
            usernames: the users you want to notice, if usernames is nil , then notice will send to yourself.

        """
        info = self._x_api.send_notice(title, status, msg, usernames)
        return info

    class NOTICE:
        SUCCEED = 1
        FAILED = 2
        COMMON = 3

    class CALIB:
        UPLOADFAILED = -1
        DELETED = 0
        PROCESSING = 1
        SUCCEED = 2
        CONVERTFAILED = 3
        FAILED = 4
        DEFAULTCATEGORY = "default"
        PROGRESSCATEGORY = "progress"

    def update_calibset(self,
                        id: int,
                        status: Optional[int] = CALIB.PROCESSING,
                        pb_url: Optional[str] = "",
                        log: Optional[str] = "",
                        folders: Optional[str] = "",
                        category: Optional[str] = "default"
                        ) -> Dict[str, Any]:
        """update calibset

        Arguments:
            id: calibset id.
            status: calibset status.
            pb_url: convert pburl.
            log: log of pipeline.
            folders: progress
            category: default update [ pburl , log , status ], progress update [ category ]
        """
        info = self._x_api.update_calibset(id, status, pb_url, log, folders, category)
        return info
