# Welcome to [Slidev](https://github.com/slidevjs/slidev)!

To start the slide show:

- `npm install`
- `npm run dev`
- visit http://localhost:3030

Edit the [slides.md](./slides.md) to see the changes.

Learn more about Slidev on [documentations](https://sli.dev/).

## Tasks

### refresh-diagrams

dir: diagrams

```sh
ls *.d2 | xargs -I {} nix run nixpkgs#d2 -- --layout=elk --theme=200 {}
mv *.svg ../public
```

### update-dynamodb-diagrams

```sh
dynamotableviz -sk=sk -attrs=purchaseDate,expires,type -file ./single-table-design.txt > single-table-design.html
dynamotableviz -sk=sk -attrs=_seq,_type,_date -file ./event-sourced-design.txt > event-sourced-design.html
```
