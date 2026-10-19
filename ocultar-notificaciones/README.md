# Ocultar Notificaciones (Android)

App que oculta las notificaciones de las apps que elijas, mientras vos quieras.

## Cómo funciona
- Elegís las apps de la lista (tocá una para marcarla/desmarcarla).
- Activás el interruptor **Ocultar notificaciones** (o el mosaico **Ocultar notif.** en los ajustes rápidos).
- Mientras esté activo, cada notificación de esas apps se borra apenas llega. Al apagarlo, todo vuelve a la normalidad.

> Las notificaciones ocultadas se descartan (no se guardan). Los mensajes siguen estando dentro de cada app.

## Obtener el APK
GitHub Actions lo compila en cada push: pestaña **Actions** → workflow **Compilar APK** → última ejecución → artefacto **OcultarNotificaciones-apk** (zip con `app-debug.apk`).

Para compilar localmente con Android Studio / SDK: `./gradlew assembleDebug`.

## Instalación
1. Instalá el APK (permití "instalar apps de origen desconocido").
2. Abrí la app y tocá **Dar permiso** → activá *Ocultar Notificaciones* en "Acceso a notificaciones".
3. **Android 13+**: si el permiso aparece bloqueado, andá a Ajustes → Apps → Ocultar Notificaciones → menú ⋮ → **Permitir ajustes restringidos**, y repetí el paso 2.
4. Para el mosaico rápido: bajá la cortina, editar mosaicos y arrastrá **Ocultar notif.**
