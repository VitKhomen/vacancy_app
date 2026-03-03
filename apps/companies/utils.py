import os


def company_logos_upload_path(instance, filename):
    return os.path.join("company_logos", str(instance.owner.id), filename)
