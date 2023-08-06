import re
import os
import mkdocs
import mkdocs.plugins
import mkdocs.structure.files

class ConditionalInclude(mkdocs.plugins.BasePlugin):
    """A mkdocs plugin that conditionally includes all matching files with a path prefix from the input list."""

    config_scheme = (
        ('rules', mkdocs.config.config_options.Type((str, list), default=None)),
    )

    def on_files(self, files, config):

        includes = []
        excludes = []

        rules = self.config['rules'] or []
        for rule in rules:
            
            # prefix is the path prefix to include
            prefix = rule['prefix'] or ""
            if not isinstance(prefix, str):
                continue
            
            ## regexes is a list of regexes to match against the path
            regexes = rule['regex'] or []
            if not isinstance(regexes, list):
                regexes = [regexes]
            
            # if regexes is empty, do nothing for this rule
            if not regexes:
                continue

            # get all files that have the prefix and match the regexes
            for i in files:
                name = i.src_path
                if name.startswith(prefix):
                    for r in regexes:
                        if re.match(r, name):
                            includes.append(i)
                            break
                        else:
                            excludes.append(i)
        
        # remove all files that are in the includes list from the excludes list
        for i in includes:
            if i in excludes:
                excludes.remove(i)
        
        out = []

        # now exclude only has files that are not explicitly included and are in the prefix
        for i in files:
            name = i.src_path
            if i in excludes:
                continue

            # Windows reports filenames as eg.  a\\b\\c instead of a/b/c.
            # To make the same globs/regexes match filenames on Windows and
            # other OSes, let's try matching against converted filenames.
            # On the other hand, Unix actually allows filenames to contain
            # literal \\ characters (although it is rare), so we won't
            # always convert them.  We only convert if os.sep reports
            # something unusual.  Conversely, some future mkdocs might
            # report Windows filenames using / separators regardless of
            # os.sep, so we *always* test with / above.
            if os.sep != '/':
                namefix = name.replace(os.sep, '/')
                if namefix in excludes:
                    continue
            out.append(i)
        return mkdocs.structure.files.Files(out)
