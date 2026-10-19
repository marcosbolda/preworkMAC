package com.marcos.ocultarnotif

import android.content.ComponentName
import android.content.Context
import android.content.SharedPreferences
import android.provider.Settings

/** Configuración compartida entre la pantalla, el servicio y el mosaico. */
object Prefs {
    private const val FILE = "config"
    const val KEY_ENABLED = "enabled"
    const val KEY_BLOCKED = "blocked_packages"
    const val KEY_HIDDEN_COUNT = "hidden_count"

    fun get(context: Context): SharedPreferences =
        context.applicationContext.getSharedPreferences(FILE, Context.MODE_PRIVATE)

    fun isEnabled(context: Context) = get(context).getBoolean(KEY_ENABLED, false)

    fun setEnabled(context: Context, enabled: Boolean) =
        get(context).edit().putBoolean(KEY_ENABLED, enabled).apply()

    fun blockedPackages(context: Context): Set<String> =
        get(context).getStringSet(KEY_BLOCKED, emptySet())!!.toSet()

    fun setBlocked(context: Context, pkg: String, blocked: Boolean) {
        val set = blockedPackages(context).toMutableSet()
        if (blocked) set.add(pkg) else set.remove(pkg)
        get(context).edit().putStringSet(KEY_BLOCKED, set).apply()
    }

    fun hiddenCount(context: Context) = get(context).getInt(KEY_HIDDEN_COUNT, 0)

    fun incrementHiddenCount(context: Context) {
        val prefs = get(context)
        prefs.edit().putInt(KEY_HIDDEN_COUNT, prefs.getInt(KEY_HIDDEN_COUNT, 0) + 1).apply()
    }

    fun shouldHide(context: Context, pkg: String) =
        isEnabled(context) && pkg in blockedPackages(context)

    fun hasListenerPermission(context: Context): Boolean {
        val flat = Settings.Secure.getString(
            context.contentResolver, "enabled_notification_listeners"
        ) ?: return false
        val me = ComponentName(context, BlockerService::class.java)
        return flat.split(":").any { ComponentName.unflattenFromString(it) == me }
    }
}
