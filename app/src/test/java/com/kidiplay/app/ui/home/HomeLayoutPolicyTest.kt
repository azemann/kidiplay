package com.kidiplay.app.ui.home

import org.junit.Assert.assertEquals
import org.junit.Test

class HomeLayoutPolicyTest {
    @Test
    fun closedFoldUsesCompactPortraitPresentation() {
        assertEquals(
            HomePresentation(
                layout = HomeLayout.Compact,
                backgroundAsset = "workshop-garden-portrait-v01.png",
            ),
            homePresentation(widthDp = 412, heightDp = 915),
        )
    }

    @Test
    fun openFoldUsesExpandedLandscapePresentation() {
        assertEquals(
            HomePresentation(
                layout = HomeLayout.Expanded,
                backgroundAsset = "workshop-garden-landscape-v01.png",
            ),
            homePresentation(widthDp = 904, heightDp = 752),
        )
    }

    @Test
    fun expandedPortraitWindowKeepsPortraitBackground() {
        assertEquals(
            HomePresentation(
                layout = HomeLayout.Expanded,
                backgroundAsset = "workshop-garden-portrait-v01.png",
            ),
            homePresentation(widthDp = 800, heightDp = 1200),
        )
    }
}
