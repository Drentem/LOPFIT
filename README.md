# Lots of Phrases Fit In This
## Todo list:
#### Backend (Phrase Expansion)
- [ ] Thread out the listener from the GUI (threading module is built into python)
  - [ ] Need listener to identify what program/tab it was in. If new, reset check.
    - [x] Need listener to identify if it is in the LOPFIT tab. If so, disable until out of tab. (Handled through the frontend actually)

    - [ ] Listener needs to detect when moving from one box to another (Selenium?)
- [ ] OS Specific handlers
  - [ ] Windows
    - [ ] Clipboard
      - [ ] Copy current clipboard to temp var
      - [ ] Copy phrase to clipboard
      - [ ] Add TODO block for future form handling
      - [ ] Paste phrase to current keyboard location (Possibly via CTRL-V)
      - [ ] Replace temp var back to clipboard (as if we never borrowed it)
      - [ ] Listener needs to detect and ignore password boxes
  - [ ] MacOS
    - [x] Clipboard
- [ ] Integrate with GUI


#### Frontend (GUI)
### COMPLETE!!!
- [x] Add selector for end key (Testing complete)
- [x] Generate API to call in phrases from the database to the GUI (Testing complete)
- [x] Add JS to handle API calls and frontend updates (Testing complete)
- [x] Fix new phrase problem where it does not save to the correct phrase (Testing complete)

#### Bugs needing worked
- [ ] Knowing when the form is dirty after saving
  - Could just consider it dirty after ANY change regardless if undo returned it back to normal
