#
# This file is part of the BIOM_AID distribution (https://bitbucket.org/kig13/dem/).
# Copyright (c) 2020-2021 Brice Nord, Romuald Kliglich, Alexandre Jaborska, Philomène Mazand.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, version 3.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#
import os
from hashlib import md5

from common import config
from document.models import Document


def document_get_or_create(file_data, owner, doc_type, description=None):

    hash = md5()
    for chunk in file_data.chunks():
        hash.update(chunk)

    # TODO : Check if a index is needed on 'hash' field => checked on 2022/05/26 : Yes, it's needed !!
    qs = Document.objects.filter(hash=hash.hexdigest())
    if qs.exists():
        physical_path = qs[0].physical_path
        file_exists = True
    else:
        physical_path = file_data.name
        base, sep = os.path.splitext(file_data.name)
        count = 1
        while os.path.exists(os.path.join(config.settings.MEDIA_ROOT, physical_path)):
            count += 1
            physical_path = '{}-{}{}'.format(base, count, sep)
        file_exists = False

    document = Document(
        physical_path=physical_path,
        logical_path=file_data.name,
        owner=owner,
        description=description,
        doc_type=doc_type,
        hash=hash.hexdigest(),
        mime_type=file_data.content_type,
    )

    # Save document on disk
    if not file_exists:
        with open(os.path.join(config.settings.MEDIA_ROOT, physical_path), 'wb') as f:
            for chunk in file_data.chunks():
                f.write(chunk)

    # Save document meta/record
    document.save()

    return document


def document_delete(pk):
    ...
