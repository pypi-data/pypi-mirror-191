import os
import pickle
from pathlib import Path
import pprint

import appdirs
from autumn8.cli.cli_environment import CliEnvironment
from autumn8.common.config.s3 import init_s3, init_s3_client

APP_NAME = "autumn8"
APP_AUTHOR = "autumn8"

data_dir = appdirs.user_data_dir(APP_NAME, APP_AUTHOR)
RESUMABLE_UPLOADS_PATH = os.path.join(data_dir, "uploads.pickle")


def retrieve_pending_uploads():
    if os.path.exists(RESUMABLE_UPLOADS_PATH):
        with open(RESUMABLE_UPLOADS_PATH, "rb") as f:
            return pickle.load(f)

    return {}


def forget_all_pending_uploads():
    os.remove(RESUMABLE_UPLOADS_PATH)


def update_upload(run_id, resume_args):
    if os.path.exists(RESUMABLE_UPLOADS_PATH):
        with open(RESUMABLE_UPLOADS_PATH, "rb") as f:
            data = pickle.load(f)

    else:
        data_path = Path(data_dir)
        data_path.mkdir(parents=True, exist_ok=True)
        data = {}

    data[run_id] = resume_args

    with open(RESUMABLE_UPLOADS_PATH, "wb") as f:
        pickle.dump(data, f)


def remove_upload(run_id):
    if os.path.exists(RESUMABLE_UPLOADS_PATH):
        with open(RESUMABLE_UPLOADS_PATH, "rb") as f:
            data = pickle.load(f)

        if run_id not in data:
            return

        resume_args = data[run_id]
        environment: CliEnvironment = resume_args["environment"]
        if (
            "model_file_upload_id" in resume_args
            and resume_args["model_file_upload_id"] is not None
        ):
            abort_upload(environment, resume_args["model_file_upload_id"])

        if (
            "input_file_upload_id" in resume_args
            and resume_args["input_file_upload_id"] is not None
        ):
            abort_upload(environment, resume_args["input_file_upload_id"])

        data.pop(run_id)

        with open(RESUMABLE_UPLOADS_PATH, "wb") as f:
            pickle.dump(data, f)


def abort_upload(environment: CliEnvironment, mpu_id: str):
    s3 = init_s3_client(environment.value.s3_host)
    s3_bucket_name = environment.value.s3_bucket_name
    mpus = s3.list_multipart_uploads(Bucket=s3_bucket_name)
    if "Uploads" in mpus:
        for upload in mpus["Uploads"]:
            upload_id = upload.get("UploadId")
            key = upload.get("Key")
            if upload_id is None or key is None:
                continue
            if upload_id == mpu_id:
                print("aborting upload", key, " - ", upload_id)
                s3.abort_multipart_upload(
                    Bucket=s3_bucket_name, Key=key, UploadId=upload_id
                )
                return
