package com.marcos.ocultarnotif

import android.app.Activity
import android.content.Intent
import android.content.SharedPreferences
import android.content.pm.PackageManager
import android.graphics.drawable.Drawable
import android.os.Bundle
import android.provider.Settings
import android.text.Editable
import android.text.TextWatcher
import android.view.View
import android.view.ViewGroup
import android.widget.BaseAdapter
import android.widget.Button
import android.widget.CheckBox
import android.widget.EditText
import android.widget.ImageView
import android.widget.ListView
import android.widget.Switch
import android.widget.TextView

class MainActivity : Activity(), SharedPreferences.OnSharedPreferenceChangeListener {

    private data class AppEntry(val label: String, val pkg: String, val icon: Drawable)

    private lateinit var permissionBox: View
    private lateinit var masterSwitch: Switch
    private lateinit var statusText: TextView
    private lateinit var countText: TextView
    private lateinit var adapter: AppAdapter

    private var allApps: List<AppEntry> = emptyList()

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)

        permissionBox = findViewById(R.id.permissionBox)
        masterSwitch = findViewById(R.id.masterSwitch)
        statusText = findViewById(R.id.statusText)
        countText = findViewById(R.id.countText)

        findViewById<Button>(R.id.grantButton).setOnClickListener {
            startActivity(Intent(Settings.ACTION_NOTIFICATION_LISTENER_SETTINGS))
        }

        masterSwitch.setOnCheckedChangeListener { _, checked ->
            if (checked != Prefs.isEnabled(this)) Prefs.setEnabled(this, checked)
        }

        adapter = AppAdapter()
        val list = findViewById<ListView>(R.id.appList)
        list.adapter = adapter
        list.setOnItemClickListener { _, _, position, _ ->
            val app = adapter.getItem(position)
            Prefs.setBlocked(this, app.pkg, app.pkg !in Prefs.blockedPackages(this))
        }

        findViewById<EditText>(R.id.searchBox).addTextChangedListener(object : TextWatcher {
            override fun beforeTextChanged(s: CharSequence?, a: Int, b: Int, c: Int) {}
            override fun onTextChanged(s: CharSequence?, a: Int, b: Int, c: Int) {}
            override fun afterTextChanged(s: Editable?) = adapter.filter(s?.toString().orEmpty())
        })

        loadApps()
    }

    override fun onResume() {
        super.onResume()
        Prefs.get(this).registerOnSharedPreferenceChangeListener(this)
        refreshUi()
    }

    override fun onPause() {
        super.onPause()
        Prefs.get(this).unregisterOnSharedPreferenceChangeListener(this)
    }

    override fun onSharedPreferenceChanged(prefs: SharedPreferences, key: String?) {
        runOnUiThread { refreshUi() }
    }

    private fun refreshUi() {
        permissionBox.visibility =
            if (Prefs.hasListenerPermission(this)) View.GONE else View.VISIBLE

        val enabled = Prefs.isEnabled(this)
        masterSwitch.isChecked = enabled
        val blocked = Prefs.blockedPackages(this)
        statusText.text = if (enabled) {
            getString(R.string.status_on, blocked.size)
        } else {
            getString(R.string.status_off)
        }
        statusText.setTextColor(if (enabled) 0xFF2E7D32.toInt() else 0xFF757575.toInt())
        countText.text = getString(R.string.hidden_count, Prefs.hiddenCount(this))
        adapter.notifyDataSetChanged()
    }

    private fun loadApps() {
        Thread {
            val pm = packageManager
            val launcher = Intent(Intent.ACTION_MAIN).addCategory(Intent.CATEGORY_LAUNCHER)
            val apps = pm.queryIntentActivities(launcher, PackageManager.MATCH_ALL)
                .map { it.activityInfo.applicationInfo }
                .filter { it.packageName != packageName }
                .distinctBy { it.packageName }
                .map { AppEntry(it.loadLabel(pm).toString(), it.packageName, it.loadIcon(pm)) }
                .sortedBy { it.label.lowercase() }
            runOnUiThread {
                allApps = apps
                adapter.filter(findViewById<EditText>(R.id.searchBox).text.toString())
            }
        }.start()
    }

    private inner class AppAdapter : BaseAdapter() {
        private var shown: List<AppEntry> = emptyList()

        fun filter(query: String) {
            val q = query.trim().lowercase()
            val blocked = Prefs.blockedPackages(this@MainActivity)
            // Las apps ya elegidas aparecen primero.
            shown = allApps
                .filter { q.isEmpty() || q in it.label.lowercase() || q in it.pkg }
                .sortedByDescending { it.pkg in blocked }
            notifyDataSetChanged()
        }

        override fun getCount() = shown.size
        override fun getItem(position: Int) = shown[position]
        override fun getItemId(position: Int) = position.toLong()

        override fun getView(position: Int, convertView: View?, parent: ViewGroup): View {
            val view = convertView ?: layoutInflater.inflate(R.layout.item_app, parent, false)
            val app = shown[position]
            view.findViewById<ImageView>(R.id.appIcon).setImageDrawable(app.icon)
            view.findViewById<TextView>(R.id.appName).text = app.label
            view.findViewById<TextView>(R.id.appPackage).text = app.pkg
            view.findViewById<CheckBox>(R.id.appCheck).isChecked =
                app.pkg in Prefs.blockedPackages(this@MainActivity)
            return view
        }
    }
}
