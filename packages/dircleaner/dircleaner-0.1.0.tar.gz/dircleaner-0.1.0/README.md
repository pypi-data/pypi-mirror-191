cleandir
========

Organizes a directory's contents into subdirectories based on file extensions.

Say goodbye to navigating between hundreds of files in your downloads directory!


Installation
------------

```shell
pip install cleandir
```

Usage
-----

Just pass the directory to organize as an argument

```shell
cleandir <dir-name>
```

By default, cleandir organizes files using the following rules:

* audio:      flac, mp3, ogg, wav
* documents:  docx, pdf, pptx, xlsx
* misc:       7z, deb, exe, rar, zip
* pictures:   gif, jpg, png, svg, webp
* videos:     mkv, mov, mp4, webm

Extensions outside this rule are ignored

Custom rules can be passed by creating a JSON file directories and list of extensions:

```json
{
  "audio": ["mp3", "wav"],
  "code": ["py", "c", "js"],
}
```

```shell
cleandir --json-file <json-file> <dir-name>
```

If duplicates files exists in the created directory, they can be removed by using the `--delete-duplicates` flag:

```shell
cleandir -d <dir-name>
```

Available help can be seen through the `--help` flag:

```shell
cleandir --help
```