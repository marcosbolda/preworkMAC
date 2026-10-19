package com.marcos.ocultarnotif

import android.service.quicksettings.Tile
import android.service.quicksettings.TileService

/** Mosaico de ajustes rápidos para activar/desactivar sin abrir la app. */
class ToggleTileService : TileService() {

    override fun onStartListening() = refresh()

    override fun onClick() {
        Prefs.setEnabled(this, !Prefs.isEnabled(this))
        refresh()
    }

    private fun refresh() {
        val tile = qsTile ?: return
        tile.state = if (Prefs.isEnabled(this)) Tile.STATE_ACTIVE else Tile.STATE_INACTIVE
        tile.updateTile()
    }
}
