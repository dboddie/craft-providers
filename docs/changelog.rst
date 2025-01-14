*********
Changelog
*********

1.7.2 (2023-02-06)
------------------
- Check LXD id map before starting an existing instance.
  If the id map does not match, the instance will be auto cleaned
  or an error will be raised.
- Add `lxc.config_get()` method to retrieve config values

1.7.1 (2023-01-23)
------------------
- Set LXD id maps after launching or copying an instance
- Raise BaseConfigurationError for snap refresh failures

1.7.0 (2023-01-11)
------------------
- LXD instances launch from a cached base instance rather than a base image.
  This reduces disk usage and launch time.
- For the LXD launch function `launched_environment`, the parameter `use_snapshots`
  has been replaced by `use_base_instance`. `use_snapshots` still works but logs
  a deprecation notice.
- Expire and recreate base instances older than 3 months (90 days)
- Add `lxc.copy()` method to copy instances
- Check for network connectivity after network-related commands fail
- Add documentation for network connectivity issues inside instances
- Enable testing for Ubuntu 22.04 images
- Update `MultipassInstance.push_file_io()` to work regardless of the
  host's working directory

1.6.2 (2022-12-08)
------------------
- Disable automatic snap refreshes inside instances.

1.6.1 (2022-10-31)
------------------
- Store temporary files in the home directory
- Fix typos

1.6.0 (2022-10-06)
------------------
- Add is_running method to base Executor class
- Add new classes Provider, LXDProvider, and MultipassProvider

Note: The new Provider classes are used to encapsulate LXD and Multipass,
      from installing the provider to creating and managing instances. The code
      was leveraged from the craft applications (snapcraft, charmcraft, rockcraft,
      lpcraft), which implemented similar variations of these Provider classes.
      These classes are not stable and are likely to change. They will be stable and
      recommended for use in the release of craft-providers 2.0.

1.5.1 (2022-09-29)
------------------
- When injecting a snap, assert the snap's publisher's account
- Avoid race condition when multiple processes add a LXD remote at the same time

1.5.0 (2022-09-23)
------------------
- Add mount method to Executor base class
- LXDInstance's mount method signature has changed - The optional parameter `device_name` has been deprecated. It now matches MultipassInstance's signature of `mount(host_source, target)`
- Signed snaps injected into a provider are asserted
- Existing .snap files are not removed before overwriting with a new .snap file

1.4.2 (2022-09-09)
------------------
- Set snapd http-proxy and https-proxy
- Pass on snapd no-CDN configuration

1.4.1 (2022-08-30)
------------------
- Fix bug in BuilddBase where hostnames longer than 64 characters may
  not having trailing hyphens removed.
- Allow overriding of compatibility tag in Bases

1.4.0 (2022-08-22)
------------------
- Use LXD-compatible instance names
- Add optional list of snaps to install in bases
- Add optional list of system packages to install in bases
- Add new temporarily_pull_file function to Executor base class
- Add exists and delete function to Executor base class
- Declare more instance paths as PurePath
- Ensure BuilddBase hostname is valid
- Move .pylintrc to pyproject.toml
- Enforce line-too-long
- Fix for unit tests on non-linux platforms

Note: The provided name for a LXD executor object is converted to comply with
      LXD naming conventions for instances. This may cause a compatibility issue
      for applications that assume the LXD instance name will be identical to
      the Executor name.

      If a provided name already complies with LXD naming conventions, it is
      not modified.

1.3.1 (2022-06-09)
------------------

- Add stdin parameter for LXC commands (default: null)

1.3.0 (2022-05-21)
------------------

- Refactor snap injection logic
- Always check multipass command execution results
- Update tests and documentation

1.2.0 (2022-04-07)
------------------

- Refactor instance configuration
- Disable automatic apt actions in instance setup
- Warm-start existing instances instead of rerunning full setup
- Don't reinstall snaps already installed on target

1.1.1 (2022-03-30)
------------------

- Fix LXD user permission verification

1.1.0 (2022-03-16)
------------------

- Add buildd base alias for Jammy

1.0.5 (2022-03-09)
------------------

- Fix uid mapping in lxd host mounts

1.0.4 (2022-03-02)
------------------

- Export public API names
- Declare instance paths as PurePath
- Address linter issues
- Update documentation
