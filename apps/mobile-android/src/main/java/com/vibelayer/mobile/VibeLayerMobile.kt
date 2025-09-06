package com.vibelayer.mobile

import android.content.Context

object VibeLayerMobile {
    const val VERSION = "1.0.0"
    
    fun initialize(context: Context) {
        // Initialize VibeLayer mobile SDK
        println("VibeLayer Mobile Android SDK v$VERSION initialized")
    }
}
