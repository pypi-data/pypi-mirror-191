from distutils.core import setup

setup(
    name='orzorng',  # How you named your package folder (MyLib)
    packages=['orzorng'],  # Chose the same as "name"
    include_package_data=True,
    # exclude_package_date={'': ['.gitignore']},
    # zip_safe=False,
    version='0.0.5',  # Start with a small number and increase it with every change you make
    license='MIT',  # Chose a license from here: https://help.github.com/articles/licensing-a-repository
    description='learn to use',  # Give a short description about your library
    author='hugo',  # Type in your name
    author_email='orzorng@gmail.com',  # Type in your E-Mail
    url='https://github.com/irnp/orzorng',  # Provide either the link to your github or to your website
    # download_url='',  # I explain this later on
    keywords=['orzorng', 'hugo'],  # Keywords that define your package best
    install_requires=[  # I get to this in a second
        'requests',  # 可以加上版本号，如validators=1.5.1
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
        'Intended Audience :: Developers',  # Define that your audience are developers
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',  # Again, pick a license
        'Programming Language :: Python :: 3',  # Specify which pyhton versions that you want to support
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
)
