import logging
import collections.abc

import synapse.lib.cell as s_cell
import synapse.lib.stormsvc as s_stormsvc

import synapse.tools.genpkg as s_genpkg

import synmods.examplepowerup.assets as svc_assets
import synmods.examplepowerup.version as svc_version

logger = logging.getLogger(__name__)

pkgfile = svc_assets.getAssetPath('synapse-examplepowerup.yaml')

class ExamplePowerupApi(s_stormsvc.StormSvc, s_cell.CellApi):
    _storm_svc_pkgs = (
        s_genpkg.tryLoadPkgProto(pkgfile, readonly=True),
    )
    _storm_svc_name = 'examplepowerup'
    _storm_svc_vers = svc_version.version

    async def getDnsByFqdn(self, fqdn):
        return await self.cell.getDnsByFqdn(fqdn)

    async def search(self, query):
        async for item in self.cell.search(query):
            yield item

class ExamplePowerup(s_cell.Cell):
    cellapi = ExamplePowerupApi

    confdefs = {
        'foo': {
            'type': 'string',
            'description': 'A foo configuration value.',
        },
    }

    COMMIT = svc_version.commit
    VERSION = svc_version.version
    VERSTRING = svc_version.verstring

    # Phase 2 of Cell startup. The nexus + service mirroring is not yet online.
    async def initServiceStorage(self):
        # Initialize any pre-nexus aware storage requirements.

        # Check for required config values
        self.foo = self.conf.reqConfValu('foo')

    # Phase 4 of Cell Startup. The nexus + service mirroring is now online.
    async def initServiceRuntime(self):
        # Initialize any runtime configuration that must be done after the
        # nexus has come online.
        pass

    async def getDnsByFqdn(self, fqdn: str) -> dict:
        '''
        An enrichment API.

        This expects a single value and returns a dictionary with results / success / error information.
        '''
        try:
            result = await self._getDnsByFqdn(fqdn)
        except Exception as e:
            logger.exception(f'Error getting DNS for {fqdn=}')
            return {
                'success': False,
                'mesg': str(e),
                'result': None
            }

        return {
            'success': True,
            'mesg': '',
            'result': result,
        }

    async def _getDnsByFqdn(self, fqdn: str) -> list[dict]:
        # Implement your data fetching here.
        result = [{
            'fqdn': 'foo.vertex.link',
            'ipv4': '1.2.3.4',
        }]
        return result

    async def search(self, query: str) -> collections.abc.AsyncGenerator[tuple[str, dict, dict], None, None]:
        '''
        A Search API.

        This yields message tuples to the caller containing <type>, <data>, and <info> values.

        Each message has a type of "data", "print", or "warn".
        '''

        try:
            async for mesg in self._search(query):
                yield mesg
        except Exception as e:
            logger.exception(f'Error searching {query=}')
            yield 'warn', {}, {'mesg': str(e)}

    async def _search(self, query: str) -> collections.abc.AsyncGenerator[tuple[str, dict, dict], None, None]:
        yield 'print', {}, {'mesg': f'Executing query: {query}'}

        data = {
            'fqdn': 'foo.vertex.link',
            'ipv4': '1.2.3.4',
        }

        yield 'data', data, {}
