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
  - [x] Folder List (Testing complete)
  - [x] Phrase2Folder Table (Testing complete)
  - [ ] Phrase
    - [ ] Add
    - [ ] Get
    - [ ] Delete
- [ ] Add JS to handle API calls and frontend updates
  - [ ] Execution Command Update
  - [x] Folders (Testing complete)
  - [x] Phrase List
    - [x] Get Folders (Testing complete)
    - [x] Correct glitch where the GET fails to re-add the listeners  (Testing complete)
    - [ ] Get phrases
    - [ ] Load Phrase on click
  - [ ] Phrase
    - [ ] Add
    - [ ] Get
    - [ ] Delete
    - [ ] POST on lost focus of any element
