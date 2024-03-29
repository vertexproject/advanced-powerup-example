import os
import json
import logging
import contextlib

from typing import Union

import vcr

import synapse.cortex as s_cortex
import synapse.tests.utils as s_t_utils

import synmods.examplepowerup.service as s_service

TESTDIR = os.path.split(__file__)[0]
ASSETDIR = os.path.join(TESTDIR, 'assets')

log = logging.getLogger(__name__)
logging.getLogger('vcr').setLevel(logging.ERROR)

class TstBase(s_t_utils.SynTest):
    '''
    Test helper class.

    VCR is used by default for recording cassettes when creating a test cortex and
    service using the get_test_core method.

    To set test-wide VCR configuration attributes, set the class attribute "vcr_kwargs" as needed.
    These follow the vcr.VCR(**kwargs) convention. See https://vcrpy.readthedocs.io/en/latest/
    for more information.
    '''
    def getAssetPath(self, name: str) -> str:
        '''
        Get the path to a test asset.
        '''
        fp = os.path.join(ASSETDIR, name)
        assert os.path.isfile(fp)
        return fp

    def getAssetBytes(self, name: str) -> bytes:
        '''
        Get the bytes for a test asset.
        '''
        fp = self.getAssetPath(name)
        with open(fp, 'rb') as f:
            byts = f.read()
        return byts

    def getAssetJson(self, name) -> Union[str | int | bool | dict | list | None]:
        '''
        Get the JSON for a test asset.
        '''
        byts = self.getAssetBytes(name)
        obj = json.loads(byts.decode())
        return obj

    def _getVcrArgs(self):
        kwargs = getattr(self, 'vcr_kwargs', {})
        return kwargs

    def getVcr(self, **kwargs) -> vcr.cassette.Cassette:
        '''
        Get a VCR cassette. This should be used as a context manager.
        '''
        # simplification from the vcr-unittest library.
        fn = '{0}.{1}.yaml'.format(self.__class__.__name__,
                                   self._testMethodName)
        fp = os.path.join(ASSETDIR, fn)
        _kwargs = self._getVcrArgs()
        _kwargs.update(kwargs)
        myvcr = vcr.VCR(**_kwargs)
        cm = myvcr.use_cassette(fp)
        return cm

    @contextlib.asynccontextmanager
    async def get_test_core(self,
                            ssvc_conf: Union[dict | None] =None,
                            core_conf: Union[dict | None] =None,
                            vcrargs: Union[dict | None] =None,
                            ) -> contextlib.AbstractAsyncContextManager[tuple[s_cortex.Cortex, s_cortex.CoreApi, s_service.ExamplePowerup], None, None]:
        '''
        Get a test cortex, cortex proxy, and a service object.

        ssvc_conf: This is an optional set of configuration information for the Storm Service.
        core_conf: This is an optional set of configuration information for the Cortex.
        vcrargs: This is an optional set of configuration data for the VCR object.
        '''
        if vcrargs is None:
            vcrargs = {}

        if ssvc_conf is None:
            ssvc_conf = {}

        async with self.getTestCoreProxSvc(s_service.ExamplePowerup,
                                           ssvc_conf=ssvc_conf,
                                           core_conf=core_conf,
        ) as (core, prox, svc):

            with self.getVcr(**vcrargs):
                yield core, prox, svc
