package com.kidiplay.app.ui.home

enum class HomeLayout {
    Compact,
    Expanded,
}

data class HomePresentation(
    val layout: HomeLayout,
    val backgroundAsset: String,
)

fun homePresentation(widthDp: Int, heightDp: Int): HomePresentation {
    val layout = if (widthDp >= 700) HomeLayout.Expanded else HomeLayout.Compact
    val background = if (widthDp > heightDp) {
        "workshop-garden-landscape-v01.png"
    } else {
        "workshop-garden-portrait-v01.png"
    }
    return HomePresentation(layout = layout, backgroundAsset = background)
}
