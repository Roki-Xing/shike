package cn.shike.app.ui

import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.TextStyle
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp

object ShikeColors {
    val Brand = Color(0xFF0F766E)
    val BrandSoft = Color(0xFFDDF4EE)
    val Warning = Color(0xFFF97316)
    val WarningSoft = Color(0xFFFFF7ED)
    val Info = Color(0xFF2563EB)
    val Ink = Color(0xFF101828)
    val Muted = Color(0xFF667085)
    val Surface = Color(0xFFF7FBFA)
    val Line = Color(0xFFE6EDF1)
}

object ShikeSpacing {
    val Xs = 4.dp
    val Sm = 8.dp
    val Md = 12.dp
    val Lg = 16.dp
    val Xl = 20.dp
    val Screen = Arrangement.spacedBy(12.dp)
}

object ShikeTypography {
    val Title = TextStyle(fontSize = 17.sp, fontWeight = FontWeight.Bold, color = ShikeColors.Ink)
    val Body = TextStyle(fontSize = 13.sp, lineHeight = 19.sp, color = ShikeColors.Muted)
    val Label = TextStyle(fontSize = 12.sp, fontWeight = FontWeight.SemiBold, color = ShikeColors.Muted)
    val Value = TextStyle(fontSize = 12.sp, fontWeight = FontWeight.SemiBold, color = ShikeColors.Ink)
    val Caption = TextStyle(fontSize = 11.sp, color = ShikeColors.Muted)
}
