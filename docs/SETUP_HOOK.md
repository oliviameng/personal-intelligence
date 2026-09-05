# Enable the IP scan hook (once per clone)

    git config core.hooksPath .githooks
    cp .ip_blocklist.local.example .ip_blocklist.local

Add codenames and names to the local file, one regex per line. It is gitignored and the hook refuses to commit it.
