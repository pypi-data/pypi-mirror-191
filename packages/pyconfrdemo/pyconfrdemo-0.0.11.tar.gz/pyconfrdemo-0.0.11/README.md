# PyConFR 2023: "Introduction to Sigstore: cryptographic signatures made easier" demo

This repository hosts the demo of the `sigstore-python` client from the talk "Introduction to Sigstore: cryptographic signatures made easier" presented at PyCon France 2023.

In this demo, we will sign a package with the `sigstore-python` GitHub Action, publish it to PyPI and then verify the signature on download using the client command line interface.

## Running the sign and publish workflow

First ensure you have a PyPI [API token](https://pypi.org/help/#apitoken) configured on your repository fork to upload your package to PyPI on a new release. See the [Encrypted Secrets section](https://docs.github.com/en/actions/security-guides/encrypted-secrets) of the GitHub documentation for adding secrets to your repository.

The workflow is triggered on a new project release. The workflow executes the following steps:
- Generate a `checksums.txt` file containing sha256 hashes for all the files contained in the project
- Sign `checksums.txt` and generate Sigstore verification materials: `checksums.txt.sig`, `checksums.txt.crt`, `checksums.txt.bundle`
- Commit and push the newly created files to the repository
- Build the project in a Python package and upload it to PyPI

### Testing the workflow locally

[`nektos/act`](https://github.com/nektos/act) is used to run the GitHub Action workflow locally. Run the command `act` in the repository root to test the action.

**Note:** If `act` has an issue finding the specified Python version for your architecture, run the `act` command with the `-P ubuntu-latest=ghcr.io/catthehacker/ubuntu:act-latest` argument. This workaround will pull a medium-sized image where Python should be installed normally (see the following [`nektos/act` GitHub issue](https://github.com/nektos/act/issues/251) for more information).

