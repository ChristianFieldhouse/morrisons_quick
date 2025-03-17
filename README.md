A python script that finds the quickest route around Morrisons for a given shopping list.

This uses adb (android debug bridge) to automate searching for the location of each
item in the Product Finder feature in the Morrisons More App. Unfortionately there
doesn't seem to be an api or a way to do this in a browser.

![Screenshot_20250317-045939](https://github.com/user-attachments/assets/e7a9aed6-7610-475d-878a-14f2e5636e9e)

Once it finds the location of each item, it finds the quickest route through the shop.
The layout of the shop is assumed to be that of Cambourne Morrisons, where aisles 1-11
are at the front, 2-22 at the back, with fresh produce next to aisle 1 and chilled food
next to aisle 12. The map_label function can be tweaked for different layouts.

All possible routes are considered and the shortest one is printed out as instructions.

```
Optimal Route:
Start at Fresh Produce (0,0)
Then go to milk - Chilled Food Aisle
Then go to toothpaste - Aisle 6
Then go to bread - Aisle 19
Then go to eggs - Aisle 20
Then go to yogurt - Aisle 21
Then go to frozen pizza - Aisle 10
```

The Morrisons More App does give a bit more detail about the locations of items, not
just the aisle number, but I'm not using that.

