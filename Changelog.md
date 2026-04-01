# v1.1.1 (Hotfix)

The v1.1.0 build does not know its own version due to a bug introduced by one of the dependencies. In consquence, its update checker is broken.

- Fix application version not being embedded due to a faulty dependency update
- Fix finalizing when installation folders are parallel to the "fomod" folder (thanks to @Nithog for reporting!)

# v1.1.0

This update focuses on bug fixes and improvements to the user experience and was supported by feedback of @oOMariselaOo.

- Multiple FOMOD elements can now be edited simultanously in independent windows
- Groups and plugins are now installed in the same order they are displayed in the FCK
- FOMOD elements can now be freely copied, cut and moved from any location to any other location where they are also accepted
  - This is even possible for different FOMODs
- Fix visible tag being handled as own type
  - This affected some more complex FOMOD installers like ENB Light
- Fix finalization of folders
- Fix finalization when "Save as..." is used on the same path
- Add and expand various help texts throughout the entire app

# v1.0.1

This patch contains multiple bug fixes.

- Fix potential XML parsing errors with an encoding specifier
- Fix changes not being saved when clicking on the "Save and close" of the messagebox asking to close a dialog with unsaved changes
- FsItemEditorWidget: Fix file dialog having the wrong initial mode (`AnyFile` instead of `ExistingFile` or `Directory`)

# v1.0.0

Initial public release
