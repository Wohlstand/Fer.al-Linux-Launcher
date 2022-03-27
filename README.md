# Fer.al-Linux-Launcher
The Unofficial launcher for the Fer.al online game for the Linux operating systems that makes the game work on these operating systems.

**Unfortunately, became trash because Fer.al game itself has closed by Wildworks as it got no success in the business.**

# Backstory
It's my hand-made launcher for the Fer.al game by Wildworks, that allows the game to work on Linux distros in a condition it has enough hardware support (Vulkan is required to work).

Why did I make my custom launcher? Because the official launcher program doesn't work at all because of its internal bugs (nobody fixed them for a whole time). So, I made my own.

What the launcher does:
- Checks the presence of the game package. If it is absent, attempt to download it and unpack it.
- Performs update checks and automatic updates if needed. If the version reported by the official server is newer than the local copy, it downloads the updated version from the official server.
- Runs the game if no updates are needed.

The official launcher also has a built-in tracker that sends various reports to Wildworks. My launcher doesn't that, as this is totally unnecessary functionality.

The game requires Windows 10 and DirectX 12 support. However, it's possible to run the game using the DXVK module that wraps DirectX API over Vulkan. (so, Wine should be configured to use Windows 10 mode).

Additionally, the game REQUIRES the virtual screen at the Wine side, otherwise, once you switch into another window, the game will become uncontrollable (will don't respond on the mouse and keyboard events) if run the game without Wine's virtual window.

I wanted to make it being easy-to-install by adding an automatic building of the compatible Wine environment with installing of all necessary dependencies but hadn't much mood to build that, and additionally, I had paused to play the game for a long time. Unfortunately, when I randomly tried to launch the game on the 27'th of March 2022 to check what's new at the game, I suddenly learned the sad fact that the game has been closed by Wildworks. And the more sudden fact that it got closed YESTERDAY.

So, I just gonna to publish the stuff I made in as-is unfinished form. Probably it could be useful for anybody also as an example how to run other games like this.

---
Good luck and have fun!

Vitaly Novichkov "Wohlstand", 27'th of March, 2022.
