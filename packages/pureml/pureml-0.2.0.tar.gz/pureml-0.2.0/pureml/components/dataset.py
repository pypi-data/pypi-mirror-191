import json
import os
from urllib.parse import urljoin
import time
import joblib
import pandas as pd
import requests
from pureml.utils.constants import BASE_URL, PATH_DATASET_DIR, PATH_DATASET_README
from pureml.utils.hash import generate_hash_for_file
from pureml.utils.readme import load_readme
from rich import print

from . import get_org_id, get_token


def init_branch(branch: str, dataset_name: str):
    user_token = get_token()
    org_id = get_org_id()

    url = "org/{}/dataset/{}/branch/create".format(org_id, dataset_name)
    url = urljoin(BASE_URL, url)

    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer {}".format(user_token),
    }

    data = {"dataset_name": dataset_name, "branchName": branch}

    data = json.dumps(data)
    
    
    response = requests.post(url, data=data, headers=headers)

    if response.ok:
        print(f"[bold green]Branch has been created!")

        return True

    else:
        print(f"[bold red]Branch has not been created!")

        return False


def check_dataset_hash(hash: str, name: str, branch: str):

    user_token = get_token()
    org_id = get_org_id()

    url = "org/{}/dataset/{}/branch/{}/hash-status".format(org_id, branch, name)
    url = urljoin(BASE_URL, url)

    headers = {"Authorization": "Bearer {}".format(user_token)}

    data = {"hash": hash, "branch": branch}

    data = json.dumps(data)
    
    
    response = requests.post(url, data=data, headers=headers)

    hash_exists = False

    if response.ok:
        hash_exists = response.json()["data"]

    return hash_exists


def branch_details(branch: str, dataset_name: str):
    user_token = get_token()
    org_id = get_org_id()

    url = "org/{}/dataset/{}/branch/{}".format(org_id, dataset_name, branch)
    url = urljoin(BASE_URL, url)

    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Authorization": "Bearer {}".format(user_token),
    }

    
    response = requests.get(url, headers=headers)

    if response.ok:
        response_text = response.json()
        # T-1161 standardize api response to contains Data as a list
        details = response_text["data"]

        # details = response_text['data'][0]
        # print(details)

        return details

    else:
        print(f"[bold red]Branch details details have not been found")
        return


def branch_status(branch: str, dataset_name: str):

    details = branch_details(branch=branch, dataset_name=dataset_name)

    if details:
        return True
    else:
        return False


def branch_delete(branch: str, dataset_name: str) -> str:

    user_token = get_token()
    org_id = get_org_id()

    url = "org/{}/dataset/{}/branch/{}/delete".format(org_id, dataset_name, branch)
    url = urljoin(BASE_URL, url)

    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Authorization": "Bearer {}".format(user_token),
    }

    
    response = requests.delete(url, headers=headers)

    if response.ok:
        print(f"[bold green]Dataset branch has been deleted")

    else:
        print(f"[bold red]Unable to delete Model branch")

    return response.text


def branch_list(dataset_name: str) -> str:

    user_token = get_token()
    org_id = get_org_id()

    url = "org/{}/dataset/{}/branch".format(org_id, dataset_name)
    url = urljoin(BASE_URL, url)

    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Authorization": "Bearer {}".format(user_token),
    }

    
    response = requests.get(url, headers=headers)

    if response.ok:
        response_text = response.json()
        branch_list = response_text["data"]

        return branch_list

    else:
        print(f"[bold red]Unable to obtain the list of branches!")

    return response.text


def list():
    """This function will return a list of all the datasets

    Returns
    -------
        A list of all the datasets

    """

    user_token = get_token()
    org_id = get_org_id()

    url = "org/{}/dataset/all".format(org_id)
    url = urljoin(BASE_URL, url)

    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Authorization": "Bearer {}".format(user_token),
    }

    
    response = requests.get(url, headers=headers)

    if response.ok:
        # print(f"[bold green]Obtained list of models")

        response_text = response.json()
        dataset_list = response_text["data"]
        # print(model_list)

        return dataset_list
    else:
        print(f"[bold red]Unable to obtain the list of dataset!")

    return


def init(name: str, readme: str = None, branch: str = None):
    user_token = get_token()
    org_id = get_org_id()

    if readme is None:
        readme = PATH_DATASET_README

    file_content, file_type = load_readme(path=readme)

    branch_user = "dev" if branch is None else branch
    branch_main = "main"

    url = "org/{}/dataset/{}/create".format(org_id, name)
    url = urljoin(BASE_URL, url)

    headers = {
        # "Content-Type": "application/json",
        "Authorization": "Bearer {}".format(user_token),
        # 'accept': 'application/json',
        'Content-Type': '*/*',
    }

    data = {
        "name": name,
        "branch_names": [branch_main, branch_user],
        "readme": {"file_type": file_type, "content": file_content},
    }
    
    data = json.dumps(data)
    files = {'file': (readme, open(readme, "rb"), file_type)}
    # response = requests.post(url, data=data, headers=headers, files=files)
    #     
    response = requests.post(url, data=data, headers=headers)


    if response.ok:
        print(f"[bold green]Dataset has been created!")

        return True

    else:
        print(f"[bold red]Dataset has not been created!")

        return False


def save_dataset(dataset, name: str):
    # file_name = '.'.join([name, 'parquet'])
    file_name = ".".join([name, "pkl"])
    save_path = os.path.join(PATH_DATASET_DIR, file_name)

    os.makedirs(PATH_DATASET_DIR, exist_ok=True)

    # dataset.to_parquet(save_path)
    joblib.dump(dataset, save_path)

    return save_path


def register(
    dataset,
    name: str,
    lineage,
    branch: str,
    is_empty: bool = False,
    storage: str = "PUREML-STORAGE",
) -> str:
    """The function takes in a dataset, a name and a version and saves the dataset locally, then uploads the
    dataset to the PureML server

    Parameters
    ----------
    dataset
        The dataset you want to register
    name : str
        The name of the dataset.
    version: str, optional
        The version of the dataset.

    """

    user_token = get_token()
    org_id = get_org_id()

    dataset_path = save_dataset(dataset, name)
    name_with_ext = dataset_path.split("/")[-1]

    dataset_hash = generate_hash_for_file(
        file_path=dataset_path, name=name, branch=branch, is_empty=is_empty
    )

    if is_empty:
        dataset_path = save_dataset(dataset=None, name=name)
        name_with_ext = dataset_path.split("/")[-1]


    dataset_exists = dataset_status(name)
    # print('Dataset status', dataset_exists)

    if not dataset_exists:
        dataset_created = init(name=name, branch=branch)
        # print('dataset_created', dataset_created)
        if not dataset_created:
            print("[bold red] Unable to register the dataset")
            return False, dataset_hash, None
    else:
        print("[bold green] Connected to Dataset")

    branch_exists = branch_status(branch=branch, dataset_name=name)
    # print('Branch status', branch_exists)

    if not branch_exists:
        branch_created = init_branch(branch=branch, dataset_name=name)
        # print('branch_created', branch_created)

        if not branch_created:
            print("[bold red] Unable to register the dataset")
            return False, dataset_hash, None
    else:
        print("[bold green] Connected to Branch")

    dataset_exists_remote = check_dataset_hash(
        hash=dataset_hash, name=name, branch=branch
    )

    if dataset_exists_remote:

        print(f"[bold red]Dataset already exists. Not registering a new version!")
        return True, dataset_hash, "latest"
    else:

        url = "org/{}/dataset/{}/branch/{}/register".format(org_id, name, branch)
        url = urljoin(BASE_URL, url)

        headers = {"Authorization": "Bearer {}".format(user_token),
                    'accept': 'application/json'}

        files = {"file": (name_with_ext, open(dataset_path, "rb"))}

        lineage = json.dumps(lineage)

        data = {
            "name": name,
            "branch": branch,
            "hash": dataset_hash,
            "lineage": lineage,
            "is_empty": is_empty,
            "storage": storage,
        }

        # data = json.dumps(data)
        
        response = requests.post(url, files=files, data=data, headers=headers)


        if response.ok:

            # print(response.json())
            try:
                dataset_version = response.json()["data"][0]["version"]
               
                if is_empty:
                    print(f"[bold green]Lineage has been registered!")
                else:
                    print(f"[bold green]Dataset and lineage have been registered!")
                    
            except Exception as e:
                print('[bold red] Incorrect json response. Dataset has not been registered')
                print(e)
                dataset_version = None



            return True, dataset_hash, dataset_version
        else:
            print(f"[bold red]Dataset has not been registered!")
            print(response.text)

            return True, dataset_hash, None


def dataset_status(name: str):

    dataset_details = details(name=name)

    if dataset_details:
        return True
    else:
        return False


def details(
    name: str,
):
    """It fetches the details of a dataset.

    Parameters
    ----------
    name : str
        The name of the dataset
    version: str
        The version of the dataset
    Returns
    -------
        The details of the dataset.

    """

    user_token = get_token()
    org_id = get_org_id()

    url = "org/{}/dataset/{}".format(org_id, name)
    url = urljoin(BASE_URL, url)

    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Authorization": "Bearer {}".format(user_token),
    }

    
    response = requests.get(url, headers=headers)

    if response.ok:
        # print(f"[bold green]Dataset details have been fetched")
        response_text = response.json()
        dataset_details = response_text["data"][0]

        return dataset_details

    else:
        print(f"[bold red]Dataset details have not been found")
        return


def version_details(name: str, branch: str, version: str = "latest"):
    """It fetches the details of a dataset.

    Parameters
    ----------
    name : str
        The name of the dataset
    version: str
        The version of the dataset
    Returns
    -------
        The details of the dataset.

    """

    user_token = get_token()
    org_id = get_org_id()

    url = "org/{}/dataset/{}/branch/{}/version/{}".format(
        org_id, name, branch, version
    )
    url = urljoin(BASE_URL, url)

    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Authorization": "Bearer {}".format(user_token),
    }

    
    response = requests.get(url, headers=headers)

    if response.ok:
        # print(f"[bold green]Dataset Version details have been fetched")
        response_text = response.json()
        dataset_details = response_text["data"][0]
        # print(dataset_details)

        return dataset_details

    else:
        print(f"[bold red]Dataset details have not been found")
        return


def fetch(name: str, branch: str, version: str = "latest"):
    """This function fetches a dataset from the server and returns it as a dataframe object

    Parameters
    ----------
    name : str, optional
        The name of the dataset you want to fetch.
    version: str
        The version of the dataset

    Returns
    -------
        The dataset dataframe is being returned.

    """

    user_token = get_token()
    org_id = get_org_id()

    dataset_details = version_details(name=name, branch=branch, version=version)

    if dataset_details is None:
        print(f"[bold red]Unable to fetch Dataset version")
        return

    is_empty = dataset_details["is_empty"]

    if is_empty:
        print("[bold orange]Dataset file is not registered to the version")
        return

    storage_path = dataset_details["path"]["source_path"]
    storage_source_type = dataset_details["path"]["source_type"]["public_url"]

    dataset_url = urljoin(storage_source_type, storage_path)

    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Authorization": "Bearer {}".format(user_token),
    }

    # print('url', dataset_url)


    
    response = requests.get(dataset_url)

    if response.ok:
        dataset_bytes = response.content
        # open('temp_dataset.parquet', 'wb').write(dataset_bytes)
        # dataset = pd.read_parquet('temp_dataset.parquet')

        open("temp_dataset.pkl", "wb").write(dataset_bytes)
        dataset = joblib.load("temp_dataset.pkl")

        # print(f"[bold green]Dataset has been fetched")
        return dataset
    else:
        print(f"[bold red]Unable to fetch Dataset")
        # print(response.status_code)
        # print(response.text)
        # print(response.url)
        return


def delete(name: str, version: str = "latest") -> str:
    """This function deletes a dataset from the project

    Parameters
    ----------
    name : str
        The name of the dataset you want to delete
    version : str
        The version of the dataset to delete.

    """

    user_token = get_token()
    org_id = get_org_id()

    url = "org/{}/dataset/{}/delete".format(org_id, name)
    url = urljoin(BASE_URL, url)

    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Authorization": "Bearer {}".format(user_token),
    }

    data = {"version": version}

    data = json.dumps(data)

    
    response = requests.delete(url, headers=headers, data=data)

    if response.ok:
        print(f"[bold green]Dataset has been deleted")

    else:
        print(f"[bold red]Unable to delete Dataset")

    return response.text
