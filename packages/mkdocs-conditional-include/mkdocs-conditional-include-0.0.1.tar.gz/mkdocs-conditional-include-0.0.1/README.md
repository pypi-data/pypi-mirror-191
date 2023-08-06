# File exclude plugin for mkdocs

`mkdocs-exclude` is a [mkdocs plugin](http://www.mkdocs.org/user-guide/plugins/) that allows you
to conditionally include files from your input using regular expressions (regexes).

This will only include the following files in your `mkdocs`:

- file location does not have the specified prefix
- file is in the specified prefix, and matches any of the specified regexes

The big advantage of this is, that you can include your closed-source repositories into a [mkdocs monorepo](https://github.com/backstage/mkdocs-monorepo-plugin), and explicitly ONLY include your documentation sub-folders in the `mkdocs` artifacts.

## Quick start

1. Install the module using pip: `pip3 install mkdocs-conditional-include`
2. In your project, add a plugin configuration to `mkdocs.yml`:

```yaml
plugins:
  - conditional_include:
      rules:
        - prefix: my-docs
          regex:
            - '.*\/docs\/.*'
            - '.*\/docs-assets\/.*'
        - prefix: my-docs-2
          regex:
            - '.*\/docs\/.*'
```

Not specifying any prefix will run the particular rule over all files, thus filtering everything.
