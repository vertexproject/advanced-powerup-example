import synmods.examplepowerup.assets as s_assets
import synmods.examplepowerup.tests.common as t_common

class TestAssets(t_common.TstBase):
    def test_module_assets(self):
        assets = s_assets.getAssets()
        self.isin('synapse-examplepowerup.yaml', assets)

        s = s_assets.getAssetStr('synapse-examplepowerup.yaml')
        self.isinstance(s, str)

        data = s_assets.getAssetJson('file.json')
        self.eq(data, {'key': 'value'})

        self.raises(ValueError, s_assets.getAssetPath, 'newp.bin')
        self.raises(ValueError, s_assets.getAssetPath,
                    '../../../../../../../../../etc/passwd')

    def test_tcommon_assets(self):
        data = self.getAssetJson('test_asset.json')
        self.eq(data, {'key': 'value'})
