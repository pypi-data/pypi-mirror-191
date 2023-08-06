from datetime import datetime
import logging
import os.path
from socket import gethostname
import subprocess
from urllib.parse import urlparse
import sys


def _find_source(source_directory, link):
    """with the given URL for a Ikiwiki post, find the source file

    This also returns the "basename" as seen from the source
    directory, to make it easier to commit the file into git later.
    """
    try:
        item_url = urlparse(link)
    except ValueError as e:
        logging.error("cannot parse item link %s: %s", link, e)
        return False
    source_path = os.path.join(source_directory, item_url.path.strip("/"))
    for ext in (".md", ".mdwn"):
        if os.path.exists(source_path + ext):
            source_path = source_path + ext
            source_basename = item_url.path.strip("/") + ext
            return source_path, source_basename
    else:
        logging.warning(
            "could not find source for %s, tried %s with .md and .mdwn extensions",
            link,
            source_path,
        )
        return None, None


def _add_directive(source_directory, source_path, source_basename, post_url):
    """add the mastodon directive to a ikiwiki post, commit and push"""
    logging.info("adding mastodon directive to post")
    now = datetime.now().isoformat()
    with open(source_path, "a", encoding="utf-8") as fp:
        fp.write("\n\n")
        fp.write(f"<!-- posted to the federation on {now} -->\n")
        fp.write(f'[[!mastodon "{post_url}"]]')
    if not fp.closed:
        logging.warning("could not write to file %s", source_path)

    logging.info("committing and pushing to git")
    commit_message = f"automatic federated post of {source_basename}\n\n"
    commit_message += f"Command: {sys.argv}\n"
    commit_message += f"Plugin file: {__file__}\n"
    commit_message += f"Source directory: {source_directory}\n"
    commit_message += "Running on: " + gethostname() + "\n"

    try:
        # TODO: make quiet when this works (unless verbose)
        subprocess.check_call(
            (
                "git",
                "-C",
                source_directory,
                "commit",
                "-m",
                commit_message,
                source_basename,
            )
        )
        subprocess.check_call(("git", "-C", source_directory, "push"))
    except subprocess.CalledProcessError as e:
        logging.warning("failed to commit and push to git: %s", e)


def output(*args, feed=None, item=None, **kwargs):
    """The toot plugin will take the given feed and pass it to the toot command

    This will generally post the update on a Mastodon server already preconfigured.

    This is *not* a standalone implementation of the Mastodon
    protocol, and is specifically tailored for integrating Mastodon
    comments inside a statically generated blog.

    In particular, it expects a "args" to point to the Ikiwiki source
    directory (not the bare repository!) where it can find the source
    file of the blog post and add the [[!mastodon]] directive so that
    comments are properly displayed.

    If no args is provided, the post is pushed without touching
    ikiwiki, but will give a warning. Use args=/dev/null to eliminate
    the warning.
    """
    try:
        source_directory = args[0]
    except IndexError:
        logging.warning(
            "no source directory provided in args, add args=/path/to/source/ to your config"
        )
        return False
    if source_directory == "/dev/null":
        source_directory = None
    if not os.path.isdir(source_directory):
        logging.warning("source directory %s not found, skipping ikiwiki editing")
        source_directory = None

    # find source file associated with the given link
    if source_directory:
        source_path, source_basename = _find_source(source_directory, item.link)

    # extract actual strings from the feedparser tags data structure
    tags = [t.get("label") or t.get("term") for t in item.tags]
    # prepend a hash sign if there is an actual tag
    tags = " ".join(["#" + t for t in tags if t])
    # construct the final post text body
    post_body = f"{item.title} {item.link} {tags}"
    logging.info("posting toot: %s", post_body)
    command = ("toot", "post", "--visibility", "public", post_body)
    logging.debug(
        "calling command: %s%s", command, feed.get("catchup", "") and " (simulated)"
    )
    if feed.get("catchup"):
        return True
    try:
        ret = subprocess.run(command, stdout=subprocess.PIPE, check=True)
    except subprocess.CalledProcessError as e:
        logging.error("failed to post toot: %s", e)
        return False
    if ret.returncode != 0:
        logging.error("failed to post toot, command failed with staus %d", ret.retcode)
        return False
    # normal output:
    # Toot posted: https://kolektiva.social/@Anarcat/109722626808467826
    _, _, post_url = ret.stdout.decode("utf-8").strip().split(maxsplit=2)

    # improved output:
    # posted http://example.com as https://kolektiva.social/@Anarcat/109722626808467826
    if not source_directory:
        print(f"posted '{post_body}' as {post_url}")
        return True

    _add_directive(source_directory, source_path, source_basename, post_url)
    # TODO: make quiet when this works reliably (unless verbose)
    print(f"posted '{post_body}' as {post_url}, metadata added to {source_path}")
    return True
