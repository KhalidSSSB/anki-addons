title: Kanji stroke color
id: kanjistrokecolor
main_file: Kanji%20stroke%20color.py
type: addon
status: hackish, desktop only
status_color: yellow
status_text_color: black
abstract: A quick hack add-on to show (colored) stroke order diagrams.
first_image: stroke%20color.png
first_alt: "The word Zustand: and a colored stroke order diagram for 況"
first_caption: Write 況 in this order.

Show colored stroke order diagrams on the desktop client, including
variants.

## Alternative

This add-on serves a similar purpose as
[cayennes](http://cayennes.github.com)’ [Kanji
colorizer](https://ankiweb.net/shared/info/1964372878). (View the code
[on githhub](https://github.com/cayennes/kanji-colorize/).)

### Pros for this add-on
* Can show stroke variants
* Does not need another field in the model
* Keeps the collection.media folder clean.

### Cons

* With this add-on, the core function, color, is not working on
  AnkiWeb/AnkiDroid/AnkiMobile.

### Difference

* This add-on shows all characters in the input field, not just the first.

### Without the add-on

When a construction like `<div
class="strokes">{{kanjiColor:Kanji}}</div>` is used on the cards and
something like
<blockquote><pre><code>.strokes {
font-size:150px;
font-family:KanjiStrokeOrders;
}</code></pre></blockquote>
in the style, it isn’t too bad on AnkiWeb or mobile devices: The kanji
will be shown with the kanji stroke order font, which uses the same
data base.

### Ospalh-special
Daring spirits can use my
[variant](https://github.com/ospalh/Anki-Android/tree/stroke-color-addon)
of [AnkiDroid](https://github.com/nicolas-raoul/Anki-Android). I have
added the equivalent of this addon, giving colored stoke order
diagrams on AnkiDroid. You should merge this branch into the newest
version of AnkiDroid, not just use that branch as-is.

## Usage

Use the template “`kanjiColor`” to see the diagrams. In the template
editor in the (front or back) template, where it says “`{{Kanji}}`”,
change it to “`{{kanjiColor:Kanji}}`”. When you use another field name
for you kanji, use that instead.

## Variants

There are three more templates, that show variant stroke order
diagrams:

### kanjiColorJinmei and kanjiColorKaisho

Using either “`{{kanjiColorJinmei:Kanji}}`” or
“`{{kanjiColorKaisho:Kanji}}`”, the Jinmei or Kaisho variant drawings
are shown, using the normal version when there is no variant.

### kanjiColorRest

<figure>
<img src="images/three_旺.png" alt="A larger colored  stroke order diagram of
旺. Below two smaller diagrams of that character. In the bottom
diagrams the third stroke is shorter. The bottom left diagram shows
the vertical sroke on the rigt drawn last.">
<figcaption>For 「旺」, there are two variant forms.</figcaption>
</figure>

Using “`{{kanjiColorRest:Kanji}}`” displays all variants of a given
kanji, and nothing when there is no variant. The variants are also
drawn smaller.

Typically you put this below a standard “`{{kanjiColor:Kanji}}`”: Like
that you always get the normal version and when there are variants,
you see them, too. For example the template for the images uses
<blockquote><pre><code>&lt;div>{{kanjiColor:Kanji}}&lt;/div>
{{kanjiColorRest:Kanji}}</code></pre></blockquote>

<blockquote class="nb">The <code>kanjiColorRest</code> template wraps the
diagrams in <code>&ltdiv class="strokevariants">...&lt;/div></code>,
 if there are any.</blockquote>


## Changing properties

### Size

The size of the displayed diagrams can be changed in the add-on’s
[source file](https://github.com/ospalh/anki-addons/blob/master/Kanji%20stroke%20color.py).
Use the “Tools/Add-ons/Kanji stroke color/Edit...” menu item to open
it. Set the size in the line “`kanji_size = 200`”. The size of the
variants shown with the “kanjiColorRest” can be set in the “`rest_size
= 120`” line.

### Colors

In the `addons` folder, there is a sub-folder named
`stroke-order-kanji`, that contains the file `_kanji_style.css`, along
with the kanji SVG files. Change the colors in this file. Use a text
editor like Wordpad, a local CSS file editor or a web service like
[CSSColorEditor](http://css-color-replace.orca-multimedia.de/).

The kanji diagrams use different CSS classes. The strokes and stroke
numbers have classes `stroke_numN` (`stroke_num1`, `stroke_num2`,
...). The strokes have the class `stroke_path`, the numbers,
`stroke_number`.

Some stroke groups also have classes. Open an SVG
file in a text (XML) editor for details. These classes are used for
the shadow effect below.

### Other effects

The SVG files load and run the script file `_kanji_script.js` from the
`stroke-order-kanji` folder. This files does nothing in the standard
installation. There is also a file `_kanji_script_shadow.js`, that
adds a shadow effect to the strokes, when renamed, where the shadow
color indicates the group. This file can be used as an inspiration or
as the basis for other effects. Animations seem possible.

<blockquote class="nb">The shadow effect may not work correctly on all
operating systems.</blockquote>

When you try the shadow effect file and the results look ugly, copy
back the original
[`_kanji_script.js`](https://raw.github.com/ospalh/kanji-colorize/etree/kanjicolorizer/extra/_kanji_script.js)
file.

### Diagrams

New diagrams with can be produced with either Cayennes'
[kanji-colorize](https://github.com/cayennes/kanji-colorize/) script
or with [my fork](https://github.com/ospalh/kanji-colorize) of it. The
diagrams that are shipped with the add-on are done with the `--mode
css` switch.


### Restart

For all of these changes to take effect, you must restart Anki.

## Data source

The diagrams use [KanjiVG](http://kanjivg.tagaini.net/) data set as the base.