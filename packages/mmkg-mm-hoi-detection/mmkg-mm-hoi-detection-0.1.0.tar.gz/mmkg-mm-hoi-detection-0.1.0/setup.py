from pathlib import Path
from setuptools import find_packages, setup

import torch

PROJECT_NAME = "mmkg-mm-hoi-detection"
PACKAGE_NAME = PROJECT_NAME.replace("-", "_")
DESCRIPTION = "MMKG Models"

TORCH_VERSION = [int(x) for x in torch.__version__.split(".")[:2]]
assert TORCH_VERSION >= [1, 7], "Requires PyTorch >= 1.8"


if __name__ == "__main__":
    version = "0.1.0"

    print(f"Building {PROJECT_NAME}-{version}")
    #print(find_packages(where='/data/wangzp/zheda/mmkg-mm-hoi-detection',exclude=("tests",)))
    #assert False
    setup(
        name=PROJECT_NAME,
        version=version,
        author="Zhipin Wang",
        author_email="zpwang99@foxmail.com",
        #url=f"https://github.com/vivym/{PROJECT_NAME}",
        #download_url=f"https://github.com/vivym/{PROJECT_NAME}/tags",
        description=DESCRIPTION,
        long_description=Path("README.md").read_text(),
        long_description_content_type="text/markdown",
        packages=find_packages(exclude=("tests",)),
        package_data={PACKAGE_NAME: ["*.dll", "*.so", "*.dylib","*.txt.gz","*.txt",]},
        zip_safe=False,
        python_requires=">=3.7",
        install_requires=[
            "pillow",
            "cython",
            "pycocotools",
            "aiofiles",
            "fastapi",
            "uvicorn[standard]",
            "scipy",
            "ftfy",
            "regex",
            "tqdm",
        ],
        include_package_data = True
    )

