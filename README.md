SMPEG image compression.
============

Reinventing the bicycle. Compress images like a boss. (c)

***

### Description

SMPEG stands for Style Mistake's Picture Eradication Graph. Yep.

It's a lossy compression algorithm that does compress something, but I
don't guarantee it.

Algorithm reduces image size by eliminating image data in areas containing
psychovisually irrelevant data, ie. blurry areas, smooth textures, while
keeping detailed areas as is.

It works best on live shots, but produces lots of overhead on screenshots,
clipart and other images, where PNG is the best choice.

***

### Usage

```
Usage: smpeg_app.py <options>
Options:
    -i --input <file>: Input file (required)
    -q --quality <n>: Quality of compression, 0-100 (default: 75)
    -h --help: Display this help message
```

Warning: this is purely for fun.

It doesn't support saving/loading smpeg images.

Send pull requests if you got some ideas.

***

### Contacts
Email: stylemistake@gmail.com
Web: [stylemistake.com](http://stylemistake.com)
