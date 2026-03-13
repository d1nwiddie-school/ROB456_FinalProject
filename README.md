# ROB456_FinalProject
SLAMMageddon: the SLAMbulance, a SLAM, Bam, thank-you ma'am. Functional frontier exploration with ros2 and stage. 

# How to use this repo?
Frankly your guess is as good as mine. We are engineers LARPING as programmers. You'll use this repo to source a NEW overlay separate from your code, which lets us work in one unified ROS-space to freely pusha and pull without touching the work in our original ~/ROB456/ros_ws/ folders.
AI DISLOSURE: Gemini Asissted in the planning and writing of this document. Chat log is diclosed here for transparency: https://gemini.google.com/share/7a2185f3080c

# ROB456 Final Project: Group Workspace

This repository hosts the ROS2 workspace files for our final project. We are using an **Overlay Structure** to keep our group code separate from our individual course assignments.

---

## The Overlay System
Instead of working directly in `~/ROB456/ros_ws/src`, we are "stacking" this project on top of it.
* **Safety:** You won't accidentally break your personal homework files while working on the project.
* **Priority:** When you "source" this project, ROS2 will prioritize our group's `lab3` package over any others in your home directory.

---

## Initial Setup (Do this once)

1. **Create the workspace folders:**
   ```bash
   mkdir -p ~/ros_group_project/src
   cd ~/ros_group_project/src
   ```

2. **Clone the repository:**
   *Note the dot `.` at the end—it is critical to clone the contents directly into /src.*
   ```bash
   git clone https://github.com/d1nwiddie-school/ROB456_FinalProject.git.
   ```

3. **Build the code:**
   ```bash
   cd ~/ros_group_project
   colcon build --symlink-install
   ```

---

## Daily Workflow (How to run)

Every time you open a **new terminal** to work on the project, you MUST source the overlay:

```bash
source ~/ros_group_project/install/setup.bash
```

Once sourced, you can run the project exactly like the original assignments:
```bash
ros2 launch lab3 lab3.launch.py
```

---

## Working with VS Code (GUI Method)

To avoid command line errors, use the VS Code Source Control tab:

1. **Open Folder:** Open `~/ros_group_project` in VS Code.
2. **Pull (Start of session):** Click the **Source Control** icon (branch icon) -> `...` -> **Pull**.
3. **Save & Commit:** * Make your changes and save.
   * In the Source Control tab, click **+** on the files you changed to "Stage" them.
   * Type a message and click **Commit**.
4. **Push (End of session):** Click **Sync Changes** to send your work to the group.

---

## ⚠️ Important: Rules of the Road
* **No Junk:** NEVER upload the `build/`, `install/`, or `log/` folders.
* **Build Often:** If you pull new code from a teammate, run `colcon build --symlink-install` again.
* **Sync Early:** Push small updates often rather than one giant update at the end of the week.

---

## Troubleshooting
* **"Package not found":** You forgot to run `source ~/ros_group_project/install/setup.bash`.
* **Code changes aren't showing up:** Run `colcon build --symlink-install` again.
* **Git Conflicts:** Use VS Code's "Merge Editor" to choose which version of the code to keep.
