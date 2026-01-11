# GenPlexMatch

![Python](https://img.shields.io/badge/Python-3.x-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

**GenPlexMatch** is a CLI utility designed to automatically generate `.plexmatch` files for Plex Media Server. It is specifically optimized for **Anime collections** with complex directory structures, helping Plex correctly identify Seasons, OVAs, and Specials without renaming original files.

**GenPlexMatch** 是一个为 Plex Media Server 自动生成 `.plexmatch` 文件的命令行工具。它专为具有复杂目录结构（如多文件夹发布版）的**动漫收藏**优化，帮助 Plex 在不修改原始文件名的前提下，正确识别季度、OVA 和特典。

---

## 🚀 Features / 功能特性

* **📂 Complex Structure Support**: Handles mixed content (Root files + Subfolders) easily. Perfect for releases containing `Season 1`, `Season 2`, `OVAs`, and `SPs` in separate folders.
    * **复杂结构支持**：轻松处理混合内容（根目录文件+子文件夹）。完美支持包含分季、OVA 和 SP特典的文件夹结构。
* **🧠 Smart Detection**: Automatically scans for video files while ignoring irrelevant folders like `CDs`, `Scans`, or `Fonts`.
    * **智能识别**：自动扫描视频文件，同时忽略 `CDs`, `Scans`, `Fonts` 等无关文件夹。
* **🔢 Interactive Mapping**: Simply input `1`, `2`, or `0` (for Specials) to map folders to seasons. No manual text editing required.
    * **交互式映射**：只需输入 `1`、`2` 或 `0`（代表特典）即可将文件夹映射到相应季度。无需手动编辑文本。
* **🆔 TMDB Integration**: Allows writing specific TMDB IDs into the `.plexmatch` file to ensure 100% accurate metadata matching.
    * **TMDB 集成**：支持写入指定的 TMDB ID，确保元数据匹配 100% 准确。
* **✨ Specials Handling**: Automatically assigns `S00Exx` episode numbers to Specials/OVAs, preserving the order.
    * **特典处理**：自动为特典/OVA 分配 `S00Exx` 集数编号，并保持文件顺序。

## 📦 Installation / 安装

### Prerequisites / 前置要求
* Python 3.x

### Download / 下载
Clone this repository or simply download the script.
克隆本仓库或直接下载脚本文件。

## 📖 Usage / 使用方法

### 1. Basic Usage / 基本用法
Navigate to your Anime folder and run the script.
进入你的动画文件夹并运行脚本。

```bash
cd "/path/to/your/Anime/[Group] Title"
python3 /path/to/GenPlexMatch/genplexmatch.py
```

### 2. Follow the Prompts / 跟随提示
The script acts like a wizard:
脚本会像向导一样引导你：

1.  **Review**: It lists all detected folders. (确认扫描到的文件夹)
2.  **TMDB ID**: Enter the TMDB ID (Optional). (输入 TMDB ID)
3.  **Map Seasons**:
    * Enter `1` for Season 1. (输入 1 代表第一季)
    * Enter `2`, `3`... for subsequent seasons. (输入 2, 3 代表后续季度)
    * Enter `0` for Specials/OVAs (Maps to Season 0). (输入 0 代表特典/OVA)
    * Enter `s` to Skip non-video folders (e.g., Soundtracks). (输入 s 跳过无关文件夹)
4.  **Finish**: A `.plexmatch` file is generated instantly. (生成文件)

### 3. Setup Alias (Recommended) / 设置别名（推荐）
For easier access, add an alias to your shell configuration (e.g., `~/.bashrc`, `~/.zshrc`, or `~/.profile`).
为了更方便地使用，建议在你的 Shell 配置文件中添加别名。

```bash
# Add this line to your config file (replace path with actual path):
alias pm='python3 /path/to/your/GenPlexMatch/genplexmatch.py'

# Then reload config:
source ~/.bashrc  # or source ~/.profile
```

Now you can simply type `pm` inside any folder to generate the file!
现在你只需要在任何文件夹内输入 `pm` 即可生成文件！

---

## 📝 Example Scenario / 示例场景

**Directory Structure / 目录结构:**
```text
[Group] Awesome Anime/
├── [Group] Awesome Anime Season 1/      (Season 1)
├── [Group] Awesome Anime Season 2/      (Season 2)
├── [Group] Awesome Anime OVA/           (OVAs/Specials)
└── CDs/                                 (Music - to skip)
```

**Script Interaction / 脚本交互:**

```text
📁 Folder: [Group] Awesome Anime Season 1
   👉 Season? (s/0/1...): 1

📁 Folder: [Group] Awesome Anime Season 2
   👉 Season? (s/0/1...): 2

📁 Folder: [Group] Awesome Anime OVA
   👉 Season? (s/0/1...): 0

📁 Folder: CDs
   👉 Season? (s/0/1...): s
```

**Generated .plexmatch:**
```text
tmdbid:12345

season:1
ep:S01E01:[Group] Awesome Anime Season 1/[01].mkv
...

season:2
ep:S02E01:[Group] Awesome Anime Season 2/[01].mkv
...

# Specials from: [Group] Awesome Anime OVA
ep:S00E01:[Group] Awesome Anime OVA/[01].mkv
...
```

---

## ⚠️ Important Note / 重要提示

After generating the file, you must **Refresh Metadata** for the show in Plex for the changes to take effect.
生成文件后，你必须在 Plex 中对该剧集点击 **"刷新元数据" (Refresh Metadata)** 才能使更改生效。

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
