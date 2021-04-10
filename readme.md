# wallabag-cli

Wallabag-cli is a command line client for the self hosted read-it-later app [wallabag](https://www.wallabag.org/). Unlike to other services, wallabag is free and open source.

--------------------------------------------------------------------------------

## Documentation

Please have a look at the [documentation overview](docs/index.md) to begin using wallabag-cli.

--------------------------------------------------------------------------------

**Features**

- List entries (filterable)
- Show the content of an entry
- Add new entries
- Delete entries
- Mark existing entries as read
- Mark existing entries as starred
- Change the title of existing entries
- Export articles as file

**Include in NixOS**

In my `configuration.nix` have (among overlay definitions) this:

```
  nixpkgs.overlays =
    let
      wallbag_src = pkgs.fetchFromGitHub {
        owner  = "agschaid";
        repo   = "wallabag-cli";
        rev    = "48fd563dd785c97fc1f211bf2bca1a898bcbc8b0";
        sha256 = "02iq17nvhcxzha9g4277xzkpwzn6wrsb2pmlb83k3wlj1r4zi09r";
      };

      src_overlays = self: super: {
        wallabag_cli = import "${wallabag_src}/default.nix";
      };

      other_overlays = self: super: {
        # other stuff
      };

    in
    [other_overlays src_overlays];

    # then install wallabag_cli as usual package
```
Not sure if this is the most elegant or idiomatic way but it works.
