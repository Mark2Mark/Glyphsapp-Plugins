# Show Siblings

## Plugin for Glyphsapp

This is a Plugin for the [Glyphs font editor](http://glyphsapp.com/). It superimposes a group of predefined glyphs in the background of your letters. This can be both pretty helpful in the beginning of a design as well as at intermediate progress where quick proof overview is needed. The degree of a desired match depends on each design, of course.

### How to use

Download or clone the whole `Glyphsapp-Plugins`repo (it will contain more plugins soon) and copy the `ShowSiblings.glyphsReporter` into your Glyphsapp Plugins folder (eg. `/Library/Application\ Support/Glyphs/Plugins`), restart Glyphs and when ever you need it, toggle `Show Siblings` from the view menu.

### Default groups

The default groups are as follows and can be customized in the `Contents/Resources/ShowSiblings.py`, search for the *defaultSiblings* dictionary.
```
c e o
b p
d q
h n r l
i j
t f
k x
v y
B D P R
C G O Q
H U N
K V X Y
```

### Examples

![Show Siblings Shequalin Demo](https://github.com/DeutschMark/Glyphsapp-Plugins/blob/Screenshots/ShowSiblings/Screenshots/ShowSiblings Shequalin DeutschMark.jpg?raw=true "Show Siblings Shequalin Demo")

![Show Siblings live Demo](https://github.com/DeutschMark/Glyphsapp-Plugins/blob/Screenshots/ShowSiblings/Screenshots/screencapDemoFont.gif?raw=true "Show Siblings live Demo")


### Known issues

- Removing a component doesn’t update the displayed layer in the group members until the .glyphs file is reopened.

### Pull Requests

Feel free to comment or pull requests for any improvements.

### License

Copyright 2015 [Mark Frömberg](http://www.markfromberg.com/) *@DeutschMark*

Made possible with the GlyphsSDK by Georg Seifert (@schriftgestalt) and Rainer Erich Scheichelbauer (@mekkablue).

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
