# Software Collection

Manage a collection of git repositories

The default storage location is /var/lib/software. Adding this repo

    sc add "https://codeberg.org/uuiouuio/software_collection.git"

will clone this repo into /var/lib/software/codeberg.org/uuiouuio/software_collection


## Usage

list

    sc list

add

    sc add "https://codeberg.org/uuiouuio/software_collection.git"

remove

    sc remove

search

    sc search <regex>

tag

    sc tag <tag> <repo> [repo...]

delete tag

    sc tag --remove <tag> <repo> [repo...]

watch/unwatch

    sc watch <repo>

    sc unwatch <repo>

whatchanged

    sc whatchanged <repo>


# collection.json

``` json
{
  tags: {
    "python": ["uuiouuio/software_collection"]
  },
  watch: {
    "uuiouuio/software_collection": "43e6116f2873c435eb7bd1840a34e8686d85c060"
  }
}

```
