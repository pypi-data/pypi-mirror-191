from pathlib import Path
from typing import Any, Callable

from ververser.reloading_asset import ReloadingAsset, ReloadStatus


AssetLoaderType = Callable[ [ Path ], Any ]


class AssetManager:

    def __init__( self, asset_folder_path : Path ):
        self.asset_folder_path = asset_folder_path
        self.asset_loaders = []
        self.assets = []

    def make_asset_path_complete( self, asset_path : Path ) -> Path:
        return self.asset_folder_path / asset_path

    def register_asset_loader( self, postfix : str, f_load_asset : AssetLoaderType ) -> None:
        self.asset_loaders.append( ( postfix, f_load_asset ) )

    def get_asset_loader_for_file( self, file_path : Path ) -> AssetLoaderType:
        # reverse search through all registered loaders
        # this way. newest registered loaders overrule older ones
        for postfix, asset_loader in reversed( self.asset_loaders ):
            if str( file_path ).endswith( postfix ):
                return asset_loader
        assert False, f'No asset loader found for file_path: "{file_path}". Known loaders: {self.asset_loaders}'

    def try_reload( self ) -> ReloadStatus:
        overall_reload_status = ReloadStatus.NOT_CHANGED
        for reloading_asset in self.assets:
            reload_status = reloading_asset.try_reload()
            if reload_status == ReloadStatus.RELOADED:
                overall_reload_status = ReloadStatus.RELOADED
            if reload_status == ReloadStatus.FAILED:
                return ReloadStatus.FAILED
        return overall_reload_status

    def exists( self, asset_path : Path ):
        complete_asset_path = self.make_asset_path_complete( asset_path )
        return complete_asset_path.is_file()

    def load( self, asset_path : Path ) -> ( Any, ReloadStatus ):
        absolute_asset_path = self.make_asset_path_complete( asset_path )
        assert self.exists( absolute_asset_path ), f'Could not load asset. File path: "{asset_path}"'
        asset_loader = self.get_asset_loader_for_file( asset_path )
        reloading_asset = ReloadingAsset(
            f_load_asset = lambda path : asset_loader( path ),
            file_path = absolute_asset_path
        )
        self.assets.append(reloading_asset)
        load_status = reloading_asset.try_reload()
        return reloading_asset, load_status
