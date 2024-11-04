const Navbar = () => {
  return (
    <div className="navbar bg-base-100">
      <div className="flex-1">
        <a href="/" className="btn btn-ghost normal-case text-xl">
          WebLibManager
        </a>
      </div>
      <div className="flex-none">
        <ul className="menu menu-horizontal px-1">
          <li>
            <a href="/">Home</a>
          </li>
          <li>
            <a href="/scans">Scans</a>
          </li>
          <li>
            <a href="/files">Files</a>
          </li>
        </ul>
      </div>
    </div>
  );
};

export default Navbar;
