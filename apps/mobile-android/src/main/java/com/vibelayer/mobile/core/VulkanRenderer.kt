package com.vibelayer.mobile.core

import android.view.Surface

class VulkanRenderer {
    private external fun nativeInit(): Long
    private external fun nativeDestroy(handle: Long)
    private external fun nativeRender(handle: Long, surface: Surface)
    
    private var nativeHandle: Long = 0
    
    companion object {
        init {
            System.loadLibrary("vibelayer_native")
        }
    }
    
    fun initialize(): Boolean {
        nativeHandle = nativeInit()
        return nativeHandle != 0L
    }
    
    fun destroy() {
        if (nativeHandle != 0L) {
            nativeDestroy(nativeHandle)
            nativeHandle = 0
        }
    }
    
    fun render(surface: Surface) {
        if (nativeHandle != 0L) {
            nativeRender(nativeHandle, surface)
        }
    }
}
