# sopel-py

Sopel Python Eval Plugin

## Important Note

This plugin relies on [a Google App Engine
service](https://github.com/sopel-irc/oblique) that still uses Python 2.7.
Google's [runtime support
schedule](https://cloud.google.com/appengine/docs/standard/lifecycle/support-schedule#python)
says they will officially end support on 30 January 2024.

While the service will still function for some indeterminate amount of time
after support ends ("End of Support" only blocks new deployments),
[eventually](https://cloud.google.com/appengine/docs/standard/lifecycle/runtime-lifecycle)
Google will Deprecate and then Decommission the `python27` App Engine runtime
entirely, at which point the backend service will no longer be available.

Replacement suggestions are welcome! Open an issue, or join us in #sopel at
Libera to discuss alternatives.

## Requirements

- Sopel 8.0+
- An `oblique` instance (see "[Configuration](#configuration)" below)

## Installation

Installing Sopel 8.0 will automatically install this plugin.

In Sopel 8.1+, use manual installation, substituting the appropriate `pip`
command if needed:

```bash
pip install sopel-py
````

### Configuration

`sopel-py` has one setting:

```ini
[py]
oblique_instance = https://oblique.sopel.chat/
```

The default value, above, points to an instance of
[oblique](https://github.com/sopel-irc/oblique) hosted by a Sopel maintainer.
See the above [important note](#important-note) about this backend service.
