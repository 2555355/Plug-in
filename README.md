# FCL Turnip A6xx Driver Plugin

一个面向 [FCL 启动器](https://github.com/FCL-Team/FCL) 的 Turnip (Mesa freedreno) Vulkan 驱动插件，专为高通 Adreno **A6xx / A7xx** 系列 GPU 适配。

## 介绍

本插件将 Mesa Turnip 驱动以 Android APK 形式打包，通过 FCL 启动器的 `fclPlugin` 与 `driver` 元数据机制注册，使 FCL 能够加载并替换系统 Vulkan 驱动，从而在 Adreno A6xx/A7xx 设备上获得更好的兼容性与性能。

### 特性

- **驱动版本**：Mesa Turnip `26.0.0-devel` (git-`5ac41be677`)，Vulkan `1.4.335`
- **驱动来源**：[K11MCH1/AdrenoToolsDrivers](https://github.com/K11MCH1/AdrenoToolsDrivers) `v26.0.0-rc08` (Turnip_v26.0.0_R8)
- **目标 GPU**：Qualcomm Adreno A6xx / A7xx
- **架构**：`arm64-v8a`
- **SONAME 适配**：已将驱动 `DT_SONAME` 由 `vulkan.ad07xx.so` 修改为 `vulkan.adreno.so`，以匹配 FCL `linkerhook` 的 ICD 替换约定（仅修改 ELF `.dynstr` 字符串，未改动任何代码或数据）
- **插件模板**：基于 [FCL-Team/FCLDriverPlugin](https://github.com/FCL-Team/FCLDriverPlugin)

### 工作原理

FCL 启动器在运行时通过原生 `linkerhook` 拦截 `dlopen` 调用，将应用对系统 Vulkan ICD 的加载重定向到本插件内置的 `libvulkan_freedreno.so`，从而用 Turnip 驱动替代厂商驱动。本插件 APK 仅承担驱动分发职责，本身不含 UI 逻辑。

## 安装

1. 从 [Releases](../../releases) 下载最新 APK
2. 在已安装 FCL 启动器的 Android 设备上安装该 APK
3. 在 FCL 启动器的驱动管理中选择 `Turnip A6xx 26.0.0`

## 构建

项目使用 Gradle + GitHub Actions 自动构建：

```bash
./gradlew :app:assembleRelease
```

产物位于 `app/build/outputs/apk/release/`。推送到 `main` 分支或手动触发 workflow 即可在 GitHub Actions 上自动构建并发布 Release。

## 许可与归属

- 本项目代码采用 **GPL-3.0** 许可，详见 [LICENSE](LICENSE) 与 [NOTICE](NOTICE)
- 内置的 Mesa Turnip 驱动采用 **MIT** 许可，版权归 Mesa 开发者所有
- 第三方组件（Mesa、K11MCH1/AdrenoToolsDrivers、FCLDriverPlugin、FCL）的完整归属声明见 [NOTICE](NOTICE)

## AI 声明

本项目的工程化工作（包括项目结构搭建、Gradle 构建配置、GitHub Actions 工作流编写、驱动 SONAME 适配分析、LICENSE / NOTICE 归属文件的整理、以及本文档的撰写）由 AI 辅助工具协助完成。

需要明确的是：

- **驱动本身并非 AI 生成**。内置的 `libvulkan_freedreno.so` 是由 Mesa 项目上游开发者编写、并由 K11MCH1/AdrenoToolsDrivers 项目编译发布的二进制产物，本项目仅做打包与分发，不包含对驱动代码的任何修改（除前述 SONAME 字符串适配外）。
- **AI 不持有版权**。AI 辅助产出的工程代码与文档，其版权归属本项目维护者，并按 GPL-3.0 许可发布；其中涉及第三方组件的部分，相应权利与义务仍以各上游项目的原始许可为准。
- **使用者责任**。本插件按“现状”（AS IS）提供，不附带任何明示或暗示的担保。因使用本插件产生的任何直接或间接损失，维护者与 AI 工具提供方均不承担责任。
