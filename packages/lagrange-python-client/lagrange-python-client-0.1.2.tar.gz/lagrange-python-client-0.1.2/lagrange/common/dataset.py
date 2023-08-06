import os

from mcs import APIClient, BucketAPI
from sqlalchemy import Integer, ForeignKey


class Dataset():
    def __init__(self, name, is_public, license, status, created_at, updated_at):
        self.name = name
        self.is_public = is_public
        self.status = status
        self.license = license
        self.created_at = created_at
        self.updated_at = updated_at

    def to_dict(self):
        return {
            "name": self.name,
            "is_public": self.is_public,
            "license": self.license,
            "status": self.status,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }
