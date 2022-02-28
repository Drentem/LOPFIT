# Lots of Phrases Fit In This
## Todo list:
#### Backend (Phrase Expansion)
- [ ] Thread out the listener from the GUI (threading module is built into python)
  - [ ] Need listener to identify what program/tab it was in. If new, reset check.
    - [ ] Need listener to identify if it is in the LOPFIT tab. If so, disable until out of tab.
#### Frontend (GUI)
- [ ] Add selector for end key (space, tab, enter, execute immediately, disable)
  - [ ] Add to GUI
  - [ ] Add JS API call to update command on backend
- [ ] Generate API to call in phrases from the database to the GUI (flask)
  - [ ] Execution Command Update
  - [x] Folder List
    - [x] Add
    - [x] Get
    - [x] Delete
  - [ ] Phrase List
    - [x] Get
    - [ ] Delete
  - [ ] Phrase
    - [ ] Add
    - [ ] Get
    - [ ] Delete
- [ ] Add JS to handle API calls and frontend updates
  - [x] Folder List
    - [x] Add
    - [x] Get
    - [ ] Delete
  - [x] Phrase List
    - [x] Get
  - [ ] Phrase
    - [ ] Add
    - [ ] Get
    - [ ] Delete
