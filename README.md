rpg-cards
=========

RPG spell/item/monster card generator

Preview
=======

Click [here](https://mephitrpg.github.io/rpg-cards/generator/) for a live preview of this generator.

Documentation
=============

Click [here](https://mephitrpg.github.io/rpg-cards/) to read the documentation.

Status of the project
=====================

I'm supporting this fork of the unmantained [original project](https://github.com/crobi/rpg-cards) in my spare time.
PR's are still welcome, so feel free to implement new awesome features!

FAQ
=====================

- What browsers are supported?
  - A modern browser (Chrome, Firefox, Edge, Safari). The generator has some issues on IE.
- Cards are generated without icons and background colors, what's wrong?
  - Enable printing backround images in your browser print dialog
- I can't find an icon that I've seen on [game-icons.net](http://game-icons.net), where is it?
  - See the section "updating icons" below.
- The layout of the cards is broken (e.g., cards are placed outside the page), what's wrong?
  - Check your page size, card size, and cards/page settings. If you ask the generator to place 4x4 poker-sized cards on a A4 paper, they won't fit and they will overflow the page.

Updating icons
==============

This project consists almost exclusively of static HTML/CSS/JavaScript files.
The only exception are icons, which are copied from the [game-icons](http://game-icons.net) project.

To build this project:

1. Check out this repository
2. Make sure you have [Node](https://nodejs.org/) installed
3. Run `npm install` in terminal or DOS prompt
4. Run `npm run build` in terminal or DOS prompt
5. Open `./generator/index.html` in your browser (or deploy the content of the `./generator` folder to your server)


License
=======

This generator is provided under the terms of the MIT License

Icons are made by various artists, available at [http://game-icons.net](http://game-icons.net).
They are provided under the terms of the Creative Commons 3.0 BY license.
