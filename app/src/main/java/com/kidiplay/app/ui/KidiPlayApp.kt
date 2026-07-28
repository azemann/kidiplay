package com.kidiplay.app.ui

import android.graphics.BitmapFactory
import androidx.activity.compose.BackHandler
import androidx.compose.foundation.BorderStroke
import androidx.compose.foundation.Image
import androidx.compose.foundation.background
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.BoxWithConstraints
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.WindowInsets
import androidx.compose.foundation.layout.aspectRatio
import androidx.compose.foundation.layout.fillMaxHeight
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.heightIn
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.safeDrawing
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.layout.windowInsetsPadding
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material3.Button
import androidx.compose.material3.ButtonDefaults
import androidx.compose.material3.CardDefaults
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.saveable.rememberSaveable
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.ImageBitmap
import androidx.compose.ui.graphics.asImageBitmap
import androidx.compose.ui.layout.ContentScale
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.platform.testTag
import androidx.compose.ui.semantics.Role
import androidx.compose.ui.semantics.role
import androidx.compose.ui.semantics.semantics
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.kidiplay.app.ui.home.HomeLayout
import com.kidiplay.app.ui.home.homePresentation
import com.kidiplay.app.ui.theme.InkBrown
import com.kidiplay.app.ui.theme.LeafGreen
import com.kidiplay.app.ui.theme.PowderPink
import com.kidiplay.app.ui.theme.SkyBlue
import com.kidiplay.app.ui.theme.SoftOrange
import com.kidiplay.app.ui.theme.Sunshine
import com.kidiplay.app.ui.theme.WarmWhite

private enum class Destination(
    val label: String,
    val iconAsset: String,
    val kiwiAsset: String,
    val accent: Color,
) {
    Home(
        label = "Accueil",
        iconAsset = "",
        kiwiAsset = "kiwi-idle-v01.png",
        accent = Sunshine,
    ),
    Games(
        label = "Jouer",
        iconAsset = "games-v01.png",
        kiwiAsset = "kiwi-happy-v01.png",
        accent = SkyBlue,
    ),
    Drawing(
        label = "Dessiner",
        iconAsset = "drawing-v01.png",
        kiwiAsset = "kiwi-drawing-v01.png",
        accent = Sunshine,
    ),
    Gallery(
        label = "Mes images",
        iconAsset = "gallery-v01.png",
        kiwiAsset = "kiwi-guide-v01.png",
        accent = PowderPink,
    ),
}

@Composable
fun KidiPlayApp() {
    var destinationName by rememberSaveable { mutableStateOf(Destination.Home.name) }
    val destination = Destination.valueOf(destinationName)

    BackHandler(enabled = destination != Destination.Home) {
        destinationName = Destination.Home.name
    }

    BoxWithConstraints(modifier = Modifier.fillMaxSize()) {
        val presentation = homePresentation(
            widthDp = maxWidth.value.toInt(),
            heightDp = maxHeight.value.toInt(),
        )

        Background(assetName = presentation.backgroundAsset)

        if (destination == Destination.Home) {
            HomeScreen(
                layout = presentation.layout,
                onDestinationSelected = { destinationName = it.name },
            )
        } else {
            PlaceholderScreen(
                destination = destination,
                onBack = { destinationName = Destination.Home.name },
            )
        }
    }
}

@Composable
private fun Background(assetName: String) {
    AssetImage(
        assetName = assetName,
        contentDescription = null,
        modifier = Modifier.fillMaxSize(),
        contentScale = ContentScale.Crop,
    )
}

@Composable
private fun HomeScreen(
    layout: HomeLayout,
    onDestinationSelected: (Destination) -> Unit,
) {
    val safeModifier = Modifier
        .fillMaxSize()
        .windowInsetsPadding(WindowInsets.safeDrawing)
        .padding(20.dp)
        .testTag("home-screen")

    if (layout == HomeLayout.Expanded) {
        Row(
            modifier = safeModifier,
            horizontalArrangement = Arrangement.spacedBy(24.dp),
            verticalAlignment = Alignment.CenterVertically,
        ) {
            Kiwi(
                assetName = Destination.Home.kiwiAsset,
                modifier = Modifier
                    .weight(0.38f)
                    .fillMaxHeight(0.82f),
            )
            ActivityGrid(
                modifier = Modifier.weight(0.62f),
                onDestinationSelected = onDestinationSelected,
            )
        }
    } else {
        Column(
            modifier = safeModifier,
            horizontalAlignment = Alignment.CenterHorizontally,
            verticalArrangement = Arrangement.spacedBy(14.dp),
        ) {
            Kiwi(
                assetName = Destination.Home.kiwiAsset,
                modifier = Modifier
                    .weight(0.34f)
                    .fillMaxWidth(0.68f),
            )
            CompactActivities(
                modifier = Modifier.weight(0.66f),
                onDestinationSelected = onDestinationSelected,
            )
        }
    }
}

@Composable
private fun ActivityGrid(
    modifier: Modifier,
    onDestinationSelected: (Destination) -> Unit,
) {
    Column(
        modifier = modifier.fillMaxHeight(0.82f),
        verticalArrangement = Arrangement.spacedBy(18.dp),
    ) {
        ActivityCard(
            destination = Destination.Games,
            modifier = Modifier
                .fillMaxWidth()
                .weight(1f),
            onClick = { onDestinationSelected(Destination.Games) },
        )
        Row(
            modifier = Modifier
                .fillMaxWidth()
                .weight(1.18f),
            horizontalArrangement = Arrangement.spacedBy(18.dp),
        ) {
            ActivityCard(
                destination = Destination.Drawing,
                modifier = Modifier
                    .weight(1f)
                    .fillMaxHeight(),
                onClick = { onDestinationSelected(Destination.Drawing) },
            )
            ActivityCard(
                destination = Destination.Gallery,
                modifier = Modifier
                    .weight(1f)
                    .fillMaxHeight(),
                onClick = { onDestinationSelected(Destination.Gallery) },
            )
        }
    }
}

@Composable
private fun CompactActivities(
    modifier: Modifier,
    onDestinationSelected: (Destination) -> Unit,
) {
    Column(
        modifier = modifier.fillMaxWidth(),
        verticalArrangement = Arrangement.spacedBy(12.dp),
    ) {
        listOf(Destination.Games, Destination.Drawing, Destination.Gallery).forEach { destination ->
            ActivityCard(
                destination = destination,
                modifier = Modifier
                    .fillMaxWidth()
                    .weight(1f),
                onClick = { onDestinationSelected(destination) },
                horizontal = true,
            )
        }
    }
}

@Composable
private fun ActivityCard(
    destination: Destination,
    modifier: Modifier = Modifier,
    horizontal: Boolean = false,
    onClick: () -> Unit,
) {
    Surface(
        onClick = onClick,
        modifier = modifier
            .heightIn(min = 96.dp)
            .semantics { role = Role.Button }
            .testTag("activity-${destination.name.lowercase()}"),
        shape = RoundedCornerShape(30.dp),
        color = WarmWhite.copy(alpha = 0.96f),
        contentColor = InkBrown,
        border = BorderStroke(5.dp, destination.accent),
        shadowElevation = 8.dp,
    ) {
        if (horizontal) {
            Row(
                modifier = Modifier
                    .fillMaxSize()
                    .padding(horizontal = 22.dp, vertical = 10.dp),
                verticalAlignment = Alignment.CenterVertically,
                horizontalArrangement = Arrangement.spacedBy(18.dp),
            ) {
                AssetImage(
                    assetName = destination.iconAsset,
                    contentDescription = null,
                    modifier = Modifier
                        .weight(0.42f)
                        .fillMaxHeight(),
                )
                ActivityLabel(
                    text = destination.label,
                    modifier = Modifier.weight(0.58f),
                )
            }
        } else {
            Column(
                modifier = Modifier
                    .fillMaxSize()
                    .padding(14.dp),
                horizontalAlignment = Alignment.CenterHorizontally,
                verticalArrangement = Arrangement.Center,
            ) {
                AssetImage(
                    assetName = destination.iconAsset,
                    contentDescription = null,
                    modifier = Modifier
                        .weight(1f)
                        .aspectRatio(1f, matchHeightConstraintsFirst = true),
                )
                ActivityLabel(text = destination.label)
            }
        }
    }
}

@Composable
private fun ActivityLabel(
    text: String,
    modifier: Modifier = Modifier,
) {
    Text(
        text = text,
        modifier = modifier,
        color = InkBrown,
        fontSize = 26.sp,
        fontWeight = FontWeight.Bold,
        textAlign = TextAlign.Center,
        maxLines = 1,
    )
}

@Composable
private fun PlaceholderScreen(
    destination: Destination,
    onBack: () -> Unit,
) {
    Column(
        modifier = Modifier
            .fillMaxSize()
            .windowInsetsPadding(WindowInsets.safeDrawing)
            .padding(24.dp)
            .testTag("destination-${destination.name.lowercase()}"),
        horizontalAlignment = Alignment.CenterHorizontally,
        verticalArrangement = Arrangement.Center,
    ) {
        Row(
            modifier = Modifier
                .fillMaxWidth()
                .weight(1f),
            horizontalArrangement = Arrangement.Center,
            verticalAlignment = Alignment.CenterVertically,
        ) {
            Kiwi(
                assetName = destination.kiwiAsset,
                modifier = Modifier
                    .weight(1f)
                    .fillMaxHeight(0.72f),
            )
            Column(
                modifier = Modifier.weight(1f),
                horizontalAlignment = Alignment.CenterHorizontally,
                verticalArrangement = Arrangement.spacedBy(18.dp),
            ) {
                AssetImage(
                    assetName = destination.iconAsset,
                    contentDescription = null,
                    modifier = Modifier.size(180.dp),
                )
                Text(
                    text = destination.label,
                    color = InkBrown,
                    fontSize = 38.sp,
                    fontWeight = FontWeight.Bold,
                    textAlign = TextAlign.Center,
                )
                Text(
                    text = "Bientôt !",
                    color = InkBrown,
                    fontSize = 24.sp,
                    textAlign = TextAlign.Center,
                )
            }
        }
        Button(
            onClick = onBack,
            modifier = Modifier
                .fillMaxWidth()
                .heightIn(min = 64.dp)
                .testTag("back-home"),
            shape = RoundedCornerShape(28.dp),
            colors = ButtonDefaults.buttonColors(
                containerColor = LeafGreen,
                contentColor = InkBrown,
            ),
        ) {
            Text(
                text = "Retour à l’accueil",
                fontSize = 22.sp,
                fontWeight = FontWeight.Bold,
            )
        }
    }
}

@Composable
private fun Kiwi(
    assetName: String,
    modifier: Modifier = Modifier,
) {
    AssetImage(
        assetName = assetName,
        contentDescription = "Kiwi, la mascotte KidiPlay",
        modifier = modifier,
    )
}

@Composable
private fun AssetImage(
    assetName: String,
    contentDescription: String?,
    modifier: Modifier = Modifier,
    contentScale: ContentScale = ContentScale.Fit,
) {
    val bitmap = rememberAssetBitmap(assetName)
    if (bitmap != null) {
        Image(
            bitmap = bitmap,
            contentDescription = contentDescription,
            modifier = modifier,
            contentScale = contentScale,
        )
    } else {
        Box(
            modifier = modifier
                .clip(RoundedCornerShape(20.dp))
                .background(MaterialTheme.colorScheme.surface.copy(alpha = 0.85f)),
            contentAlignment = Alignment.Center,
        ) {
            Text(
                text = "Image indisponible",
                modifier = Modifier.padding(12.dp),
                color = InkBrown,
                textAlign = TextAlign.Center,
            )
        }
    }
}

@Composable
private fun rememberAssetBitmap(assetName: String): ImageBitmap? {
    val context = LocalContext.current
    return remember(assetName) {
        runCatching {
            context.assets.open(assetName).use { stream ->
                requireNotNull(BitmapFactory.decodeStream(stream)).asImageBitmap()
            }
        }.getOrNull()
    }
}
