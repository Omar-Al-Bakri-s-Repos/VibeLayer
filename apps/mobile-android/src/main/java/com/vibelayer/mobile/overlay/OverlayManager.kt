package com.vibelayer.mobile.overlay

import android.content.Context
import android.view.Surface
import com.airbnb.lottie.LottieAnimationView
import com.airbnb.lottie.LottieDrawable
import com.vibelayer.mobile.core.OpenGLESRenderer
import com.vibelayer.mobile.core.VulkanRenderer
import kotlinx.coroutines.CoroutineScope
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.launch

class OverlayManager(private val context: Context) {
    
    private val openGLRenderer = OpenGLESRenderer()
    private val vulkanRenderer = VulkanRenderer()
    private val lottieAnimations = mutableMapOf<String, LottieAnimationView>()
    
    private var isVulkanSupported = false
    
    init {
        isVulkanSupported = vulkanRenderer.initialize()
    }
    
    fun addLottieAnimation(name: String, assetName: String): LottieAnimationView {
        val animationView = LottieAnimationView(context)
        animationView.setAnimation(assetName)
        animationView.repeatCount = LottieDrawable.INFINITE
        lottieAnimations[name] = animationView
        return animationView
    }
    
    fun playAnimation(name: String) {
        lottieAnimations[name]?.playAnimation()
    }
    
    fun stopAnimation(name: String) {
        lottieAnimations[name]?.cancelAnimation()
    }
    
    fun renderFrame(surface: Surface) {
        CoroutineScope(Dispatchers.Main).launch {
            if (isVulkanSupported) {
                vulkanRenderer.render(surface)
            } else {
                // Fallback to OpenGL ES rendering
                // Note: This would need proper surface setup
            }
        }
    }
    
    fun destroy() {
        vulkanRenderer.destroy()
        lottieAnimations.clear()
    }
}
