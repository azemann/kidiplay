package com.kidiplay.app.ui.theme

import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.lightColorScheme
import androidx.compose.runtime.Composable
import androidx.compose.ui.graphics.Color

val PaperCream = Color(0xFFFFF9E8)
val WarmWhite = Color(0xFFFFFDF7)
val Sunshine = Color(0xFFFFD54F)
val SoftOrange = Color(0xFFFFB74D)
val SkyBlue = Color(0xFF81D4FA)
val LeafGreen = Color(0xFFAED581)
val PowderPink = Color(0xFFF8BBD0)
val InkBrown = Color(0xFF4B3B2A)

private val KidiPlayColors = lightColorScheme(
    primary = Sunshine,
    onPrimary = InkBrown,
    secondary = SkyBlue,
    onSecondary = InkBrown,
    tertiary = LeafGreen,
    onTertiary = InkBrown,
    background = PaperCream,
    onBackground = InkBrown,
    surface = WarmWhite,
    onSurface = InkBrown,
)

@Composable
fun KidiPlayTheme(content: @Composable () -> Unit) {
    MaterialTheme(
        colorScheme = KidiPlayColors,
        content = content,
    )
}
