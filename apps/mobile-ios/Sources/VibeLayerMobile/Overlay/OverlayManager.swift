import Foundation
import Lottie
import Metal

public class OverlayManager: ObservableObject {
    private let metalRenderer: MetalRenderer
    private var lottieAnimations: [String: LottieAnimation] = [:]
    
    @Published public var isActive: Bool = false
    
    public init() {
        self.metalRenderer = MetalRenderer()
    }
    
    public func addLottieAnimation(named name: String, path: String) {
        let animation = LottieAnimation.named(name)
        lottieAnimations[name] = animation
    }
    
    public func playAnimation(named name: String) {
        // Implementation for playing Lottie animations
    }
    
    public func stopAnimation(named name: String) {
        // Implementation for stopping Lottie animations
    }
    
    public func renderFrame(to drawable: CAMetalDrawable) {
        metalRenderer.render(to: drawable)
    }
}
