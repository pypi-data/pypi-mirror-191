from typing import Any, Dict
from google.cloud import storage
from google.oauth2 import service_account
import json
import pickle
from PIL import Image
import numpy as np
import os
import io
import shutil
from rich.console import Console


creds = {
    "type": "service_account",
    "project_id": "dev-backend-369517",
    "private_key_id": "497c1d68fc3dca13e9e4a72e1f6ebc5156de7742",
    "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQDqxf5h2PvHtu+a\nzIBVwRUXXLln7CDaWiV0XK5w9jOu1lPcDjEsBIBbFQgL8ApC0U9eBQrrRpmTEBgQ\nGXf4i1ipv+xrl7psDSUJ7kgpY2ank+wWvI06u9Bo5XMj6ig3oPInVnN1Zq09vN1K\n52MG4IqC8S+ezbUHZKe+iczeokc73LjP6J11RnTNCI+pmD8FH2mQW7oDsilOcZvY\nuX7g2kTgQNJGexlyE9fq2JLc+LdhVOyLErfdVSuRTDT3MnR2NTpt0bBFQFofLPRq\ndW130jGoXSb8881NYelPinFWHB8FUjsuZXS0KP3UpMIKMl+Q14f4dZqQaxTjKMdw\nP0hjGvipAgMBAAECggEASTRRfIse/wgQsDEB9ztMa0tzWG8tU0h2k1Du57QtK2AT\nJ/OY64O/zibBqo8/c9Q2LjfeTrxl2JBVIHgAi5RPoiaA/o+CBn0WxoDxKU6gTLJ4\nFCLY2q6DbqHVBCbYQXhC6XcwazQH4s9IJTn/C77qEahI0/iKcPK2x1fKdMUe9w/j\n/1pLlO8Z+i8FgKexk5z2QCsHRhS5efDqMxvhI7/Ct+VxBveMfLQhD2t6yuigFRwN\n0CY7jIv4x1uLbVrYuIxnLNxoeEMO9VdVpkT6JYXSU217KIoZQxoCFfDe3RYJhIB+\n/EJpxn1PZ1MYU8tia34jUA4ZjjEmqz+Ey+wJ9mCXPQKBgQD309cJxsewNKZOffyu\n9D8q0y/qsVNSCtiVGrYP5/3caGIaqN/TA6hGazonsSL2xBWqwbnxGbCg+QKPiRQ6\n9GTZAQlg+9O7wCFd3o9aMvTHubK169HT2GTHGSJ5xDGt3tgG2TUNxOiMiyiLvESo\nV9KLS2G5IL0cu/oHp3qMTBhXNwKBgQDyg/N5W8E9eENkA3EkQ0FCi7JJjSy5SjUX\nrd1L7LxOg/g2M4Dy+EPvKPJWfvZfytVDNkxQuFlScT9zlZn1Q8N7DY2tP1VAhcbW\nTdRbK7XEHWVYUyZJUUT6Bl0VRfZvkKkWvu3OKaEBi8y35y5xWIG2qEZCOGMBoaMH\nct6K+g1fHwKBgGfMUT+mAxMZKiKr//5jDGXqaCJbPPOa2VWyB1koKJp9GcHiw0RF\nPuCnnobrWSKTxCNt2mxR/zmcsebeWhvLKsX8+imlr+vuL8t6IP59YyqX63Lon0yk\nUKlXLKplcw1IzaAor2Dh/SiITGYiZ3s+tU9kNjzsqmhzjuhPzDMg1/0HAoGBAJix\n3CsdSp6ZilT+lc5vSjfMHYWSDgbcYnF2V0/mzungzffSle5lwuBit7MeXaIS5BRd\nq89nQ1ZVV84+86Ep+XsRHZNnvRXTJU7p0jtVWi0RFS53rDOdqACE4TbzxiaYvt5D\neRfFvkpq64sfVG6pe4K2kQZA2pW8YBngiZ6XsrOhAoGBAKuNdpgUW9mJv2a9z3Mw\njjN5/dk8XcuwU0PD3lB0fmlMkMdlhwvJb0oPJbZpTBJ5RTNlvDiioCOGhHFJynPK\nLJpjY2jBe6yVbiHBld0yzcFo8jG8HSMzJy3Kh5DF3ViMeJ8KWzkeODQZW3KaRHM5\nq1aZbG8A8/Zj4GNl0mrx41z8\n-----END PRIVATE KEY-----\n",
    "client_email": "gsa-alectio-dev-bucket@dev-backend-369517.iam.gserviceaccount.com",
    "client_id": "100877879306817124839",
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/gsa-alectio-dev-bucket%40dev-backend-369517.iam.gserviceaccount.com",
}
credentials = service_account.Credentials.from_service_account_info(creds)
gcpStorageClient = storage.Client(project=None, credentials=credentials)
console = Console()


class GCP_Storage:
    def download_file(
        self, storage_bucket: str, object_key: str, format: str, dest_path: str
    ):
        bucket = gcpStorageClient.get_bucket(storage_bucket)
        blob = bucket.blob(object_key)
        if format in ["jpg", "png", "jpeg"]:
            os.makedirs(os.path.dirname(dest_path), exist_ok=True)
            blob.download_to_filename(dest_path)
        if format == "zip":
            done = False
            with console.status("[bold green]Loading dataset from cloud...") as status:
                while not done:
                    blob.download_to_filename(dest_path + ".zip")
                    shutil.unpack_archive(dest_path + ".zip", dest_path)
                    done = True

    def read_file(self, storage_bucket: str, object_key: str, format: str):
        bucket = gcpStorageClient.get_bucket(storage_bucket)
        blob = bucket.blob(object_key)

        if format == "json":
            data = json.loads(blob.download_as_string(client=None))
        if format == "pkl":
            data = pickle.loads(blob.download_as_string(client=None))
        if format == "text":
            data = blob.download_as_string(client=None)
        return data

    def upload_object(
        self, storage_bucket: str, object: Any, object_key: str, format: str
    ):
        bucket = gcpStorageClient.get_bucket(storage_bucket)
        blob = bucket.blob(object_key)

        if format == "json":
            blob.upload_from_string(data=json.dumps(object))
        if format == "pkl":
            blob.upload_from_string(data=pickle.dumps(object))
        if format == "txt":
            blob.upload_from_string(data=object)
        if format in ["png", "jpg"]:
            img = Image.fromarray(np.uint8(object)).convert("RGB")
            blob.upload_from_string(img.tobytes(), content_type="image/jpeg")

    def upload_file(self, storage_bucket: str, file_path: str, object_key: str):
        bucket = gcpStorageClient.get_bucket(storage_bucket)
        blob = bucket.blob(object_key)
        blob.upload_from_filename(file_path)
