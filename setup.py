from setuptools import find_packages, setup

sorl_thumbnail_version = "sorl-thumbnail>=12.4.1,<12.5"
easy_thumbnails_version = "easy-thumbnails==2.5"

test_requires = [
    "WebTest>=2.0,<2.1",
    "django-webtest==1.9.4",
    "py>=1.4.31",
    "psycopg2>=2.7,<2.8",
    "pytest>=4.0,<4.5",
    "pytest-django==3.4.8",
    sorl_thumbnail_version,
    easy_thumbnails_version,
]

setup(
    name="django-oscar-promotions",
    version="1.0",
    url="https://github.com/oscaro/django-oscar-promotins",
    author="Oscar Team",
    author_email="sasha@metaclass.co",
    description="Promotions for Django Oscar",
    long_description=open("README.rst").read(),
    license="BSD",
    packages=find_packages(exclude=["sandbox*", "tests*"]),
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Web Environment",
        "Framework :: Django",
        "Framework :: Django :: 2.0",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: Unix",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
    ],
    install_requires=["django>=1.11,<2.3", "django-oscar>=2.0"],
    extras_require={
        "test": test_requires,
        "sorl-thumbnail": [sorl_thumbnail_version],
        "easy-thumbnails": [easy_thumbnails_version],
    },
    test_requires=test_requires,
)
