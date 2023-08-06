import math
import os
from typing import Dict, Optional
import tempfile
from urllib.parse import urljoin
from pathlib import Path
import shutil

from fiddler.libs.http_client import RequestClient
from fiddler.utils import logging
from fiddler.v2.constants import UploadType
from fiddler.v2.utils.response_handler import APIResponseHandler

logger = logging.getLogger(__name__)

UPLOAD_TYPE_KEY = 'upload_type'
RESOURCE_IDENT_KEY = 'resource_identifier'
FILE_NAME_KEY = 'file_name'
MULTIPART_UPLOAD_KEY = 'multipart_upload'
IS_UPDATE = 'is_update'
CONTENT_TYPE_KEY = 'Content-Type'
UPLOAD_ID_KEY = 'upload_id'
MULTIPART_UPLOAD_SIZE_THRESHOLD = 5 * 1024 * 1024 # bytes

def multipart_upload(
    client: RequestClient,
    organization_name: str,
    project_name: str,
    identifier: str,
    upload_type: UploadType,
    file_path: str,
    file_name: str,
    chunk_size: Optional[int] = 100 * 1024 * 1024,  # bytes
) -> Dict[str, str]:
    """
    Perform multipart upload for datasets/events ingestion
    """
    base_url = f'datasets/{organization_name}:{project_name}/'
    UPLOAD_INITIALIZE_URL = urljoin(base_url, 'initialize')
    UPLOAD_URL = urljoin(base_url, 'upload')
    UPLOAD_COMPLETE_URL = urljoin(base_url, 'complete')

    if not os.path.exists(file_path):
        raise ValueError(
            f'File {file_path} not found. Please check if the entered path is correct.'
        )
    file_size = os.path.getsize(file_path)
    if file_size < MULTIPART_UPLOAD_SIZE_THRESHOLD:
        with open(file_path, 'rb') as f:
            file_data = f.read()
            response = client.put(
                url=UPLOAD_URL,
                params={
                    UPLOAD_TYPE_KEY: upload_type,
                    MULTIPART_UPLOAD_KEY: False,
                    RESOURCE_IDENT_KEY: identifier,
                    FILE_NAME_KEY: file_name,
                },
                data=file_data,
                headers={CONTENT_TYPE_KEY: 'application/octet-stream'},
            )
    else:
        # Step 1: Initialize multipart upload
        response = client.post(
            url=UPLOAD_INITIALIZE_URL,
            data={
                RESOURCE_IDENT_KEY: identifier,
                FILE_NAME_KEY: file_name,
                UPLOAD_TYPE_KEY: upload_type,
            },
        )
        response_data = APIResponseHandler(response).get_data()
        upload_id = response_data.get(UPLOAD_ID_KEY)
        file_name = response_data.get(FILE_NAME_KEY)
        part_no = 1
        parts = []
        total_chunks = math.ceil(file_size / chunk_size)
        # Step 2: Chunk and upload
        with open(file_path, 'rb') as f:
            logger.info('Beginning chunk upload')
            file_data = f.read(chunk_size)
            while file_data:
                response = client.put(
                    url=UPLOAD_URL,
                    params={
                        UPLOAD_TYPE_KEY: upload_type,
                        MULTIPART_UPLOAD_KEY: True,
                        RESOURCE_IDENT_KEY: identifier,
                        FILE_NAME_KEY: file_name,
                        UPLOAD_ID_KEY: upload_id,
                        'part_number': part_no,
                    },
                    data=file_data,
                    headers={CONTENT_TYPE_KEY: 'application/octet-stream'},
                )
                resp_data = APIResponseHandler(response).get_data()
                parts.append(
                    {
                        'ETag': resp_data.get('info').get('ETag'),
                        'PartNumber': resp_data.get('info').get('PartNumber'),
                    }
                )
                logger.info(f'Chunk uploaded: {part_no}/{total_chunks}')
                part_no += 1
                file_data = f.read(chunk_size)
        # Step 3: Complete the upload
        response = client.post(
            url=UPLOAD_COMPLETE_URL,
            params={
                UPLOAD_TYPE_KEY: upload_type,
                RESOURCE_IDENT_KEY: identifier,
                FILE_NAME_KEY: file_name,
                UPLOAD_ID_KEY: upload_id,
            },
            data={'parts': parts},
        )
    logger.info('File successfully uploaded to blob store')
    return APIResponseHandler(response).get_data()


def multipart_upload_model(
    client: RequestClient,
    organization_name: str,
    project_name: str,
    model_name: str,
    artifact_path: str,
    is_update: Optional[bool] = False,
    chunk_size: Optional[int] = 100 * 1024 * 1024,  # bytes
    ) -> Dict[str, str]:
    """
    Perform multipart upload for model ingestion
    """
    base_url = f'model-artifacts/{organization_name}:{project_name}:{model_name}/'
    UPLOAD_INITIALIZE_URL = urljoin(base_url, 'initialize')
    UPLOAD_URL = urljoin(base_url, 'upload')
    UPLOAD_COMPLETE_URL = urljoin(base_url, 'complete')

    if not os.path.exists(artifact_path):
        raise ValueError(
            f'File {artifact_path} not found. Please check if the entered path is correct.'
        )

    with tempfile.TemporaryDirectory() as tmp:
        file_name = shutil.make_archive(
            base_name=str(Path(tmp) / 'files'),
            format='tar',
            root_dir=str(artifact_path),
            base_dir='.',
        )
        file_size = os.path.getsize(file_name)

        if file_size < MULTIPART_UPLOAD_SIZE_THRESHOLD:
            with open(file_name, 'rb') as f:
                file_data = f.read()
                response = client.put(
                    url=UPLOAD_URL,
                    params={
                        MULTIPART_UPLOAD_KEY: False,
                        IS_UPDATE: is_update,
                    },
                    data=file_data,
                    headers={CONTENT_TYPE_KEY: 'application/octet-stream'},
                )
        else:
            # Step 1: Initialize multipart upload
            response = client.post(
                url=UPLOAD_INITIALIZE_URL,
            )
            response_data = APIResponseHandler(response).get_data()
            upload_id = response_data.get(UPLOAD_ID_KEY)
            part_no = 1
            parts = []
            total_chunks = math.ceil(file_size / chunk_size)
            # Step 2: Chunk and upload
            with open(file_name, 'rb') as f:
                logger.info('Beginning chunk upload')
                file_data = f.read(chunk_size)
                while file_data:
                    response = client.put(
                        url=UPLOAD_URL,
                        params={
                            MULTIPART_UPLOAD_KEY: True,
                            IS_UPDATE: is_update,
                            UPLOAD_ID_KEY: upload_id,
                            'part_number': part_no,
                        },
                        data=file_data,
                        headers={CONTENT_TYPE_KEY: 'application/octet-stream'},
                    )
                    resp_data = APIResponseHandler(response).get_data()
                    parts.append(
                        {
                            'ETag': resp_data.get('info').get('ETag'),
                            'PartNumber': resp_data.get('info').get('PartNumber'),
                        }
                    )
                    logger.info(f'Chunk uploaded: {part_no}/{total_chunks}')
                    part_no += 1
                    file_data = f.read(chunk_size)
            # Step 3: Complete the upload
            response = client.post(
                url=UPLOAD_COMPLETE_URL,
                params={
                    UPLOAD_ID_KEY: upload_id,
                },
                data={'parts': parts},
            )

    logger.info('Model successfully uploaded to blob store')
    return APIResponseHandler(response).get_data()
