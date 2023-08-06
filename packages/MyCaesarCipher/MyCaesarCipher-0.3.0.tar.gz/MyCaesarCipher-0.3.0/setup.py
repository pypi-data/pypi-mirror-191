import pathlib
from setuptools import setup, find_packages

readme = pathlib.Path("readme.md").read_text()
reqs = pathlib.Path("requirements.txt").read_text()
setup(name="MyCaesarCipher",
      version="0.3.0",
      description=
      'Simple cryptographic substitution-based cipher for encoding plaintext.',
      url='https://github.com/schlopp96/MyCaesarCipher',
      author='schlopp96',
      author_email='schloppdaddy@gmail.com',
      long_description=readme,
      long_description_content_type='text/markdown',
      packages=find_packages(),
      include_package_data=True,
      install_requires=[reqs],
      classifiers=[
          "Development Status :: 3 - Alpha",
          "Intended Audience :: Developers",
          "Intended Audience :: End Users/Desktop",
          "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
          "Natural Language :: English",
          "Operating System :: Microsoft :: Windows",
          "Programming Language :: Python :: 3",
          "Programming Language :: Python :: 3.9",
          "Programming Language :: Python :: 3.10",
          "Programming Language :: Python :: 3.11",
          "Topic :: Software Development :: Libraries :: Python Modules",
          "Topic :: Security :: Cryptography",
          "Topic :: Utilities",
      ],
      keywords=[
          'cryptography', 'Caesar-Cipher', 'Caesar', 'Cipher', 'encryption',
          'decryption', 'cryptographic', 'module', 'script', 'python'
      ])
