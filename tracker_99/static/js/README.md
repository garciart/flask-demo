# JavaScript Notes

This application uses [DataTables](https://datatables.net/ "DataTables | Javascript table library") to display, search, sort, and manipulate tables. DataTables requires:

- Bootstrap 5.3.3
- DataTables 2.2.1
- jQuery 3.7.0
- Responsive 3.0.3

These files are stored locally in the `static/js` directory.

- To ensure the files are always available, even in air-gapped systems.
- To avoid any external dependencies for security, privacy, etc.
- To allow full control over the files for customization, etc.

To learn more about DataTables, see:

- DataTables Home at <https://datatables.net/>
- DataTables Examples at <https://datatables.net/examples/index>

This application use DataTables Core, with no extensions. To learn about available extensions, see <https://datatables.net/extensions/index>.

While the application uses the minified version of JS files required by DataTables (e.g., `bootstrap.bundle.min.js`, etc.), I have included the full, uncompressed (non-minified) versions of the files (e.g., `bootstrap.bundle.js`, etc.) and the source maps (e.g., `bootstrap.bundle.js.map`, `bootstrap.bundle.min.js.map`, etc.) for debugging.
