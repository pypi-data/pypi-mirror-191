from distutils.core import setup

version = 'v0.0.6'

setup(
    name='cdj_minecraft',
    packages=['cdj_minecraft'],
    version=version,
    license='MIT',
    description='Een minecraft wrapper bovenop de mineflayer wrapper gemaakt voor CoderDojo Zwalm',
    author='Arthurdw',
    author_email='dev@arthurdw.com',
    url='https://github.com/Arthurdw/CoderdojoMinecraft',
    download_url=f'https://github.com/Arthurdw/CoderdojoMinecraft/archive/version.tar.gz',
    keywords=['Minecraft', 'CoderDojo', 'Python', 'Wrapper', 'Bot', 'Mineflayer'],
    install_requires=['javascript'],
    classifiers=[
        'Development Status :: 3 - Alpha',  # "3 - Alpha", "4 - Beta" or "5 - Production/Stable"
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
    ],
)
