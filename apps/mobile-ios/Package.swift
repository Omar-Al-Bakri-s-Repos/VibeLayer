// swift-tools-version: 5.9
import PackageDescription

let package = Package(
    name: "VibeLayerMobile",
    platforms: [
        .iOS(.v17)
    ],
    products: [
        .library(
            name: "VibeLayerMobile",
            targets: ["VibeLayerMobile"]
        ),
    ],
    dependencies: [
        .package(url: "https://github.com/airbnb/lottie-ios.git", from: "4.4.0"),
        .package(url: "https://github.com/apple/swift-algorithms", from: "1.2.0"),
        .package(url: "https://github.com/apple/swift-collections", from: "1.0.0")
    ],
    targets: [
        .target(
            name: "VibeLayerMobile",
            dependencies: [
                .product(name: "Lottie", package: "lottie-ios"),
                .product(name: "Algorithms", package: "swift-algorithms"),
                .product(name: "Collections", package: "swift-collections")
            ],
            path: "Sources"
        ),
        .testTarget(
            name: "VibeLayerMobileTests",
            dependencies: ["VibeLayerMobile"],
            path: "Tests"
        ),
    ]
)
