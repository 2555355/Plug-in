plugins {
    alias(libs.plugins.android.application)
    alias(libs.plugins.jetbrains.kotlin.android)
}

android {
    namespace = "com.mio.plugin.renderer"
    compileSdk = 34

    defaultConfig {
        applicationId = "com.mio.plugin.renderer"
        minSdk = 26
        targetSdk = 34
        versionCode = 3
        versionName = "1.2.0"
    }

    signingConfigs {
        create("release") {
            storeFile = file("../release.keystore")
            storePassword = System.getenv("SIGNING_STORE_PASSWORD") ?: "FCLTurnip2026"
            keyAlias = System.getenv("SIGNING_KEY_ALIAS") ?: "fcl-turnip-a6xx"
            keyPassword = System.getenv("SIGNING_KEY_PASSWORD") ?: "FCLTurnip2026"
        }
    }

    buildTypes {
        release {
            isMinifyEnabled = false
            signingConfig = signingConfigs.getByName("release")
        }
        configureEach {
            //应用名
            //app name
            resValue("string","app_name","Turnip A6xx v31")
            //包名后缀
            //package name Suffix
            applicationIdSuffix = ".turnipa6xxv31"

            //驱动在启动器内显示的名称
            //The name displayed by the driver in the launcher
            manifestPlaceholders["driver"] = "Turnip A6xx v31"
        }
    }
    compileOptions {
        sourceCompatibility = JavaVersion.VERSION_1_8
        targetCompatibility = JavaVersion.VERSION_1_8
    }
    kotlinOptions {
        jvmTarget = "1.8"
    }
}

dependencies {
}