"""User facing entry point for pathlesstaken for anyone running the
code from the repository and not pypi.
"""

from src.demystify import demystify


def main():
    """Primary entry point for this script."""
    demystify.main()


if __name__ == "__main__":
    main()
