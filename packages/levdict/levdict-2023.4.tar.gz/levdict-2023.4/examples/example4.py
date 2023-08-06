from levdict import LevDictJson

cfg = LevDictJson("example4.json")
for item in cfg.menu.popup.menuitem:
    print(f"{item.value} -> {item.onclick}")
