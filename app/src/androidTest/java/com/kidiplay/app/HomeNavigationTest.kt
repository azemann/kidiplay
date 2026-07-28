package com.kidiplay.app

import androidx.compose.ui.test.assertIsDisplayed
import androidx.compose.ui.test.junit4.createAndroidComposeRule
import androidx.compose.ui.test.onNodeWithTag
import androidx.compose.ui.test.performClick
import org.junit.Rule
import org.junit.Test

class HomeNavigationTest {
    @get:Rule
    val composeRule = createAndroidComposeRule<MainActivity>()

    @Test
    fun drawingCardOpensPlaceholderAndReturnsHome() {
        composeRule.onNodeWithTag("home-screen").assertIsDisplayed()
        composeRule.onNodeWithTag("activity-drawing").performClick()
        composeRule.onNodeWithTag("destination-drawing").assertIsDisplayed()
        composeRule.onNodeWithTag("back-home").performClick()
        composeRule.onNodeWithTag("home-screen").assertIsDisplayed()
    }
}
