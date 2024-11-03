import os
import tarfile
import json

def extract_tar_gz_to_json(tar_gz_path, output_dir):
    with tarfile.open(tar_gz_path, "r:gz") as tar:
        for member in tar.getmembers():
            if member.isfile():
                file_content = tar.extractfile(member).read().decode('utf-8')
                json_content = json.loads(file_content)
                output_file_path = os.path.join(output_dir, f"{os.path.splitext(member.name)[0]}.json")
                output_file_dir = os.path.dirname(output_file_path)
                if not os.path.exists(output_file_dir):
                    os.makedirs(output_file_dir)
                with open(output_file_path, 'w') as json_file:
                    json.dump(json_content, json_file, indent=4)

def process_samples_folder(samples_folder, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    for file_name in os.listdir(samples_folder):
        if file_name.endswith(".tar.gz"):
            tar_gz_path = os.path.join(samples_folder, file_name)
            extract_tar_gz_to_json(tar_gz_path, output_folder)

def test_single_file(tar_gz_path, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    extract_tar_gz_to_json(tar_gz_path, output_dir)

if __name__ == "__main__":
    # samples_folder = "./samples"
    # output_folder = "./output"
    # process_samples_folder(samples_folder, output_folder)
    
    tar_gz_path = "data/structured/structured-2018-04-08-proleague1.tar.gz"
    output_dir = "./output"
    test_single_file(tar_gz_path, output_dir)