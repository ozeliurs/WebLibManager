import { useState, useEffect } from "react";

const FilesystemBrowser = ({ onSelectPath }) => {
  const [currentPath, setCurrentPath] = useState("/");
  const [contents, setContents] = useState({ dirs: [], files: [] });

  useEffect(() => {
    fetch(`https://weblibmanager.ozeliurs.com/api/fs/?path=${currentPath}`)
      .then((res) => res.json())
      .then((data) => setContents(data));
  }, [currentPath]);

  const navigateUp = () => {
    setCurrentPath((prev) => {
      const parts = prev.split("/").filter(Boolean);
      parts.pop();
      return parts.length === 0 ? "/" : "/" + parts.join("/");
    });
  };

  const navigateToDir = (dir) => {
    setCurrentPath((prev) => {
      const base = prev === "/" ? "" : prev;
      return `${base}/${dir}`;
    });
  };

  return (
    <div className="card bg-base-100 shadow-xl">
      <div className="card-body">
        <h2 className="card-title">Filesystem Browser</h2>
        <div className="text-sm breadcrumbs">
          <ul>
            <li>{currentPath}</li>
          </ul>
        </div>
        <div className="grid grid-cols-1 gap-2">
          <button className="btn btn-sm" onClick={navigateUp}>
            ../
          </button>
          {contents.dirs.map((dir) => (
            <button
              key={dir}
              className="btn btn-sm"
              onClick={() => navigateToDir(dir)}
            >
              📁 {dir}
            </button>
          ))}
        </div>
        <div className="card-actions justify-end">
          <button
            className="btn btn-primary"
            onClick={() => onSelectPath(currentPath)}
          >
            Scan this directory
          </button>
        </div>
      </div>
    </div>
  );
};

export default FilesystemBrowser;
