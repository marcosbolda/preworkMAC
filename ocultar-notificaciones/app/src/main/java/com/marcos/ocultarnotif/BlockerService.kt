package com.marcos.ocultarnotif

import android.content.SharedPreferences
import android.service.notification.NotificationListenerService
import android.service.notification.StatusBarNotification

/**
 * Recibe todas las notificaciones del sistema y borra al instante las de las apps
 * elegidas mientras el interruptor esté activo.
 */
class BlockerService : NotificationListenerService(),
    SharedPreferences.OnSharedPreferenceChangeListener {

    override fun onListenerConnected() {
        Prefs.get(this).registerOnSharedPreferenceChangeListener(this)
        clearActive()
    }

    override fun onListenerDisconnected() {
        Prefs.get(this).unregisterOnSharedPreferenceChangeListener(this)
    }

    override fun onNotificationPosted(sbn: StatusBarNotification) {
        if (Prefs.shouldHide(this, sbn.packageName)) {
            cancelNotification(sbn.key)
            Prefs.incrementHiddenCount(this)
        }
    }

    // Al activar el interruptor o agregar una app, limpiamos las que ya estaban visibles.
    override fun onSharedPreferenceChanged(prefs: SharedPreferences, key: String?) {
        if (key == Prefs.KEY_ENABLED || key == Prefs.KEY_BLOCKED) clearActive()
    }

    private fun clearActive() {
        val active = try {
            activeNotifications
        } catch (e: SecurityException) {
            null
        } ?: return
        for (sbn in active) {
            if (Prefs.shouldHide(this, sbn.packageName)) cancelNotification(sbn.key)
        }
    }
}
