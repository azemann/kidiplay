package com.kidiplay.app

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import com.kidiplay.app.ui.KidiPlayApp
import com.kidiplay.app.ui.theme.KidiPlayTheme

class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContent {
            KidiPlayTheme {
                KidiPlayApp()
            }
        }
    }
}
