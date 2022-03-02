# Lots of Phrases Fit In This
## Todo list:
#### Backend (Phrase Expansion)
- [ ] Thread out the listener from the GUI (threading module is built into python)
  - [ ] Need listener to identify what program/tab it was in. If new, reset check.
    - [ ] Need listener to identify if it is in the LOPFIT tab. If so, disable until out of tab.
    - [ ] Listener needs to detect and ignore password boxes
    - [ ] Listener needs to detect when moving from one box to another (Selenium?)

#### Frontend (GUI)
- [x] Add selector for end key (Testing complete)
- [ ] Generate API to call in phrases from the database to the GUI (flask)
  - [x] Execution Command Update
  - [x] Folder List (Testing complete)
  - [x] Phrase2Folder Table (Testing complete)
  - [ ] Phrase
    - [x] Add
    - [x] Get
    - [x] Delete
    - [ ] Post
- [ ] Add JS to handle API calls and frontend updates
  - [x] Execution Command Update
  - [x] Folders (Testing complete)
  - [x] Phrase List (Testing complete)
  - [ ] Phrase
    - [x] Add
    - [x] Get
    - [x] Delete
    - [ ] POST on Save
    - [ ] Warning on change without save?
