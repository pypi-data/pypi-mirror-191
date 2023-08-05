"""
Copyright (c) 2023 MEEO s.r.l.

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""


import os
import logging
logger=logging.getLogger('adamapi')

from . import AdamApiError

class Datasets():
    def __init__(self, client):
        self.client = client
        self.LOG = logger

    def getDatasets(self, datasetId=None, **kwargs):
        """
        Dataset Catalogue Search
        @ datasetId, the datase identifier as resource_id:dataseId or the dataset oid (_id["$oid"])
        """

        params={}
        params["client"]="adamapi"
        if datasetId is not None:
            resource_id = datasetId.split(":")[0]
            url=os.path.join("apis", "v2", "datasets", resource_id )
        else:
            url=os.path.join("apis", "v2", "datasets")

        params['startIndex']=kwargs.get('startIndex', 0)
        params['maxRecords']=kwargs.get('maxRecords', 10)

        r = self.client.client( url, params, 'GET' )
        self.LOG.info( 'Datasets request executed' )
        response = r.json()
        return response
