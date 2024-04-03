import logging

import synmods.examplepowerup.service as s_service

import synmods.examplepowerup.tests.common as t_common

logger = logging.getLogger(__name__)

srcguid = '3faafd06b11d05ed4f8a126236de63c3'

class TestService(t_common.TstBase):

    async def test_service_basic(self):
        svc_conf = {
            'foo': 'bar',
        }

        async with self.get_test_core(svc_conf) as (core, prox, svc):

            self.isinstance(svc, s_service.ExamplePowerup)

            # Basic telepath API works - this should be changed by the implementer.
            async with svc.getLocalProxy() as svc_prox:
                resp = await svc_prox.getDnsByFqdn('vertex.link')
            self.isinstance(resp, dict)
            self.eq(set(resp.keys()),
                    {'success', 'mesg', 'result'})

            # meta:source node is made
            await core.nodes('$mod=$lib.import(examplepowerup.ingest) $mod.initMetaSource()')
            opts = {'vars': {'guid': srcguid}}
            nodes = await core.nodes('meta:source=$guid', opts=opts)
            self.len(1, nodes)
            logger.debug('Found meta:source node')

            # basic storm commands - this should be changed by the implementer.
            self.len(1, await core.nodes('[ inet:fqdn=vertex.link ] | examplepowerup.enrich --yield'))
            self.len(1, await core.nodes('examplepowerup.search lol --yield'))

            # Example of enriching an unsupported node type
            msgs = await core.stormlist('[inet:asn=0] | examplepowerup.enrich --debug')
            self.stormIsInPrint('enrich() skipping node inet:asn=0', msgs)
